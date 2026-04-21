import sys
import time

from rich.console import Console
from rich.rule import Rule

from luminolex.config import (
    BRAND, BRAND_DIM, GOLD, TEXT_DIM,
    SUCCESS, DANGER, INFO, DEFAULT_PARAMS, DEFAULT_SYSTEM
)
from luminolex.ui import (
    animate_banner, print_subtitle, print_help,
    render_user_bubble, render_ai_bubble, typewriter_effect
)
from luminolex.model import load_model
from luminolex.inference import generate_with_spinner
from luminolex.session import build_memory_block, save_conversation, show_history

console = Console()


def main():
    console.clear()
    animate_banner()
    print_subtitle()
    console.print(Rule(style=BRAND_DIM))
    console.print(f"  [bold {TEXT_DIM}]Type [bold {GOLD}]?[/] or [bold {GOLD}]/help[/] for commands.  "
                  f"Type [bold {DANGER}]/exit[/] to quit.[/]")
    console.print(Rule(style=BRAND_DIM))
    console.print()

    try:
        model, tokenizer = load_model()
    except Exception as exc:
        console.print(f"\n[bold {DANGER}]✖  Failed to load model:[/]\n  {exc}\n")
        sys.exit(1)

    console.print(Rule(f"[bold {BRAND}] Chat Session Started [/]", style=BRAND_DIM))
    console.print()

    system_prompt  = DEFAULT_SYSTEM
    learned_facts  = []
    params         = dict(DEFAULT_PARAMS)
    history        = []
    turn           = 0
    total_in_tok   = 0
    total_out_tok  = 0

    while True:
        try:
            console.print(f"[bold {GOLD}]┌─[You]─[/]")
            user_input = console.input(f"[bold {GOLD}]└─▶ [/]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print(f"\n\n[bold {BRAND}]Goodbye! 👋[/]\n")
            break

        if not user_input:
            continue

        low = user_input.lower()

        if low in ("?", "/help"):
            print_help()
            continue

        if low in ("/exit", "/quit", "exit", "quit"):
            console.print(f"\n[bold {BRAND}]Session ended. Goodbye![/]\n")
            break

        if low == "/clear":
            history.clear()
            turn = 0
            console.clear()
            animate_banner()
            print_subtitle()
            console.print(f"  [{SUCCESS}]✔[/]  Session cleared.\n")
            continue

        if low == "/history":
            show_history(history)
            continue

        if low == "/tokens":
            console.print(
                f"\n  [{INFO}]Token stats —[/]  "
                f"In: [bold]{total_in_tok}[/]   Out: [bold]{total_out_tok}[/]   "
                f"Total: [bold]{total_in_tok + total_out_tok}[/]\n"
            )
            continue

        if low.startswith("/system "):
            system_prompt = user_input[8:].strip()
            history.clear()
            turn = 0
            console.print(f"  [{SUCCESS}]✔[/]  System prompt updated. History reset.\n")
            continue

        if low.startswith("/temp "):
            try:
                val = float(user_input.split()[1])
                assert 0.0 < val <= 2.0
                params["temperature"] = val
                console.print(f"  [{SUCCESS}]✔[/]  Temperature set to [bold]{val}[/]\n")
            except Exception:
                console.print(f"  [{DANGER}]✖[/]  Usage: /temp <0.1–2.0>\n")
            continue

        if low.startswith("/maxtok "):
            try:
                val = int(user_input.split()[1])
                assert val > 0
                params["max_new_tokens"] = val
                console.print(f"  [{SUCCESS}]✔[/]  max_new_tokens set to [bold]{val}[/]\n")
            except Exception:
                console.print(f"  [{DANGER}]✖[/]  Usage: /maxtok <positive integer>\n")
            continue

        if low.startswith("/save"):
            parts = user_input.split(maxsplit=1)
            fname = parts[1] if len(parts) > 1 else None
            save_conversation(history, fname)
            continue

        if low.startswith("/learn "):
            fact = user_input[7:].strip()
            if fact:
                learned_facts.append(fact)
                preview = fact[:80] + "…" if len(fact) > 80 else fact
                console.print(
                    f"  [{SUCCESS}]✔[/]  Learned about you ([bold]{len(learned_facts)}[/] total): "
                    f"[{TEXT_DIM}]{preview}[/]\n"
                )
            else:
                console.print(f"  [{DANGER}]✖[/]  Usage: /learn <any fact about you …>\n")
            continue

        if low == "/learned":
            if not learned_facts:
                console.print(f"  [{TEXT_DIM}]Nothing learned yet. Use /learn <fact>[/]\n")
            else:
                console.print(f"\n  [{BRAND}]Facts I know about you ({len(learned_facts)}):[/]")
                for i, f in enumerate(learned_facts, 1):
                    console.print(f"  [{GOLD}]{i}.[/] {f}")
                console.print()
            continue

        if low == "/forget":
            learned_facts.clear()
            console.print(f"  [{SUCCESS}]✔[/]  All learned facts wiped.\n")
            continue

        # ── Normal message ───────────────────────────────────────────────────
        turn += 1
        render_user_bubble(user_input, turn)
        history.append({"role": "user", "content": user_input})

        if learned_facts:
            effective_system = system_prompt + build_memory_block(learned_facts)
        else:
            effective_system = system_prompt

        messages = [{"role": "system", "content": effective_system}] + history

        console.print(f"  [{BRAND_DIM}]…[/]")
        t0 = time.time()
        try:
            response, in_tok, out_tok = generate_with_spinner(model, tokenizer, messages, params)
        except Exception as exc:
            console.print(f"\n[bold {DANGER}]✖  Inference error:[/] {exc}\n")
            history.pop()
            turn -= 1
            continue
        elapsed = time.time() - t0

        total_in_tok  += in_tok
        total_out_tok += out_tok

        typewriter_effect(response, delay=0.005)
        render_ai_bubble(response, turn, in_tok, out_tok, elapsed)

        history.append({"role": "assistant", "content": response})
        console.print()
