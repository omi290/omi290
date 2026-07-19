from dataclasses import dataclass

@dataclass
class Theme:
    name: str
    background: str
    foreground: str
    primary: str
    success: str
    error: str
    font_main: str

# --------------------------
# Available Themes
# --------------------------

GITHUB_DARK = Theme(
    name="GitHubDark",
    background="#0d1117",
    foreground="#c9d1d9",
    primary="#58a6ff",
    success="#3fb950",
    error="#f85149",
    font_main="Courier New, monospace"
)

CLASSIC_TERMINAL = Theme(
    name="Classic Terminal",
    background="#000000",
    foreground="#00ff00",
    primary="#00ff00",
    success="#00ff00",
    error="#ff0000",
    font_main="Courier New, monospace"
)

CATPPUCCIN = Theme(
    name="Catppuccin",
    background="#1E1E2E",
    foreground="#CDD6F4",
    primary="#CBA6F7",
    success="#A6E3A1",
    error="#F38BA8",
    font_main="Courier New, monospace"
)

# Active Theme
ACTIVE_THEME = GITHUB_DARK
