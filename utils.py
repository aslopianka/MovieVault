"""Utility helpers for terminal output formatting."""


def color_text(text, color_code):
    """Wrap text in ANSI color codes for terminal display."""
    colors = {
        "ERROR": 31,
        "SUCCESS": 32,
        "MENU": 34,
        "INPUT": 35
    }
    code = colors.get(color_code, "MENU")
    return f"\033[{code}m{text}\033[0m"