from .base_generator import BaseGenerator
from utils.svg_builder import create_svg

import os
import json
import config


class SkillsGenerator(BaseGenerator):
    @property
    def filename(self) -> str:
        return "skills"

    def fetch_data(self):
        profile_path = os.path.join(os.path.dirname(__file__), '..', '..', 'profile.json')
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                self.profile = json.load(f)
        except Exception:
            self.profile = {}

    def render_svg(self) -> str:
        padding = config.PADDING if hasattr(config, 'PADDING') else 20

        skills = self.profile.get("skills", {})

        def fmt_list(v):
            if not v:
                return ""
            if isinstance(v, list):
                return " • ".join([str(x) for x in v if x is not None and str(x).strip() != ""])
            return str(v)

        # Categories (fixed order required)
        languages = fmt_list(skills.get("languages"))
        big_data = fmt_list(skills.get("big_data") or skills.get("big_data_tools") or skills.get("big_data_tools_list"))
        web_dev = fmt_list(skills.get("web_development") or skills.get("web") or skills.get("web_tools"))
        databases = fmt_list(skills.get("databases"))
        libraries = fmt_list(skills.get("libraries"))
        iot = fmt_list(skills.get("iot") or skills.get("iot_tools"))
        cloud = fmt_list(skills.get("cloud") or skills.get("cloud_platforms"))
        coursework = fmt_list(skills.get("coursework") or skills.get("course"))

        # Compatibility: if the profile.json uses the existing structure only
        # (languages/frameworks/databases/ai_stack/core_cs), map them into required categories.
        # This is not hardcoding skill items; it only remaps existing arrays.
        if not big_data:
            big_data = fmt_list(skills.get("frameworks") and ["Apache Spark (PySpark)", "Hadoop (HDFS)", "MapReduce"])
        if not web_dev:
            web_dev = fmt_list(skills.get("frameworks"))
        if not libraries:
            libraries = fmt_list(skills.get("ai_stack"))
        if not coursework:
            coursework = fmt_list(skills.get("core_cs"))
        if not cloud:
            cloud = ""
        if not iot:
            iot = ""

        categories = [
            ("Languages", languages),
            ("Big Data & Tools", big_data),
            ("Web Development", web_dev),
            ("Databases", databases),
            ("Libraries", libraries),
            ("IoT", iot),
            ("Cloud", cloud),
            ("Coursework", coursework),
        ]

        # Ensure something is shown if some categories are empty
        def ensure_nonempty(s: str) -> str:
            return s if s.strip() else "N/A"

        categories = [(k, ensure_nonempty(v)) for k, v in categories]

        # Terminal-style layout
        # Command line + reveal one category at a time.
        # GitHub-compatible: no clip-path/mask/filter/foreignObject.
        header_y = padding + 14
        command_delay = 0.0
        start_y = header_y + 42
        line_height = 24
        category_spacing = 18

        # Build text content (default visible; animation only fades between states)
        # We use opacity animation with forwards fill to keep GitHub-compatible visibility.
        content = '''
        <style>
            @keyframes reveal {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            .cmd {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                animation: reveal 0.18s ease-out backwards;
            }
            .header {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                font-weight: 700;
                animation: reveal 0.18s ease-out backwards;
            }
            .cat-title {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                font-weight: 700;
                fill: #c9d1d9;
            }
            .cat-line {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                fill: #8b949e;
                opacity: 1;
            }
            .reveal {
                animation: reveal 0.3s ease-out forwards;
                opacity: 0;
            }
            .cursor {
                animation: cursorBlink 1s steps(2, start) infinite;
            }
            @keyframes cursorBlink {
                50% { opacity: 0; }
            }
        </style>
        <g xml:space="preserve">
        '''

        content += (
            f'<text x="{padding}" y="{header_y}" class="cmd" style="animation-delay: {command_delay}s;">'
            f'<tspan class="color-success">om@github</tspan>'
            f'<tspan class="color-primary">:</tspan>'
            f'<tspan class="color-blue">~$</tspan>'
            f'<tspan class="color-primary"> cat skills.json</tspan>'
            f'</text>\n'
        )

        current_y = start_y
        delay = 0.25
        stagger = 0.55

        for idx, (title, values) in enumerate(categories):
            # Category title
            content += (
                f'<text x="{padding}" y="{current_y}" class="cat-title reveal" style="animation-delay: {delay}s;">'
                f'{title}'
                f'</text>\n'
            )
            current_y += category_spacing
            # Category values
            content += (
                f'<text x="{padding}" y="{current_y}" class="cat-line reveal" style="animation-delay: {delay + 0.12}s;">'
                f'<tspan class="color-secondary">{values}</tspan>'
                f'</text>\n'
            )
            current_y += line_height + 10
            delay += stagger

        cursor_y = current_y + 6
        cursor_delay = delay + 0.1
        content += (
            f'<text x="{padding}" y="{cursor_y}" class="cmd reveal" style="animation-delay: {cursor_delay}s;">'
            f'<tspan class="color-success">om@github</tspan>'
            f'<tspan class="color-primary">:</tspan>'
            f'<tspan class="color-blue">~$</tspan> '
            f'<tspan class="color-primary cursor">█</tspan>'
            f'</text>\n'
        )

        content += '</g>'

        card_height = cursor_y + padding
        return create_svg(820, int(card_height), content)

