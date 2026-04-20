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
        print("\n  ✖  Dependencies were upgraded but the model architecture is still not recognised.")
        print("     This usually means Colab cached the old version.")
        print("\n  ➜  Please run this ONE cell in Colab, then re-run the script:\n")
        print("     !pip install -q git+https://github.com/huggingface/transformers.git")
        print("     Then:  Runtime → Restart session  →  re-run this cell.\n")
        sys.exit(1)

    print("\n  ⚡  Required model architecture not found in current transformers.")
    print("     Upgrading from GitHub main branch (this takes ~30 s) …\n")

    cmds = [
        [sys.executable, "-m", "pip", "install", "-q", "--upgrade",
         "git+https://github.com/huggingface/transformers.git"],
        [sys.executable, "-m", "pip", "install", "-q", "--upgrade",
         "git+https://github.com/huggingface/accelerate.git"],
        [sys.executable, "-m", "pip", "install", "-q", "--upgrade", "peft"],
        [sys.executable, "-m", "pip", "install", "-q", "bitsandbytes>=0.46.1"],
    ]
    for cmd in cmds:
        rc = subprocess.run(cmd).returncode
        if rc != 0:
            print(f"  ✖  Command failed: {' '.join(cmd)}\n")
            sys.exit(1)

    print("\n  ✔  Packages upgraded — restarting process to load new libraries …\n")
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
        print("  ℹ  Colab/Jupyter detected.")
        print("     ➜  Go to:  Runtime → Restart session  then re-run this cell.\n")
        print("     (The upgrade is already done — only a session restart is needed.)\n")
        sys.exit(0)
    else:
        os.execve(sys.executable, [sys.executable] + sys.argv, env)
