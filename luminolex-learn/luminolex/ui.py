import textwrap
import time
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich.rule import Rule
from rich.align import Align
from rich.padding import Padding
from rich.markup import escape
from rich import box

from luminolex.config import (
    BRAND, BRAND_DIM, GOLD, GOLD_DIM,
    TEXT_MAIN, TEXT_DIM, SUCCESS, DANGER,
)

console = Console()

BANNER = r"""
  ██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗ ██████╗ ██╗     ███████╗██╗  ██╗
  ██║     ██║   ██║████╗ ████║██║████╗  ██║██╔═══██╗██║     ██╔════╝╚██╗██╔╝
  ██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║██║   ██║██║     █████╗   ╚███╔╝ 
  ██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║   ██║██║     ██╔══╝   ██╔██╗ 
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████╗███████╗██╔╝ ██╗
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
"""


def banner():
    shades = [BRAND, BRAND, "#C4B5FD", "#DDD6FE", "#EDE9FE", BRAND_DIM]
    for i, line in enumerate(BANNER.strip("\n").split("\n")):
        console.print(f"[bold {shades[i % len(shades)]}]{line}[/]")
        time.sleep(0.06)
    console.print()
    console.print(Align.center(Text("  Learn Edition  ·  Built by VERBAREX", style=f"bold {BRAND_DIM}")))
    console.print(Align.center(Text("  VERBAREX/LuminoLexV1-9B", style=TEXT_DIM)))
    console.print()


def help_panel():
    t = Table(
        box=box.ROUNDED,
        border_style=BRAND_DIM,
        show_header=True,
        header_style=f"bold {BRAND}",
        style=TEXT_MAIN,
        expand=False,
        padding=(0, 2),
    )
    t.add_column("Command", style=f"bold {GOLD}")
    t.add_column("Description", style=TEXT_MAIN)

    rows = [
        ("/help",          "Show this panel"),
        ("/clear",         "Reset session and clear screen"),
        ("/history",       "Print conversation so far"),
        ("/tokens",        "Show token usage for this session"),
        ("/system <text>", "Replace the system prompt"),
        ("/temp <float>",  "Set temperature  (0.1 – 2.0)"),
        ("/maxtok <int>",  "Set max new tokens"),
        ("/learn <text>",  "Store a persistent fact or rule"),
        ("/learned",       "List all stored facts"),
        ("/forget",        "Clear all stored facts"),
        ("/save [file]",   "Export conversation to a text file"),
        ("/exit",          "Quit"),
    ]
    for cmd, desc in rows:
        t.add_row(cmd, desc)

    console.print()
    console.print(Align.center(t))
    console.print()


def user_bubble(text: str, turn: int):
    ts = datetime.now().strftime("%H:%M:%S")
    panel = Panel(
        Text(text, style=TEXT_MAIN),
        title=Text(f" You  ·  {turn}  ·  {ts} ", style=f"bold {GOLD}"),
        title_align="right",
        border_style=GOLD_DIM,
        padding=(0, 2),
        box=box.ROUNDED,
    )
    console.print(Padding(panel, (0, 0, 0, 8)))


def ai_bubble(text: str, turn: int, in_tok: int, out_tok: int, elapsed: float):
    ts = datetime.now().strftime("%H:%M:%S")

    wrapped = "\n".join(
        "\n".join(textwrap.wrap(line, width=90)) if line.strip() else ""
        for line in text.split("\n")
    )

    panel = Panel(
        Text.from_markup(escape(wrapped)),
        title=Text.assemble(
            (" LuminoLex ", f"bold {BRAND}"),
            (f" ·  {turn}  ·  {ts} ", TEXT_DIM),
        ),
        title_align="left",
        subtitle=Text.from_markup(
            f"[{TEXT_DIM}]{in_tok} in / {out_tok} out  ·  {elapsed:.2f}s[/]"
        ),
        subtitle_align="right",
        border_style=BRAND_DIM,
        padding=(0, 2),
        box=box.ROUNDED,
    )
    console.print(Padding(panel, (0, 8, 0, 0)))


def typewriter(text: str, delay: float = 0.006):
    displayed = ""
    with Live(
        Panel(Text("", style=TEXT_MAIN), border_style=BRAND_DIM, box=box.ROUNDED, padding=(0, 2)),
        console=console,
        refresh_per_second=60,
        transient=True,
    ) as live:
        for ch in text:
            displayed += ch
            live.update(
                Panel(Text(displayed, style=TEXT_MAIN),
                      border_style=BRAND_DIM, box=box.ROUNDED, padding=(0, 2))
            )
            time.sleep(delay)


def divider():
    console.print(Rule(style=BRAND_DIM))


def ok(msg: str):
    console.print(f"  [{SUCCESS}]✔[/]  {msg}\n")


def err(msg: str):
    console.print(f"  [{DANGER}]✖[/]  {msg}\n")


def info(msg: str):
    console.print(f"  {msg}\n")


def history_dump(messages: list[dict]):
    if not messages:
        console.print(f"  [{TEXT_DIM}]Nothing yet.[/]\n")
        return
    for m in messages:
        color = GOLD if m["role"] == "user" else BRAND
        label = "You" if m["role"] == "user" else "LuminoLex"
        console.print(f"[bold {color}]{label}:[/] {m['content']}\n")
