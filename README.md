<div align="center">

```
  ██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗ ██████╗ ██╗     ███████╗██╗  ██╗
  ██║     ██║   ██║████╗ ████║██║████╗  ██║██╔═══██╗██║     ██╔════╝╚██╗██╔╝
  ██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║██║   ██║██║     █████╗   ╚███╔╝ 
  ██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║   ██║██║     ██╔══╝   ██╔██╗ 
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████╗███████╗██╔╝ ██╗
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝

                          L E A R N   E D I T I O N
```

**A rich terminal chat interface for LuminoLex Learn · Powered by VERBAREX**

</div>

---

## Overview

LuminoLex Learn is a terminal-based chat application that loads the **VERBAREX/LuminoLexV1-9B** adapter on top of **Qwen3.5-9B** (4-bit NF4 quantized). It features a beautiful `rich`-powered UI with animated banners, chat bubbles, a typewriter effect, and session-persistent user memory.

---

## Requirements

- Python **3.10+**
- A CUDA GPU with **≥ 13 GB VRAM** (e.g. NVIDIA A100, L4, or RTX 3090+)
- Or: Google Colab with a **T4 / A100** GPU (free/Pro tier)

---

## Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/luminolex-learn.git
cd luminolex-learn

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python luminolex_learn.py
```

> **Note:** On first run the script will auto-upgrade `transformers` from GitHub main if the `qwen3_5` architecture is not found in your installed version. This takes ~30 seconds and then restarts automatically.

---

## Google Colab

A ready-to-use Colab notebook is included: **`LuminoLex_Learn_Colab.ipynb`**

See the [Colab Instructions](#colab-instructions) section below for the step-by-step guide.

---

## Chat Commands

| Command | Description |
|---|---|
| `?` or `/help` | Show the help panel |
| `/clear` | Wipe the screen and reset session |
| `/history` | Print full conversation history |
| `/tokens` | Show token usage stats for this session |
| `/system <prompt>` | Replace the system prompt on-the-fly |
| `/temp <0.1–2.0>` | Change temperature (default: `0.8`) |
| `/maxtok <int>` | Change max_new_tokens (default: `2048`) |
| `/learn <fact>` | Teach the model a fact about you — persists all session |
| `/learned` | Show everything the model has learned about you |
| `/forget` | Wipe all learned facts |
| `/save [file]` | Save the conversation to a `.txt` file |
| `/exit` or `/quit` | Exit LuminoLex Learn |

---

## Generation Parameters (defaults)

| Parameter | Default |
|---|---|
| `max_new_tokens` | `2048` |
| `temperature` | `0.8` |
| `top_p` | `0.9` |
| `repetition_penalty` | `1.1` |

---

## Colab Instructions

### Step 1 — Open the Notebook

Upload `LuminoLex_Learn_Colab.ipynb` to [colab.research.google.com](https://colab.research.google.com) or open it directly from GitHub via **File → Open notebook → GitHub tab**.

### Step 2 — Enable GPU

Go to **Runtime → Change runtime type** and select:
- Hardware accelerator: **T4 GPU** (free tier) or **A100** (Colab Pro)

Click **Save**.

### Step 3 — Run the Cells in Order

**Cell 1** — Clones this repo into Colab's filesystem:
```python
!git clone https://github.com/YOUR_USERNAME/luminolex-learn.git
%cd luminolex-learn
```

**Cell 2** — Installs all Python dependencies:
```python
!pip install -q torch transformers peft accelerate rich bitsandbytes>=0.46.1 packaging
```

**Cell 3** — *(Only if needed)* Upgrades `transformers` from GitHub if Qwen3.5 is not supported:
```python
!pip install -q git+https://github.com/huggingface/transformers.git
```
After this cell finishes: **Runtime → Restart session**, then skip straight to Cell 4.

**Cell 4** — Launches the chat:
```python
!python luminolex_learn.py
```

The model will download and load (~5–10 minutes on first run). After that you will see the animated LuminoLex banner and a prompt. Type normally and press **Enter** to chat.

### Stopping the Session

Type `/exit` or `/quit` in the chat prompt, or press the **Stop** button (■) on the running cell.

---

## File Structure

```
luminolex-learn/
├── luminolex_learn.py          # Main application
├── LuminoLex_Learn_Colab.ipynb # Ready-to-use Colab notebook
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## Credits

Built by **VERBAREX**. Base model: [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B). Adapter: [VERBAREX/LuminoLexV1-9B](https://huggingface.co/VERBAREX/LuminoLexV1-9B).
