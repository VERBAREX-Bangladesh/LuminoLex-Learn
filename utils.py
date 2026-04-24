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
    Feeds memory to the model while strictly forbidding it from narrating
    the memory process or adopting the facts as its own identity.
    """
    facts_text = "\n".join(f"- Fact about the human user: {f}" for f in learned_facts)
    
    return (
        "\n\n"
        "##########  USER MEMORY  ##########\n"
        "The following facts are known about the human user you are speaking to.\n"
        "CRITICAL RULES FOR USING THIS MEMORY:\n"
        "1. NEVER adopt these facts as your own identity.\n"
        "2. NEVER say phrases like 'According to your explicit statement', 'Based on my memory', 'My records show', or 'You mentioned'.\n"
        "3. Use this knowledge completely naturally, as if you organically remember the person you are conversing with.\n\n"
        + facts_text +
        "\n\n##########  END OF USER MEMORY  ##########"
    )
