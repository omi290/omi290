import os
import json
from .base_generator import BaseGenerator
from utils.svg_builder import create_svg
import config
from utils.xml_utils import xml_escape_text


class ProjectsGenerator(BaseGenerator):
    @property
    def filename(self) -> str:
        return "projects"

    def fetch_data(self):
        profile_path = os.path.join(os.path.dirname(__file__), "..", "..", "profile.json")
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                self.profile = json.load(f)
        except Exception:
            self.profile = {}

    def render_svg(self) -> str:
        padding = config.PADDING if hasattr(config, "PADDING") else 24

        projects = self.profile.get("projects", [])
        if not projects:
            projects = []

        content = '''
        <style>
            @keyframes fade {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            .cmd, .r {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                animation: fade 0.3s backwards;
            }
            .name { font-weight: bold; font-size: 15px; }
        </style>
        <g xml:space="preserve">
        '''

        prompt_y = padding + 14
        content += (
            f'<text x="{padding}" y="{prompt_y}" class="cmd" style="animation-delay: 0s;">'
            f'<tspan class="color-success">om@github</tspan>'
            f'<tspan class="color-primary">:</tspan>'
            f'<tspan class="color-blue">~$</tspan>'
            f'<tspan class="color-primary"> ls projects --featured</tspan>'
            f'</text>\n'
        )

        current_y = prompt_y + 40
        delay = 0.4
        stagger = 0.1

        if projects:
            for idx, p in enumerate(projects):
                if idx > 0:
                    content += f'<text x="{padding}" y="{current_y}" class="r color-secondary" style="animation-delay: {delay}s;">{"-" * 60}</text>\n'
                    current_y += 24
                    delay += stagger

                name = xml_escape_text(p.get("name", "Unnamed"))
                content += (
                    f'<text x="{padding}" y="{current_y}" class="r name color-primary" style="animation-delay: {delay}s;">'
                    f'{name}'
                    f'</text>\n'
                )
                current_y += 20
                delay += stagger

                desc = p.get("description", "")
                if str(desc).strip():
                    desc_escaped = xml_escape_text(desc)
                    content += (
                        f'<text x="{padding}" y="{current_y}" class="r color-secondary" style="animation-delay: {delay}s;">'
                        f'{desc_escaped}'
                        f'</text>\n'
                    )
                    current_y += 24
                    delay += stagger

                tech = p.get("technologies", [])
                tech_str = (
                    " • ".join([str(t) for t in tech if isinstance(t, str) and t.strip()])
                    if isinstance(tech, list)
                    else ""
                ).strip()

                if tech_str:
                    tech_escaped = xml_escape_text(tech_str)
                    content += (
                        f'<text x="{padding}" y="{current_y}" class="r" style="animation-delay: {delay}s;">'
                        f'<tspan class="color-secondary">Stack:</tspan><tspan class="color-blue"> {tech_escaped}</tspan>'
                        f'</text>\n'
                    )
                    current_y += 20
                    delay += stagger

                current_y += 12  # Gap before next project
        else:
            content += f'<text x="{padding}" y="{current_y}" class="r color-secondary" style="animation-delay: {delay}s;">No Projects Found</text>\n'

        content += '</g>'
        card_height = current_y + padding
        return create_svg(820, int(card_height), content)

