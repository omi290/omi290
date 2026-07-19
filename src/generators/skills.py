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
            .cmd, .r {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                animation: fade 0.3s backwards;
            }
        </style>
        <g xml:space="preserve">
        '''
        
        prompt_y = padding + 14
        # Terminal command
        content += f'<text x="{padding}" y="{prompt_y}" class="cmd" style="animation-delay: 0s;">'
        content += '<tspan class="color-success">om@github</tspan><tspan class="color-primary">:</tspan><tspan class="color-blue">~$</tspan><tspan class="color-primary"> cat skills.json</tspan>'
        content += '</text>\n'
        
        current_y = prompt_y + 40
        delay = 0.4
        stagger = 0.15
        
        # Opening bracket
        content += f'<text x="{padding}" y="{current_y}" class="r color-primary" style="animation-delay: {delay}s;">{{</text>\n'
        current_y += 24
        delay += stagger
        
        # Prepare skills for structured mapping
        skill_groups = [
            ("Languages", skills.get("languages", [])),
            ("Frameworks", skills.get("frameworks", [])),
            ("Databases", skills.get("databases", [])),
            ("AI Stack", skills.get("ai_stack", [])),
            ("Core CS", skills.get("core_cs", []))
        ]
        
        # Filter empty
        skill_groups = [(k, v) for k, v in skill_groups if v]
        
        # Determine label width for proper alignment
        max_len = max([len(k) for k, v in skill_groups]) if skill_groups else 10
        label_width = max_len + 5 # "Key": + padding
        
        for i, (key, values) in enumerate(skill_groups):
            key_str = f'"{key}":'
            val_str = ", ".join(values)
            
            content += f'<text x="{padding + 24}" y="{current_y}" class="r" style="animation-delay: {delay}s;">'
            content += f'<tspan class="color-secondary">{key_str.ljust(label_width)}</tspan>'
            content += f'<tspan class="color-primary">[ </tspan>'
            content += f'<tspan class="color-blue">{val_str}</tspan>'
            content += f'<tspan class="color-primary"> ]</tspan>'
            
            # Add comma if not the last item
            if i < len(skill_groups) - 1:
                content += '<tspan class="color-primary">,</tspan>'
                
            content += '</text>\n'
            
            current_y += 24
            delay += stagger
            
        # Closing bracket
        content += f'<text x="{padding}" y="{current_y}" class="r color-primary" style="animation-delay: {delay}s;">}}</text>\n'
        
        content += '</g>'
        card_height = current_y + padding + 14
        
        return create_svg(820, int(card_height), content)
