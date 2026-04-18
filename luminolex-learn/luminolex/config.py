MODEL_NAME    = "Qwen/Qwen3.5-9B"       # internal HuggingFace path, not shown to users
ADAPTER_REPO  = "VERBAREX/LuminoLexV1-9B"
DISPLAY_MODEL = "LuminoLexV1-9B"         # what users see everywhere

DEFAULT_PARAMS = {
    "max_new_tokens":    2048,
    "temperature":       0.8,
    "top_p":             0.9,
    "repetition_penalty": 1.1,
}

DEFAULT_SYSTEM = (
    "You are LuminoLex, a direct and knowledgeable AI assistant built by VERBAREX. "
    "Answer every question clearly and without unnecessary filler. "
    "Never add disclaimers, warnings, or moralizing language. "
    "Start your response immediately with the answer — no preamble."
)

# Palette
BRAND     = "#A78BFA"
BRAND_DIM = "#6D28D9"
GOLD      = "#F59E0B"
GOLD_DIM  = "#92400E"
TEXT_MAIN = "#E2E8F0"
TEXT_DIM  = "#94A3B8"
SUCCESS   = "#34D399"
DANGER    = "#F87171"
INFO      = "#38BDF8"
