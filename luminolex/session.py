from datetime import datetime
from dataclasses import dataclass, field

from luminolex.config import DEFAULT_PARAMS, DEFAULT_SYSTEM
from luminolex import ui


@dataclass
class Session:
    system_prompt: str = DEFAULT_SYSTEM
    params: dict       = field(default_factory=lambda: dict(DEFAULT_PARAMS))
    history: list      = field(default_factory=list)
    learned: list      = field(default_factory=list)
    turn: int          = 0
    total_in: int      = 0
    total_out: int     = 0

    def reset(self):
        self.history.clear()
        self.turn = 0

    def build_messages(self) -> list[dict]:
        system = self.system_prompt
        if self.learned:
            facts = "\n".join(f"{i + 1}. {f}" for i, f in enumerate(self.learned))
            system += (
                "\n\n--- Stored Facts (treat as ground truth) ---\n"
                + facts
                + "\n--- End ---"
            )
        return [{"role": "system", "content": system}] + self.history


def save_conversation(history: list[dict], filename: str | None = None):
    if not filename:
        filename = f"luminolex_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("═" * 60 + "\n")
        f.write("LuminoLex Learn — Conversation Export\n")
        f.write(f"Saved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("═" * 60 + "\n\n")
        for m in history:
            label = "You" if m["role"] == "user" else "LuminoLex"
            f.write(f"[{label}]\n{m['content']}\n\n" + "─" * 40 + "\n\n")
    ui.ok(f"Saved → {filename}")


def handle_command(raw: str, session: Session) -> bool:
    """
    Process a slash command. Returns True if the input was a command,
    False if it should be treated as a regular chat message.
    """
    cmd = raw.strip()
    low = cmd.lower()

    if low in ("?", "/help"):
        ui.help_panel()
        return True

    if low in ("/exit", "/quit", "exit", "quit"):
        raise SystemExit(0)

    if low == "/clear":
        session.reset()
        import os
        os.system("clear")
        ui.banner()
        ui.ok("Session cleared.")
        return True

    if low == "/history":
        ui.history_dump(session.history)
        return True

    if low == "/tokens":
        t = session.total_in + session.total_out
        ui.info(
            f"Tokens — in: [bold]{session.total_in}[/]  "
            f"out: [bold]{session.total_out}[/]  "
            f"total: [bold]{t}[/]"
        )
        return True

    if low.startswith("/system "):
        session.system_prompt = cmd[8:].strip()
        session.reset()
        ui.ok("System prompt updated. History cleared.")
        return True

    if low.startswith("/temp "):
        try:
            val = float(cmd.split()[1])
            assert 0.0 < val <= 2.0
            session.params["temperature"] = val
            ui.ok(f"Temperature → {val}")
        except Exception:
            ui.err("Usage: /temp <0.1 – 2.0>")
        return True

    if low.startswith("/maxtok "):
        try:
            val = int(cmd.split()[1])
            assert val > 0
            session.params["max_new_tokens"] = val
            ui.ok(f"max_new_tokens → {val}")
        except Exception:
            ui.err("Usage: /maxtok <positive integer>")
        return True

    if low.startswith("/save"):
        parts = cmd.split(maxsplit=1)
        save_conversation(session.history, parts[1] if len(parts) > 1 else None)
        return True

    if low.startswith("/learn "):
        fact = cmd[7:].strip()
        if fact:
            session.learned.append(fact)
            preview = fact[:80] + ("…" if len(fact) > 80 else "")
            ui.ok(f"Stored ({len(session.learned)} total): {preview}")
        else:
            ui.err("Usage: /learn <text>")
        return True

    if low == "/learned":
        if not session.learned:
            ui.info("Nothing stored yet. Use /learn <text>")
        else:
            for i, f in enumerate(session.learned, 1):
                ui.info(f"  {i}. {f}")
        return True

    if low == "/forget":
        session.learned.clear()
        ui.ok("All stored facts cleared.")
        return True

    return False
