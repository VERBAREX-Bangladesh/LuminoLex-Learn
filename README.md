# LuminoLex Learn

> **An uncensored terminal AI chat that learns about you — Powered by VERBAREX**

LuminoLex Learn is a local terminal chat application built on **Qwen3.5-9B** with the **VERBAREX/LuminoLexV1-9B** LoRA adapter. It is **fully uncensored** — it answers directly and thoroughly without moralizing, warnings, or refusals. On top of that, its defining feature is a **session memory system**: as you use `/learn` to share facts about yourself, the model builds a user profile and naturally incorporates that knowledge into every response — no re-prompting needed.

---

## How the Learning Works

When you use the `/learn` command, the fact is stored in a live user profile for your session:

```
/learn I'm a software engineer in Dhaka
/learn I prefer concise answers with code examples
/learn I'm currently learning Rust
```

These facts are silently injected into the system context before every reply, so the model responds with awareness of who you are and what you care about — without you having to repeat yourself.

You can inspect the profile at any time with `/learned` and wipe it with `/forget`.

---

## Features

- 🔓 **Fully uncensored** — responds directly and thoroughly with no refusals, warnings, or moralizing
- 🧠 **Learns about you** — builds a persistent user profile through `/learn` that shapes every response
- 🚀 **4-bit NF4 quantization** — runs a 9B model in ~13 GB VRAM
- 🎨 **Styled terminal UI** — animated banner, typewriter output, token stats
- ⚙️ **Live parameter control** — adjust temperature and token limit mid-session
- 💾 **Conversation export** — save any session to a timestamped `.txt` file
- 🔄 **Auto-bootstrap** — upgrades `transformers` automatically if the architecture is missing

---

## Requirements

| Requirement | Version |
|---|---|
| Python | 3.10+ |
| CUDA (recommended) | 12.x |
| VRAM (GPU) | ≥ 13 GB (or CPU fallback) |

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/VERBAREX/LuminoLex-Learn.git
cd LuminoLex-Learn

# 2. Install dependencies
pip install torch transformers peft accelerate bitsandbytes rich packaging
```

> **First run note:** If your `transformers` version doesn't support Qwen3.5, the bootstrap script upgrades it automatically and restarts. In Colab, manually go to **Runtime → Restart session** after the upgrade, then re-run.

---

## Usage

```bash
python main.py
```

### Chat Commands

| Command | Description |
|---|---|
| `?` or `/help` | Show the help panel |
| `/learn <fact>` | Teach the model a fact about you — injected into every reply |
| `/learned` | Show all facts the model currently knows about you |
| `/forget` | Wipe the user profile for this session |
| `/clear` | Wipe the screen and reset the session |
| `/history` | Print full conversation history |
| `/tokens` | Show token usage stats for this session |
| `/system <prompt>` | Replace the system prompt on the fly |
| `/temp <0.1–2.0>` | Change temperature (default: `0.5`) |
| `/maxtok <int>` | Change max output tokens (default: `2048`) |
| `/save [filename]` | Save conversation to a text file |
| `/exit` or `/quit` | Exit the application |

---

## Project Structure

```
.
├── main.py          # Entry point — chat loop and command handling
├── model.py         # Model loading (4-bit) and inference with spinner
├── ui.py            # Rich terminal UI components and effects
├── utils.py         # Memory block builder, conversation save/load
├── config.py        # Colours, banners, model IDs, and system prompt
└── bootstrap.py     # Auto-upgrade transformers if architecture is missing
```

---

## Configuration

Key settings live in `config.py`:

| Variable | Default | Description |
|---|---|---|
| `BASE_MODEL` | `Qwen/Qwen3.5-9B` | Base model pulled from HuggingFace |
| `ADAPTER_REPO` | `VERBAREX/LuminoLexV1-9B` | LoRA adapter repo |
| `DEFAULT_SYSTEM` | *(see config.py)* | System prompt injected at the start of every session |

---

## Generation Defaults

| Parameter | Default |
|---|---|
| `max_new_tokens` | `2048` |
| `temperature` | `0.5` |
| `top_p` | `0.9` |
| `repetition_penalty` | `1.1` |

---

## Google Colab

1. Run the script — bootstrap installs the correct `transformers` version automatically.
2. When prompted, go to **Runtime → Restart session**.
3. Re-run the cell — the model loads normally on the second run.

---

## License

This project is released under the [MIT License](LICENSE).

---

## Credits

Built by **VERBAREX** · Model adapter: [VERBAREX/LuminoLexV1-9B](https://huggingface.co/VERBAREX/LuminoLexV1-9B)
