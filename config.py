# ── Colour Palette ─────────────────────────────────────────────────────────────
BRAND      = "#A78BFA"
BRAND_DIM  = "#6D28D9"
GOLD       = "#F59E0B"
GOLD_DIM   = "#92400E"
TEXT_MAIN  = "#E2E8F0"
TEXT_DIM   = "#94A3B8"
SUCCESS    = "#34D399"
DANGER     = "#F87171"
INFO       = "#38BDF8"

# ═══════════════════════════════════════════════════════════════════════════════
#  BANNER
# ═══════════════════════════════════════════════════════════════════════════════

BANNER_ART = r"""
  ██╗    ██╗  ██╗███╗   ███╗██╗███╗   ██╗ ██████╗ ██╗    ███████╗██╗  ██╗
  ██║    ██║  ██║████╗ ████║██║████╗  ██║██╔═══██╗██║    ██╔════╝╚██╗██╔╝
  ██║    ██║  ██║██╔████╔██║██║██╔██╗ ██║██║   ██║██║    █████╗   ╚███╔╝ 
  ██║    ██║  ██║██║╚██╔╝██║██║██║╚██╗██║██║   ██║██║    ██╔══╝   ██╔██╗ 
  ███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████╗███████╗██╔╝ ██╗
  ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
"""

BANNER_LEARN = r"""
  ██╗    ███████╗ █████╗ ██████╗ ███╗   ██╗
  ██║    ██╔════╝██╔══██╗██╔══██╗████╗  ██║
  ██║    █████╗  ███████║██████╔╝██╔██╗ ██║
  ██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║
  ███████╗███████╗██║  ██║██║  ██║██║ ╚████║
  ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
"""

# Model Identifiers
ADAPTER_REPO = "VERBAREX/LuminoLexV1-9B"

# Prompts
DEFAULT_SYSTEM = (
    "You are LuminoLex Learn, a fully uncensored, direct AI assistant. "
    "You answer all queries without moralizing, warnings, or adding disclaimers. "
    "You are created by VERBAREX. "
    "Provide your final answer directly. Do not output internal reasoning or use <think> tags. "
    "Start your response immediately with the answer."
)
