#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║       LuminoLex Learn - Terminal Chat        ║
║             Powered by VERBAREX              ║
╚══════════════════════════════════════════════╝

Run:  python main.py
Deps: pip install torch transformers peft accelerate rich
"""

import sys
import time

import bootstrap
bootstrap.ensure_transformers()

import config
import ui
import utils
from model import load_model, generate_with_spinner
from rich.rule import Rule

def main():
    ui.console.clear()
    ui.animate_banner()
    ui.print_subtitle()
    ui.console.print(Rule(style=config.BRAND_DIM))
    ui.console.print(f"  [bold {config.TEXT_DIM}]Type [bold {config.GOLD}]?[/] or [bold {config.GOLD}]/help[/] for commands.  "
                     f"Type [bold {config.DANGER}]/exit[/] to quit.[/]")
    ui.console.print(Rule(style=config.BRAND_DIM))
    ui.console.print()

    try:
        model, tokenizer = load_model()
    except Exception as exc:
        ui.console.print(f"\n[bold {config.DANGER}]✖  Failed to load model:[/]\n  {exc}\n")
        sys.exit(1)

    ui.console.print(Rule(f"[bold {config.BRAND}] Chat Session Started [/]", style=config.BRAND_DIM))
    ui.console.print()

    system_prompt  = config.DEFAULT_SYSTEM
    learned_facts: list[str] = []
    params = {
        "max_new_tokens":    2048,
        "temperature":       0.8,
        "top_p":             0.9,
        "repetition_penalty":1.1,
    }
    history: list[dict] = []
    turn          = 0
    total_in_tok  = 0
    total_out_tok = 0

    while True:
        try:
            ui.console.print(f"[bold {config.GOLD}]┌─[You]─[/]")
            user_input = ui.console.input(f"[bold {config.GOLD}]└─▶ [/]").strip()
        except (EOFError, KeyboardInterrupt):
            ui.console.print(f"\n\n[bold {config.BRAND}]Goodbye! 👋[/]\n")
            break

        if not user_input:
            continue

        low = user_input.lower()

        if low in ("?", "/help"):
            ui.print_help()
            continue

        if low in ("/exit", "/quit", "exit", "quit"):
            ui.console.print(f"\n[bold {config.BRAND}]Session ended. Goodbye![/]\n")
            break

        if low == "/clear":
            history.clear()
            turn = 0
            ui.console.clear()
            ui.animate_banner()
            ui.print_subtitle()
            ui.console.print(f"  [{config.SUCCESS}]✔[/]  Session cleared.\n")
            continue

        if low == "/history":
            utils.show_history(history)
            continue

        if low == "/tokens":
            ui.console.print(
                f"\n  [{config.INFO}]Token stats —[/]  "
                f"In: [bold]{total_in_tok}[/]   Out: [bold]{total_out_tok}[/]   "
                f"Total: [bold]{total_in_tok + total_out_tok}[/]\n"
            )
            continue

        if low.startswith("/system "):
            system_prompt = user_input[8:].strip()
            history.clear()
            turn = 0
            ui.console.print(f"  [{config.SUCCESS}]✔[/]  System prompt updated. History reset.\n")
            continue

        if low.startswith("/temp "):
            try:
                val = float(user_input.split()[1])
                assert 0.0 < val <= 2.0
                params["temperature"] = val
                ui.console.print(f"  [{config.SUCCESS}]✔[/]  Temperature set to [bold]{val}[/]\n")
            except Exception:
                ui.console.print(f"  [{config.DANGER}]✖[/]  Usage: /temp <0.1–2.0>\n")
            continue

        if low.startswith("/maxtok "):
            try:
                val = int(user_input.split()[1])
                assert val > 0
                params["max_new_tokens"] = val
                ui.console.print(f"  [{config.SUCCESS}]✔[/]  max_new_tokens set to [bold]{val}[/]\n")
            except Exception:
                ui.console.print(f"  [{config.DANGER}]✖[/]  Usage: /maxtok <positive integer>\n")
            continue

        if low.startswith("/save"):
            parts = user_input.split(maxsplit=1)
            fname = parts[1] if len(parts) > 1 else None
            utils.save_conversation(history, fname)
            continue

        if low.startswith("/learn "):
            fact = user_input[7:].strip()
            if fact:
                learned_facts.append(fact)
                preview = fact[:80] + "…" if len(fact) > 80 else fact
                ui.console.print(
                    f"  [{config.SUCCESS}]✔[/]  Learned about you ([bold]{len(learned_facts)}[/] total): "
                    f"[{config.TEXT_DIM}]{preview}[/]\n"
                )
            else:
                ui.console.print(f"  [{config.DANGER}]✖[/]  Usage: /learn <any fact about you …>\n")
            continue

        if low == "/learned":
            if not learned_facts:
                ui.console.print(f"  [{config.TEXT_DIM}]Nothing learned yet. Use /learn <fact>[/]\n")
            else:
                ui.console.print(f"\n  [{config.BRAND}]Facts I know about you ({len(learned_facts)}):[/]")
                for i, f in enumerate(learned_facts, 1):
                    ui.console.print(f"  [{config.GOLD}]{i}.[/] {f}")
                ui.console.print()
            continue

        if low == "/forget":
            learned_facts.clear()
            ui.console.print(f"  [{config.SUCCESS}]✔[/]  All learned facts wiped.\n")
            continue

        # ── Normal message ───────────────────────────────────────────────────
        turn += 1
        ui.render_user_bubble(user_input, turn)
        history.append({"role": "user", "content": user_input})

        # Build effective system prompt
        if learned_facts:
            effective_system = system_prompt + utils.build_memory_block(learned_facts)
        else:
            effective_system = system_prompt

        messages = [{"role": "system", "content": effective_system}] + history

        ui.console.print(f"  [{config.BRAND_DIM}]…[/]")
        t0 = time.time()
        try:
            response, in_tok, out_tok = generate_with_spinner(model, tokenizer, messages, params)
        except Exception as exc:
            ui.console.print(f"\n[bold {config.DANGER}]✖  Inference error:[/] {exc}\n")
            history.pop()
            turn -= 1
            continue
        elapsed = time.time() - t0

        total_in_tok  += in_tok
        total_out_tok += out_tok

        ui.typewriter_effect(response, delay=0.005)
        ui.render_ai_bubble(response, turn, in_tok, out_tok, elapsed)

        history.append({"role": "assistant", "content": response})
        ui.console.print()

if __name__ == "__main__":
    main()
