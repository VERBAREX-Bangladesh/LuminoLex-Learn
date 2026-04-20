import sys
import time

from rich.console import Console
from rich.rule import Rule

from luminolex.bootstrap import ensure_dependencies
from luminolex.session import Session, handle_command
from luminolex.config import BRAND, BRAND_DIM, GOLD, DANGER, TEXT_DIM
from luminolex import ui, inference

console = Console()


def run():
    ensure_dependencies()

    from luminolex import model as model_loader

    console.clear()
    ui.banner()
    console.print(Rule(style=BRAND_DIM))
    console.print(
        f"  [bold {TEXT_DIM}]Type [bold {GOLD}]?[/] or [bold {GOLD}]/help[/] for commands.  "
        f"Type [bold {DANGER}]/exit[/] to quit.[/]"
    )
    console.print(Rule(style=BRAND_DIM))
    console.print()

    try:
        llm, tokenizer = model_loader.load()
    except Exception as exc:
        console.print(f"\n[bold {DANGER}]✖  Failed to load model:[/]\n  {exc}\n")
        sys.exit(1)

    console.print(Rule(f"[bold {BRAND}] Chat Session Started [/]", style=BRAND_DIM))
    console.print()

    session = Session()

    while True:
        try:
            console.print(f"[bold {GOLD}]┌─[You]─[/]")
            user_input = console.input(f"[bold {GOLD}]└─▶ [/]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print(f"\n\n[bold {BRAND}]Goodbye! 👋[/]\n")
            break

        if not user_input:
            continue

        try:
            if handle_command(user_input, session):
                continue
        except SystemExit:
            console.print(f"\n[bold {BRAND}]Session ended. Goodbye![/]\n")
            break

        session.turn += 1
        ui.user_bubble(user_input, session.turn)
        session.history.append({"role": "user", "content": user_input})

        messages = session.build_messages()

        console.print(f"  [{BRAND_DIM}]…[/]")
        t0 = time.time()
        try:
            response, in_tok, out_tok = inference.run(llm, tokenizer, messages, session.params)
        except Exception as exc:
            console.print(f"\n[bold {DANGER}]✖  Inference error:[/] {exc}\n")
            session.history.pop()
            session.turn -= 1
            continue

        elapsed = time.time() - t0
        session.total_in  += in_tok
        session.total_out += out_tok

        ui.typewriter(response)
        ui.ai_bubble(response, session.turn, in_tok, out_tok, elapsed)

        session.history.append({"role": "assistant", "content": response})
        console.print()
