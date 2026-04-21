import re
import time
import threading

from rich.console import Console
from luminolex.config import BRAND, BRAND_DIM

console = Console()


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
            f"\r  [{BRAND}]{frame}[/] [dim]Thinking … {elapsed:.1f}s[/]",
            end="", highlight=False,
        )
        frame_i += 1
        time.sleep(0.12)
    t.join()
    console.print("\r" + " " * 40 + "\r", end="", highlight=False)

    if "error" in result_box:
        raise RuntimeError(result_box["error"])
    return result_box.get("output", ""), result_box.get("in_tok", 0), result_box.get("out_tok", 0)
