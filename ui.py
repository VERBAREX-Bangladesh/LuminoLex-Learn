import time
import textwrap
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table
from rich.rule import Rule
from rich.align import Align
from rich import box
from rich.padding import Padding
from rich.markup import escape

from luminolex.config import (
    BRAND, BRAND_DIM, GOLD, GOLD_DIM,
    TEXT_MAIN, TEXT_DIM, SUCCESS, DANGER, INFO
)

console = Console()

BANNER_ART = r"""
  ██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗ ██████╗ ██╗     ███████╗██╗  ██╗
  ██║     ██║   ██║████╗ ████║██║████╗  ██║██╔═══██╗██║     ██╔════╝╚██╗██╔╝
  ██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║██║   ██║██║     █████╗   ╚███╔╝ 
  ██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║   ██║██║     ██╔══╝   ██╔██╗ 
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████╗███████╗██╔╝ ██╗
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
"""

BANNER_LEARN = r"""
  ██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗
  ██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║
  ██║     █████╗  ███████║██████╔╝██╔██╗ ██║
  ██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║
  ███████╗███████╗██║  ██║██║  ██║██║ ╚████║
  ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
"""


def animate_banner():
    lines = BANNER_ART.strip("\n").split("\n")
    learn_lines = BANNER_LEARN.strip("\n").split("\n")
    colours = [BRAND, BRAND, "#C4B5FD", "#DDD6FE", "#EDE9FE", BRAND_DIM]
    for i, line in enumerate(lines):
        colour = colours[i % len(colours)]
        console.print(f"[bold {colour}]{line}[/]")
        time.sleep(0.06)
    console.print()
    for i, line in enumerate(learn_lines):
        colour = colours[i % len(colours)]
        console.print(f"[bold {colour}]{line}[/]")
        time.sleep(0.04)
    console.print()


def print_subtitle():
    subtitle = Text("  LuminoLex Learn  ·  Uncensored · Fast  ·  Built by VERBAREX", style=f"bold {BRAND_DIM}")
    version  = Text("  Model: VERBAREX/LuminoLexV1-9B  ·  Edition: Learn", style=f"{TEXT_DIM}")
    console.print(Align.center(subtitle))
    console.print(Align.center(version))
    console.print()


def print_help():
    t = Table(box=box.ROUNDED, border_style=BRAND_DIM, show_header=True,
              header_style=f"bold {BRAND}", style=TEXT_MAIN, expand=False, padding=(0, 2))
    t.add_column("Command",    style=f"bold {GOLD}")
    t.add_column("Action",     style=TEXT_MAIN)
    cmds = [
        ("/help  or  ?",        "Show this help panel"),
        ("/clear",              "Wipe the screen and reset session"),
        ("/history",            "Print full conversation history"),
        ("/tokens",             "Show token usage stats for this session"),
        ("/system  <prompt>",   "Replace the system prompt on-the-fly"),
        ("/temp   <0.1-2.0>",   "Change temperature (current default: 0.8)"),
        ("/maxtok <int>",       "Change max_new_tokens (default: 2048)"),
        ("/learn  <fact>",      "Teach the model a fact about you — persists all session"),
        ("/learned",            "Show everything the model has learned about you"),
        ("/forget",             "Wipe all learned facts"),
        ("/save   [file]",      "Save conversation to a text file"),
        ("/exit  or  /quit",    "Exit LuminoLex Learn"),
    ]
    for cmd, desc in cmds:
        t.add_row(cmd, desc)
    console.print()
    console.print(Align.center(t))
    console.print()


class LoadingStep:
    def __init__(self, label: str):
        self.label = label

    def __enter__(self):
        self._live = Live(
            Spinner("dots2", text=f"[{BRAND}] {self.label}[/]", style=f"bold {BRAND}"),
            console=console, refresh_per_second=20, transient=True
        )
        self._live.__enter__()
        return self

    def __exit__(self, *args):
        self._live.__exit__(*args)
        console.print(f"  [{SUCCESS}]✔[/]  [bold {TEXT_MAIN}]{self.label}[/]")


def render_user_bubble(text: str, turn: int):
    ts = datetime.now().strftime("%H:%M:%S")
    header = Text(f" You  ·  turn {turn}  ·  {ts} ", style=f"bold {GOLD}")
    body   = Text(text, style=TEXT_MAIN)
    panel  = Panel(
        body,
        title=header,
        title_align="right",
        border_style=GOLD_DIM,
        padding=(0, 2),
        box=box.ROUNDED,
    )
    console.print(Padding(panel, (0, 0, 0, 8)))


def render_ai_bubble(text: str, turn: int, in_tok: int, out_tok: int, elapsed: float):
    ts = datetime.now().strftime("%H:%M:%S")
    stats = f"[{TEXT_DIM}]{in_tok}in / {out_tok}out tok  ·  {elapsed:.2f}s[/]"
    header = Text.assemble(
        (" LuminoLex Learn ", f"bold {BRAND}"),
        (f" ·  turn {turn}  ·  {ts} ", TEXT_DIM),
    )

    wrapped = "\n".join(
        "\n".join(textwrap.wrap(line, width=90)) if line.strip() else ""
        for line in text.split("\n")
    )

    footer = Text.from_markup(stats)
    panel = Panel(
        Text.from_markup(escape(wrapped)),
        title=header,
        title_align="left",
        subtitle=footer,
        subtitle_align="right",
        border_style=BRAND_DIM,
        padding=(0, 2),
        box=box.ROUNDED,
    )
    console.print(Padding(panel, (0, 8, 0, 0)))


def typewriter_effect(text: str, delay: float = 0.008):
    displayed = ""
    with Live(
        Panel(Text("", style=TEXT_MAIN), border_style=BRAND_DIM,
              box=box.ROUNDED, padding=(0, 2)),
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
