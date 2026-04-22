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

import config

console = Console()

def animate_banner():
    lines = config.BANNER_ART.strip("\n").split("\n")
    learn_lines = config.BANNER_LEARN.strip("\n").split("\n")
    colours = [config.BRAND, config.BRAND, "#C4B5FD", "#DDD6FE", "#EDE9FE", config.BRAND_DIM]
    
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
    subtitle = Text("  LuminoLex Learn  ·  Uncensored · Fast  ·  Built by VERBAREX", style=f"bold {config.BRAND_DIM}")
    version  = Text("  Model: VERBAREX/LuminoLexV1-9B  ·  Edition: Learn", style=f"{config.TEXT_DIM}")
    console.print(Align.center(subtitle))
    console.print(Align.center(version))
    console.print()

def print_help():
    t = Table(box=box.ROUNDED, border_style=config.BRAND_DIM, show_header=True,
              header_style=f"bold {config.BRAND}", style=config.TEXT_MAIN, expand=False, padding=(0, 2))
    t.add_column("Command",    style=f"bold {config.GOLD}")
    t.add_column("Action",     style=config.TEXT_MAIN)
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
            Spinner("dots2", text=f"[{config.BRAND}] {self.label}[/]", style=f"bold {config.BRAND}"),
            console=console, refresh_per_second=20, transient=True
        )
        self._live.__enter__()
        return self

    def __exit__(self, *args):
        self._live.__exit__(*args)
        console.print(f"  [{config.SUCCESS}]✔[/]  [bold {config.TEXT_MAIN}]{self.label}[/]")

def render_user_bubble(text: str, turn: int):
    ts = datetime.now().strftime("%H:%M:%S")
    header = Text(f" You  ·  turn {turn}  ·  {ts} ", style=f"bold {config.GOLD}")
    body   = Text(text, style=config.TEXT_MAIN)
    panel  = Panel(
        body,
        title=header,
        title_align="right",
        border_style=config.GOLD_DIM,
        padding=(0, 2),
        box=box.ROUNDED,
    )
    console.print(Padding(panel, (0, 0, 0, 8)))

def render_ai_bubble(text: str, turn: int, in_tok: int, out_tok: int, elapsed: float):
    ts = datetime.now().strftime("%H:%M:%S")
    stats = f"[{config.TEXT_DIM}]{in_tok}in / {out_tok}out tok  ·  {elapsed:.2f}s[/]"
    header = Text.assemble(
        (" LuminoLex Learn ", f"bold {config.BRAND}"),
        (f" ·  turn {turn}  ·  {ts} ", config.TEXT_DIM),
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
        border_style=config.BRAND_DIM,
        padding=(0, 2),
        box=box.ROUNDED,
    )
    console.print(Padding(panel, (0, 8, 0, 0)))

def typewriter_effect(text: str, delay: float = 0.008):
    displayed = ""
    with Live(
        Panel(Text("", style=config.TEXT_MAIN), border_style=config.BRAND_DIM,
              box=box.ROUNDED, padding=(0, 2)),
        console=console,
        refresh_per_second=60,
        transient=True,
    ) as live:
        for ch in text:
            displayed += ch
            live.update(
                Panel(Text(displayed, style=config.TEXT_MAIN),
                      border_style=config.BRAND_DIM, box=box.ROUNDED, padding=(0, 2))
            )
            time.sleep(delay)
