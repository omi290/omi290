import os
import json
from .base_generator import BaseGenerator
from utils.svg_builder import create_svg
import config
from utils.xml_utils import xml_escape_text



class FastfetchGenerator(BaseGenerator):
    @property
    def filename(self) -> str:
        return "fastfetch"

    def fetch_data(self):
        profile_path = os.path.join(os.path.dirname(__file__), "..", "..", "profile.json")
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                self.profile = json.load(f)
        except Exception:
            self.profile = {}

    def render_svg(self) -> str:
        padding = config.PADDING if hasattr(config, "PADDING") else 24

        personal = self.profile.get("personal", {})
        education = self.profile.get("education", {})
        skills = self.profile.get("skills", {})
        achievements = self.profile.get("achievements", [])

        def join_list(v):
            if not v:
                return ""
            if isinstance(v, list):
                return " • ".join([str(x) for x in v if x is not None and str(x).strip() != ""])
            return str(v).strip()

        def first_or(v, fallback="N/A"):
            if isinstance(v, list) and v:
                return str(v[0])
            return fallback

        # Required Display (remove Host/Status completely)
        stats = [
            ("OS", personal.get("os", ""), "color-primary"),
            ("User", personal.get("user", ""), "color-primary"),
            ("Role", personal.get("role", ""), "color-primary"),
            ("Specialization", personal.get("specialization", ""), "color-primary"),
            ("Education", education.get("stream", education.get("degree", "")), "color-primary"),
            ("College", education.get("college", ""), "color-primary"),
            ("Languages", join_list(skills.get("languages")), "color-blue"),
            ("AI Stack", join_list(skills.get("ai_stack")), "color-blue"),
            (
                "Core Coursework",
                join_list(skills.get("core_cs") or skills.get("coursework")),
                "color-blue",
            ),
            ("Achievements", first_or(achievements, "N/A"), "color-success"),
        ]

        stats = [s for s in stats if str(s[1]).strip() != ""]
        if not stats:
            stats = [("OS", personal.get("os", "GitHub"), "color-primary")]

        content = '''
        <style>
            @keyframes t {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes b {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
            .r {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                opacity: 1;
                animation: t 0.15s linear forwards;
            }
            .c { animation: b 1s infinite; }
        </style>
        <g xml:space="preserve">
        '''

        prompt_y = padding + 14
        content += f'<text x="{padding}" y="{prompt_y}" class="r" style="animation-delay: 0s;">'
        content += '<tspan class="color-success">om@github</tspan><tspan class="color-primary">:</tspan><tspan class="color-blue">~$</tspan><tspan class="color-primary"> fastfetch</tspan>'
        content += '</text>\n'

        current_y = prompt_y + 42
        stagger_delay = 0.08
        start_delay = 0.2

        label_width = max(len(k) for k, v, c in stats) + 2

        for i, (key, value, color_class) in enumerate(stats):
            delay = start_delay + (i * stagger_delay)
            content += f'<text x="{padding}" y="{current_y}" class="r {color_class}" style="animation-delay: {delay}s;">'
            content += f'<tspan class="color-secondary">{xml_escape_text(key.ljust(label_width))}</tspan>{xml_escape_text(value)}'
            content += '</text>\n'
            current_y += 24

        total_rows = len(stats)
        cursor_delay = start_delay + (total_rows * stagger_delay) + 0.15
        current_y += 12
        content += f'<text x="{padding}" y="{current_y}" class="r c" style="animation-delay: {cursor_delay}s;">'
        content += '<tspan class="color-success">om@github</tspan><tspan class="color-primary">:</tspan><tspan class="color-blue">~$</tspan> <tspan class="color-primary">█</tspan>'
        content += '</text>\n</g>'

        card_height = current_y + padding
        return create_svg(820, int(card_height), content)

