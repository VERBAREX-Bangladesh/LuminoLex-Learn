import gc
import sys
import time
import threading
import re
import subprocess

import config
from ui import console, LoadingStep, Rule

def load_model():
    import warnings
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel, PeftConfig

    warnings.filterwarnings("ignore", message=".*copying from a non-meta parameter.*")
    warnings.filterwarnings("ignore", message=".*torch_dtype.*deprecated.*")

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

    try:
        import bitsandbytes as _bnb
        from packaging.version import Version
        if Version(_bnb.__version__) < Version("0.46.1"):
            raise ImportError("too old")
    except Exception:
        console.print(f"  [{config.INFO}]Installing bitsandbytes>=0.46.1 …[/]")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-U", "bitsandbytes>=0.46.1"],
            check=True
        )
        import importlib
        if "bitsandbytes" in sys.modules:
            del sys.modules["bitsandbytes"]

    console.print(Rule(f"[bold {config.BRAND}] Loading LuminoLex Learn [/]", style=config.BRAND_DIM))
    console.print()

    has_cuda = torch.cuda.is_available()
    if has_cuda:
        vram_gb  = torch.cuda.get_device_properties(0).total_memory / 1e9
        gpu_name = torch.cuda.get_device_properties(0).name
        console.print(f"  [{config.INFO}]GPU:[/] [bold]{gpu_name}[/]  [{config.TEXT_DIM}]{vram_gb:.1f} GB VRAM[/]")
    else:
        vram_gb = 0
        console.print(f"  [{config.TEXT_DIM}]No GPU found — running on CPU (will be slow)[/]")

    console.print()

    with LoadingStep("Fetching base model configuration …"):
        # Dynamically determine the base model without hardcoding its name
        peft_config = PeftConfig.from_pretrained(config.ADAPTER_REPO)
        base_model_path = peft_config.base_model_name_or_path

    with LoadingStep("Loading tokenizer …"):
        tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token_id = tokenizer.eos_token_id

    with LoadingStep("Loading base model in 4-bit NF4 (streaming to GPU) …"):
        from transformers import BitsAndBytesConfig
        bnb_cfg = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            quantization_config=bnb_cfg,
            device_map="auto",
            max_memory={0: "13GiB", "cpu": "6GiB"},
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            attn_implementation="eager",
        )

    with LoadingStep("Attaching LuminoLex Learn adapter …"):
        try:
            model = PeftModel.from_pretrained(
                base_model, config.ADAPTER_REPO, is_trainable=False
            )
        except Exception:
            gc.collect()
            if has_cuda:
                torch.cuda.empty_cache()
            base_model = base_model.to("cpu")
            model = PeftModel.from_pretrained(
                base_model, config.ADAPTER_REPO, device_map=None, is_trainable=False
            )
            if has_cuda:
                model = model.cuda()

        model.eval()

    gc.collect()
    if has_cuda:
        torch.cuda.empty_cache()
        used  = torch.cuda.memory_allocated() / 1e9
        total = torch.cuda.get_device_properties(0).total_memory / 1e9
        console.print()
        console.print(f"  [{config.SUCCESS}] Model ready  │  "
                      f"VRAM: [bold]{used:.1f}[/] / {total:.1f} GB  │  "
                      f"Device: [bold {config.INFO}]{next(model.parameters()).device}[/]")
    else:
        console.print()
        console.print(f"  [{config.SUCCESS}] Model ready on CPU")

    console.print()
    return model, tokenizer

def _run_inference(model, tokenizer, messages, params, result_box):
    import torch
    try:
        model_inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            enable_thinking=False,
            return_dict=True,
            return_tensors="pt",
        ).to(next(model.parameters()).device)

        with torch.no_grad():
            outputs = model.generate(
                **model_inputs,
                max_new_tokens=params["max_new_tokens"],
                do_sample=True,
                temperature=params["temperature"],
                top_p=params["top_p"],
                repetition_penalty=params["repetition_penalty"],
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

        input_length = model_inputs.input_ids.shape[1]
        generated_ids = outputs[0][input_length:]
        full_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

        # Strip any leaked thinking tags as a safety net
        text = re.sub(r"<think>.*?(?:</think>|$)", "", full_text, flags=re.DOTALL).strip()

        result_box["output"]  = text
        result_box["in_tok"]  = input_length
        result_box["out_tok"] = len(generated_ids)
    except Exception as exc:
        result_box["error"] = str(exc)

def generate_with_spinner(model, tokenizer, messages, params):
    result_box: dict = {}
    t = threading.Thread(
        target=_run_inference,
        args=(model, tokenizer, messages, params, result_box),
        daemon=True,
    )
    t.start()

    frames = ["◐", "◓", "◑", "◒"]
    frame_i = 0
    start = time.time()
    while t.is_alive():
        elapsed = time.time() - start
        frame   = frames[frame_i % len(frames)]
        console.print(
            f"\r  [{config.BRAND}]{frame}[/] [dim]Thinking … {elapsed:.1f}s[/]",
            end="", highlight=False,
        )
        frame_i += 1
        time.sleep(0.12)
    t.join()
    console.print("\r" + " " * 40 + "\r", end="", highlight=False)

    if "error" in result_box:
        raise RuntimeError(result_box["error"])
    return result_box.get("output", ""), result_box.get("in_tok", 0), result_box.get("out_tok", 0)
