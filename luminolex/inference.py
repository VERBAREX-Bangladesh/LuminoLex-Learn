import re
import time
import threading

from rich.console import Console

from luminolex.config import BRAND

console = Console()


def _generate(model, tokenizer, messages, params, out: dict):
    import torch
    try:
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            enable_thinking=False,
            return_dict=True,
            return_tensors="pt",
        ).to(next(model.parameters()).device)

        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=params["max_new_tokens"],
                do_sample=True,
                temperature=params["temperature"],
                top_p=params["top_p"],
                repetition_penalty=params["repetition_penalty"],
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

        prompt_len     = inputs.input_ids.shape[1]
        generated_ids  = output_ids[0][prompt_len:]
        raw            = tokenizer.decode(generated_ids, skip_special_tokens=True)
        text           = re.sub(r"<think>.*?(?:</think>|$)", "", raw, flags=re.DOTALL).strip()

        out["text"]    = text
        out["in_tok"]  = prompt_len
        out["out_tok"] = len(generated_ids)

    except Exception as exc:
        out["error"] = str(exc)


def run(model, tokenizer, messages: list[dict], params: dict) -> tuple[str, int, int]:
    out: dict = {}

    worker = threading.Thread(
        target=_generate,
        args=(model, tokenizer, messages, params, out),
        daemon=True,
    )
    worker.start()

    frames = ["◐", "◓", "◑", "◒"]
    i, t0  = 0, time.time()

    while worker.is_alive():
        elapsed = time.time() - t0
        console.print(
            f"\r  [{BRAND}]{frames[i % 4]}[/] [dim]Thinking … {elapsed:.1f}s[/]",
            end="",
            highlight=False,
        )
        i += 1
        time.sleep(0.12)

    worker.join()
    console.print("\r" + " " * 30 + "\r", end="", highlight=False)

    if "error" in out:
        raise RuntimeError(out["error"])

    return out.get("text", ""), out.get("in_tok", 0), out.get("out_tok", 0)
