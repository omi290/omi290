from utils.theme import ACTIVE_THEME

def create_svg(width: int, height: int, content: str) -> str:
    """Wraps content in a standard SVG tag with terminal chrome."""
    theme = ACTIVE_THEME
    
    # Terminal Chrome settings
    header_height = 32
    radius = 8
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>
        .terminal-text {{ font-family: {theme.font_main}; font-size: 14px; fill: {theme.foreground}; }}
        .terminal-text-bold {{ font-family: {theme.font_main}; font-size: 14px; font-weight: 700; fill: {theme.foreground}; }}
        .terminal-bg {{ fill: {theme.background}; stroke: #30363d; stroke-width: 1px; }}
        .terminal-header {{ fill: #161b22; }}
        
        /* Color classes */
        .color-primary {{ fill: {theme.primary}; }}
        .color-success {{ fill: {theme.success}; }}
        .color-error {{ fill: {theme.error}; }}
        .color-warning {{ fill: #d29922; }}
        .color-secondary {{ fill: #8b949e; }}
        .color-purple {{ fill: #bc8cff; }}
    </style>
    
    <!-- Window Background with Border -->
    <rect width="{width-1}" height="{height-1}" x="0.5" y="0.5" class="terminal-bg" rx="{radius}"/>
    
    <!-- Header -->
    <path class="terminal-header" d="M 0.5 {radius} Q 0.5 0.5 {radius} 0.5 L {width - radius - 0.5} 0.5 Q {width - 0.5} 0.5 {width - 0.5} {radius} L {width - 0.5} {header_height} L 0.5 {header_height} Z" />
    <line x1="0.5" y1="{header_height}" x2="{width-0.5}" y2="{header_height}" stroke="#30363d" stroke-width="1" />
    
    <!-- Window Controls -->
    <circle cx="20" cy="16" r="6" fill="#f85149" />
    <circle cx="40" cy="16" r="6" fill="#d29922" />
    <circle cx="60" cy="16" r="6" fill="#3fb950" />
    
    <!-- Inner Content -->
    <g transform="translate(0, {header_height})">
        {content}
    </g>
</svg>'''
