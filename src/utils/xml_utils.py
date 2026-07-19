from __future__ import annotations

import html


def xml_escape_text(value) -> str:
    """Escape text for safe embedding inside SVG/HTML text nodes.

    Requirements:
    - Convert &, <, >, ", ' to XML entities
    """
    if value is None:
        return ""
    # html.escape escapes &, <, > by default; quote=True escapes "
    # Then we map ' to &apos; for XML compatibility.
    s = str(value)
    s = html.escape(s, quote=True)
    return s.replace("'", "&apos;")

