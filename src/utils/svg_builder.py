from utils.theme import ACTIVE_THEME

def create_svg(width: int, height: int, content: str) -> str:
    """Wraps content in a standard SVG tag."""
    theme = ACTIVE_THEME
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>
        .terminal-text {{ font-family: {theme.font_main}; fill: {theme.foreground}; }}
        .terminal-bg {{ fill: {theme.background}; }}
    </style>
    <rect width="{width}" height="{height}" class="terminal-bg" rx="10"/>
    {content}
</svg>'''

