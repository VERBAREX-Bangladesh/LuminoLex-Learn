import os
import sys
import subprocess

_FLAG = "__LUMINOLEX_UPGRADED__"


def _model_arch_available() -> bool:
    try:
        from transformers.models.auto.configuration_auto import CONFIG_MAPPING
        return "qwen3_5" in CONFIG_MAPPING
    except Exception:
        return False


def ensure_dependencies():
    if _model_arch_available():
        return

    if os.environ.get(_FLAG) == "1":
        print("Upgrade completed but the model architecture is still not available.")
        print("If you are on Colab: Runtime → Restart session, then re-run.")
        sys.exit(1)

    print("Model architecture not found in current transformers. Upgrading dependencies...\n")

    packages = [
        "git+https://github.com/huggingface/transformers.git",
        "git+https://github.com/huggingface/accelerate.git",
        "peft",
        "bitsandbytes>=0.46.1",
    ]

    for pkg in packages:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "--upgrade", pkg]
        )
        if result.returncode != 0:
            print(f"Failed to install: {pkg}")
            sys.exit(1)

    env = os.environ.copy()
    env[_FLAG] = "1"

    in_notebook = False
    try:
        from IPython import get_ipython
        if get_ipython() is not None:
            in_notebook = True
    except ImportError:
        pass

    if in_notebook:
        print("Upgrade done. Go to Runtime → Restart session, then re-run.")
        sys.exit(0)

    os.execve(sys.executable, [sys.executable] + sys.argv, env)
