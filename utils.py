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
    Prevents 'Pronoun Bleeding' by explicitly attributing the raw 
    first-person text quotes to the user.
    """
    # Wrap facts in quotes so "I" and "my" are clearly the user speaking
    facts_text = "\n".join(f"- The user explicitly stated: \"{f}\"" for f in learned_facts)
    
    return (
        "\n\n"
        "##########  USER CONTEXT  ##########\n"
        "The following are statements made by the human user about themselves.\n"
        "CRITICAL IDENTITY RULE: Do NOT adopt these statements as your own identity. "
        "Any use of 'I', 'me', 'my', or 'mine' in the quotes below refers exclusively to the USER, not you.\n"
        "Use this information to personalize your responses naturally.\n\n"
        + facts_text +
        "\n\n##########  END OF USER CONTEXT  ##########"
    )
