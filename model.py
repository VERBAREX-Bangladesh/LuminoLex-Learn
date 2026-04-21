import gc
import sys
import subprocess
import warnings

from rich.console import Console
from rich.rule import Rule
from luminolex.config import BRAND, BRAND_DIM, TEXT_DIM, SUCCESS, INFO, DANGER

console = Console()

_BASE_MODEL   = "Qwen/Qwen3.5-9B"
_ADAPTER_REPO = "VERBAREX/LuminoLexV1-9B"


def load_model():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

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
        console.print(f"  [{INFO}]Installing bitsandbytes>=0.46.1 …[/]")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-U", "bitsandbytes>=0.46.1"],
            check=True
        )
        if "bitsandbytes" in sys.modules:
            del sys.modules["bitsandbytes"]

    console.print(Rule(f"[bold {BRAND}] Loading LuminoLex Learn [/]", style=BRAND_DIM))
    console.print()

    has_cuda = torch.cuda.is_available()
    if has_cuda:
        vram_gb  = torch.cuda.get_device_properties(0).total_memory / 1e9
        gpu_name = torch.cuda.get_device_properties(0).name
        console.print(f"  [{INFO}]GPU:[/] [bold]{gpu_name}[/]  [{TEXT_DIM}]{vram_gb:.1f} GB VRAM[/]")
    else:
        console.print(f"  [{TEXT_DIM}]No GPU found — running on CPU (will be slow)[/]")

    console.print()

    from luminolex.ui import LoadingStep

    with LoadingStep("Loading tokenizer …"):
        tokenizer = AutoTokenizer.from_pretrained(_BASE_MODEL, trust_remote_code=True)
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
            _BASE_MODEL,
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
                base_model, _ADAPTER_REPO, is_trainable=False
            )
        except Exception:
            gc.collect()
            if has_cuda:
                torch.cuda.empty_cache()
            base_model = base_model.to("cpu")
            model = PeftModel.from_pretrained(
                base_model, _ADAPTER_REPO, device_map=None, is_trainable=False
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
        console.print(f"  [{SUCCESS}] Model ready  │  "
                      f"VRAM: [bold]{used:.1f}[/] / {total:.1f} GB  │  "
                      f"Device: [bold {INFO}]{next(model.parameters()).device}[/]")
    else:
        console.print()
        console.print(f"  [{SUCCESS}] Model ready on CPU")

    console.print()
    return model, tokenizer
