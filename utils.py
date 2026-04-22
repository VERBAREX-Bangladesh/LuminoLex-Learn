from datetime import datetime
import config
from ui import console

def save_conversation(history, filename=None):
    if not filename:
        filename = f"luminolex_learn_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("═" * 60 + "\n")
        f.write("  LuminoLex Learn — Conversation Export\n")
        f.write(f"  Saved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("═" * 60 + "\n\n")
        for msg in history:
            role = "You" if msg["role"] == "user" else "LuminoLex Learn"
            f.write(f"[{role}]\n{msg['content']}\n\n{'─'*40}\n\n")
    console.print(f"  [{config.SUCCESS}]✔[/]  Saved to [bold {config.INFO}]{filename}[/]\n")

def show_history(history):
    if not history:
        console.print(f"  [{config.TEXT_DIM}]No conversation history yet.[/]\n")
        return
    for msg in history:
        role  = msg["role"]
        color = config.GOLD if role == "user" else config.BRAND
        label = "You" if role == "user" else "LuminoLex Learn"
        console.print(f"[bold {color}]{label}:[/] {msg['content']}\n")

def build_memory_block(learned_facts: list[str]) -> str:
    """
    Frame learned facts explicitly as facts *about the user*, not about the
    model itself.
    """
    facts_text = "\n".join(f"{i+1}. {f}" for i, f in enumerate(learned_facts))
    return (
        "\n\n"
        "##########  KNOWN FACTS ABOUT THE USER  ##########\n"
        "The following facts describe the person you are talking to (the USER).\n"
        "These are NOT facts about you (the AI). They are personal details about the human user.\n"
        "CRITICAL: Use these facts naturally and seamlessly in conversation when relevant. "
        "NEVER say things like:\n"
        "- 'Based on my records...'\n"
        "- 'According to the facts...'\n"
        "- 'I see here that...'\n"
        "- 'You mentioned earlier...'\n"
        "Simply state the answer as if you natively and naturally remember the user. Treat this as organic memory.\n"
        "Do NOT claim any of these facts as your own identity.\n\n"
        + facts_text +
        "\n\n##########  END OF USER FACTS  ##########"
    )
