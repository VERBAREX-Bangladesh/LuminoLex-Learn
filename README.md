# LuminoLex Learn

```
  ██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗ ██████╗ ██╗     ███████╗██╗  ██╗
  ██║     ██║   ██║████╗ ████║██║████╗  ██║██╔═══██╗██║     ██╔════╝╚██╗██╔╝
  ██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║██║   ██║██║     █████╗   ╚███╔╝
  ██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║   ██║██║     ██╔══╝   ██╔██╗
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████╗███████╗██╔╝ ██╗
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
```

**LuminoLex Learn** is a terminal-based AI chat interface powered by the `VERBAREX/LuminoLexV1-9B` model — a fine-tuned adapter on top of `Qwen/Qwen3.5-9B`, loaded in 4-bit NF4 quantization for efficient inference.

> Built by **VERBAREX**

---

## Features

- 🚀 **4-bit NF4 quantization** via `bitsandbytes` — runs on ~13 GB VRAM
- 🧠 **Session memory** — teach the model facts about you with `/learn`
- 💬 **Rich terminal UI** — animated banner, chat bubbles, spinner, typewriter effect
- 🔧 **Live parameter control** — change temperature, max tokens, and system prompt on the fly
- 💾 **Export conversations** to text files with `/save`
- 🔄 **Auto-bootstrap** — automatically upgrades `transformers` if the model architecture isn't available

---

## Requirements

- Python 3.10+
- CUDA-capable GPU with ~13 GB VRAM (recommended) — CPU fallback available but slow
- Internet connection on first run (to download model weights)

---

## Installation

```bash
git clone https://github.com/VERBAREX-Bangladesh/LuminoLex-Learn.git
cd luminolex-learn
pip install -r requirements.txt
```

---

## Usage

```bash
python luminolex_learn.py
```

On first run the script will:
1. Check if your installed `transformers` supports the model architecture.
2. Auto-upgrade packages if needed.
3. Download and cache the base model + adapter from Hugging Face.
4. Launch the interactive chat REPL.

---

## Chat Commands

| Command | Description |
|---|---|
| `/help` or `?` | Show the help panel |
| `/clear` | Wipe the screen and reset the session |
| `/history` | Print full conversation history |
| `/tokens` | Show token usage stats for this session |
| `/system <prompt>` | Replace the system prompt on-the-fly |
| `/temp <0.1-2.0>` | Change temperature (default: 0.8) |
| `/maxtok <int>` | Change max_new_tokens (default: 2048) |
| `/learn <fact>` | Teach the model a fact about you — persists all session |
| `/learned` | Show everything the model has learned about you |
| `/forget` | Wipe all learned facts |
| `/save [file]` | Save conversation to a text file |
| `/exit` or `/quit` | Exit LuminoLex Learn |

---

## Google Colab

If you're running in Google Colab and the architecture upgrade is needed, you will be prompted to:

```
Runtime → Restart session → re-run the cell
```

The upgrade installs from the Hugging Face `transformers` GitHub main branch. This is a one-time step.

---

## Model Details

| Field | Value |
|---|---|
| Base model | `Qwen/Qwen3.5-9B` |
| Adapter | `VERBAREX/LuminoLexV1-9B` |
| Quantization | 4-bit NF4 (bitsandbytes) |
| Compute dtype | `bfloat16` |
| Max VRAM | ~13 GB |

---

## License

See [LICENSE](LICENSE).
