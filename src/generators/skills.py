import os
import json
from .base_generator import BaseGenerator
from utils.svg_builder import create_svg
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
        except Exception as e:
            self.profile = {}
            print(f"Error loading profile.json: {e}")

    def render_svg(self) -> str:
        padding = config.PADDING if hasattr(config, 'PADDING') else 24
        
        skills = self.profile.get("skills", {})
        
        # GitHub-safe CSS: fade in with backwards fill so it's fully visible statically if stripped
        content = '''
        <style>
            @keyframes fade {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
            .cmd, .r, .stagger {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                animation: fade 0.2s backwards;
            }
            .cursor {
                animation: blink 1s infinite;
            }
        </style>
        <g xml:space="preserve">
        '''
        
        prompt_y = padding + 14
        # Terminal command
        content += f'<text x="{padding}" y="{prompt_y}" class="cmd" style="animation-delay: 0s;">'
        content += '<tspan class="color-success">om@github</tspan><tspan class="color-primary">:</tspan><tspan class="color-blue">~$</tspan><tspan class="color-primary"> skills --all</tspan>'
        content += '</text>\n'
        
        current_y = prompt_y + 40
        delay = 0.3
        
        # Define categories to display in order, with display names and specific accent colors
        skill_groups = [
            ("Languages", skills.get("languages", []), "color-primary"),
            ("Frontend", skills.get("frontend", []), "color-primary"),
            ("Backend", skills.get("backend", []), "color-primary"),
            ("AI / ML", skills.get("ai_ml", []), "color-blue"),
            ("Databases", skills.get("databases", []), "color-primary"),
            ("Cloud & DevOps", skills.get("cloud_devops", []), "color-success"),
            ("Developer Tools", skills.get("developer_tools", []), "color-primary"),
            ("Core CS", skills.get("core_cs", []), "color-primary"),
            ("Embedded / IoT", skills.get("embedded_iot", []), "color-primary")
        ]
        
        # Filter empty groups
        skill_groups = [(k, v, c) for k, v, c in skill_groups if v]
        
        # Total stagger time needs to fit under 2.5s.
        # Command (0.3) + total groups * stagger + total skills * skill_stagger
        total_items = sum(len(v) + 1 for _, v, _ in skill_groups) # +1 for category header
        stagger = 1.8 / total_items if total_items > 0 else 0.1
        
        for k, v, color_class in skill_groups:
            # Render Category Header
            content += f'<text x="{padding}" y="{current_y}" class="r color-secondary" style="animation-delay: {delay:.2f}s;">{k}</text>\n'
            current_y += 24
            delay += stagger
            
            # Render Skills on one line, but stagger them individually
            content += f'<text x="{padding}" y="{current_y}" class="r" style="animation-delay: {delay:.2f}s;">'
            
            for i, skill in enumerate(v):
                # Skill
                content += f'<tspan class="{color_class} stagger" style="animation-delay: {delay:.2f}s;">{skill}</tspan>'
                delay += stagger
                # Separator
                if i < len(v) - 1:
                    content += f'<tspan class="color-secondary stagger" style="animation-delay: {delay:.2f}s;"> • </tspan>'
                    delay += stagger
            
            content += '</text>\n'
            current_y += 26
            
        # Blinking cursor
        cursor_delay = delay + 0.1
        content += f'<text x="{padding}" y="{current_y}" class="r cursor" style="animation-delay: {cursor_delay:.2f}s;">'
        content += '<tspan class="color-success">om@github</tspan><tspan class="color-primary">:</tspan><tspan class="color-blue">~$</tspan> <tspan class="color-primary">█</tspan>'
        content += '</text>\n'
        
        content += '</g>'
        card_height = current_y + padding + 14
        
        return create_svg(820, int(card_height), content)
