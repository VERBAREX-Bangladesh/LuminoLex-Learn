# LuminoLex Learn

A terminal chat interface for **LuminoLexV1-9B** by VERBAREX — loaded in 4-bit NF4 for fast GPU inference.

---

## Requirements

- Python 3.10+
- CUDA GPU recommended (T4 or better). CPU works but is slow.

---

## Installation

```bash
git clone https://github.com/VERBAREX-Bangladesh/LuminoLex-Learn
cd LuminoLex-Learn
pip install -r requirements.txt
```

> If required model dependencies are missing, the script upgrades them automatically on first run.

---

## Usage

```bash
python run.py
```

---

## Commands

| Command | Description |
|---|---|
| `/help  or  ?` | Show this help panel |
| `/clear` | Wipe the screen and reset session |
| `/history` | Print full conversation history |
| `/tokens` | Show token usage stats for this session |
| `/system <prompt>` | Replace the system prompt on-the-fly |
| `/temp <0.1-2.0>` | Change temperature (default: 0.8) |
| `/maxtok <int>` | Change max_new_tokens (default: 2048) |
| `/learn <fact>` | Teach the model something — persists all session |
| `/learned` | Show everything the model has learned |
| `/forget` | Wipe all learned facts |
| `/save [file]` | Save conversation to a text file |
| `/exit  or  /quit` | Exit LuminoLex |

---

## Project Structure

```
LuminoLex-Learn/
├── run.py                  # Entry point
├── requirements.txt
└── luminolex/
    ├── __init__.py
    ├── config.py           # Constants, defaults, colour palette
    ├── bootstrap.py        # Auto-upgrade dependencies if needed
    ├── model.py            # Model + tokenizer loading
    ├── inference.py        # Generation with spinner
    ├── ui.py               # All terminal rendering
    ├── session.py          # Session state + command handler
    └── main.py             # REPL loop
```

---

## Model

| Field | Value |
|---|---|
| Model | `LuminoLexV1-9B` |
| Developer | `VERBAREX` |
| Quantisation | 4-bit NF4 (bitsandbytes) |
| VRAM (T4) | ~6 GB |

---

## License

MIT
