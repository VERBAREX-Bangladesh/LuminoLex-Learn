# LuminoLex Learn

A terminal chat interface for **LuminoLexV1-9B** by VERBAREX — loaded in 4-bit NF4 for fast GPU inference.

---

## Requirements

- Python 3.10+
- CUDA GPU recommended (T4 or better). CPU works but is slow.

---

## Installation

```bash
git clone https://github.com/VERBAREX/luminolex-learn
cd luminolex-learn
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
| `/help` | Show command list |
| `/clear` | Reset session |
| `/history` | Print conversation |
| `/tokens` | Show token usage |
| `/system <text>` | Replace system prompt |
| `/temp <float>` | Set temperature (0.1 – 2.0) |
| `/maxtok <int>` | Set max new tokens |
| `/learn <text>` | Store a persistent fact or rule |
| `/learned` | List stored facts |
| `/forget` | Clear stored facts |
| `/save [file]` | Export conversation to file |
| `/exit` | Quit |

---

## Project Structure

```
luminolex-learn/
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
