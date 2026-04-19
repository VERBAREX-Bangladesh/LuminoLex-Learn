import gc
import sys
import subprocess
import warnings

from rich.console import Console
from rich.rule import Rule

from luminolex.config import MODEL_NAME, ADAPTER_REPO, DISPLAY_MODEL, BRAND, BRAND_DIM, INFO, SUCCESS, TEXT_DIM, TEXT_MAIN

console = Console()


def _ensure_bitsandbytes():
    try:
        import bitsandbytes as bnb
        from packaging.version import Version
        if Version(bnb.__version__) < Version("0.46.1"):
            raise ImportError
    except Exception:
        console.print(f"  [{INFO}]Installing bitsandbytes>=0.46.1...[/]")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-U", "bitsandbytes>=0.46.1"],
            check=True,
        )
        if "bitsandbytes" in sys.modules:
            del sys.modules["bitsandbytes"]


class LoadingStep:
    def __init__(self, label: str):
        self.label = label

    def __enter__(self):
        from rich.live import Live
        from rich.spinner import Spinner
        self._live = Live(
            Spinner("dots2", text=f"[{BRAND}] {self.label}[/]", style=f"bold {BRAND}"),
            console=console,
            refresh_per_second=20,
            transient=True,
        )
        self._live.__enter__()
        return self

    def __exit__(self, *args):
        self._live.__exit__(*args)
        console.print(f"  [{SUCCESS}]✔[/]  [bold {TEXT_MAIN}]{self.label}[/]")


def load(verbose: bool = True):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import PeftModel

    warnings.filterwarnings("ignore", message=".*copying from a non-meta parameter.*")
    warnings.filterwarnings("ignore", message=".*torch_dtype.*deprecated.*")

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

    _ensure_bitsandbytes()

    if verbose:
        console.print(Rule(f"[bold {BRAND}] LuminoLex Learn — {DISPLAY_MODEL} [/]", style=BRAND_DIM))
        console.print()

    has_cuda = torch.cuda.is_available()
    if has_cuda:
        props    = torch.cuda.get_device_properties(0)
        vram_gb  = props.total_memory / 1e9
        if verbose:
            console.print(f"  [{INFO}]GPU:[/] {props.name}  [{TEXT_DIM}]{vram_gb:.1f} GB[/]")
            console.print()
    else:
        vram_gb = 0
        if verbose:
            console.print(f"  [{TEXT_DIM}]No GPU detected — CPU mode (slow)[/]\n")

    with LoadingStep("Loading tokenizer"):
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token_id = tokenizer.eos_token_id

    with LoadingStep("Loading base model (4-bit NF4)"):
        bnb_cfg = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        base = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            quantization_config=bnb_cfg,
            device_map="auto",
            max_memory={0: "13GiB", "cpu": "6GiB"},
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            attn_implementation="eager",
        )

    with LoadingStep("Attaching LoRA adapter"):
        try:
            model = PeftModel.from_pretrained(base, ADAPTER_REPO, is_trainable=False)
        except Exception:
            gc.collect()
            if has_cuda:
                torch.cuda.empty_cache()
            base = base.to("cpu")
            model = PeftModel.from_pretrained(base, ADAPTER_REPO, device_map=None, is_trainable=False)
            if has_cuda:
                model = model.cuda()

        model.eval()

    gc.collect()
    if has_cuda:
        torch.cuda.empty_cache()
        used  = torch.cuda.memory_allocated() / 1e9
        total = torch.cuda.get_device_properties(0).total_memory / 1e9
        if verbose:
            console.print()
            console.print(
                f"  [{SUCCESS}]Ready[/]  VRAM {used:.1f} / {total:.1f} GB  "
                f"[{TEXT_DIM}]device: {next(model.parameters()).device}[/]"
            )
    else:
        if verbose:
            console.print(f"\n  [{SUCCESS}]Ready (CPU)[/]")

    console.print()
    return model, tokenizer
