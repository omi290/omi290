import os
import json
from .base_generator import BaseGenerator
from utils.svg_builder import create_svg
import config

class FastfetchGenerator(BaseGenerator):
    @property
    def filename(self) -> str:
        return "fastfetch"

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
        
        # Read from profile
        personal = self.profile.get("personal", {})
        skills = self.profile.get("skills", {})
        projects = self.profile.get("projects", [])
        achievements = self.profile.get("achievements", [])
        
        # Helper to map fields to their respective value colors
        def make_stat(key, value, color_class="color-primary"):
            return (key, value, color_class)
            
        stats = [
            make_stat("OS", personal.get("os", "GitHub")),
            make_stat("Host", personal.get("host", "N/A")),
            make_stat("Role", personal.get("role", "N/A")),
            make_stat("Specialization", personal.get("specialization", "N/A")),
            make_stat("Languages", " ".join(skills.get("languages", [])), "color-blue"),
            make_stat("Frameworks", " ".join(skills.get("frameworks", [])), "color-blue"),
            make_stat("Databases", " ".join(skills.get("databases", [])), "color-blue"),
            make_stat("AI Stack", " ".join(skills.get("ai_stack", [])), "color-blue"),
            make_stat("Core CS", " ".join(skills.get("core_cs", [])), "color-blue"),
            make_stat("Projects", " | ".join(p.get("name", "") if isinstance(p, dict) else p for p in projects)),
            make_stat("Achievements", achievements[0] if achievements else "N/A"),
            make_stat("LeetCode", personal.get("leetcode", "N/A")),
            make_stat("Status", personal.get("status", "N/A"), "color-success")
        ]
        
        # Setup animation CSS - Optimized and compressed
        content = '''
        <style>
            @keyframes t {
                from { clip-path: inset(0 100% 0 0); }
                to { clip-path: inset(0 0 0 0); }
            }
            @keyframes b {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
            .r {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                clip-path: inset(0 100% 0 0);
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
        
        # Dynamic label width calculation
        label_width = max(len(k) for k, v, c in stats) + 2
        
        for i, (key, value, color_class) in enumerate(stats):
            delay = start_delay + (i * stagger_delay)
            content += f'<text x="{padding}" y="{current_y}" class="r {color_class}" style="animation-delay: {delay}s;">'
            content += f'<tspan class="color-secondary">{key.ljust(label_width)}</tspan>{value}'
            content += '</text>\n'
            current_y += 24

        total_rows = len(stats)
        cursor_delay = start_delay + (total_rows * stagger_delay) + 0.15
        current_y += 12
        content += f'<text x="{padding}" y="{current_y}" class="r c" style="animation-delay: {cursor_delay}s;">'
        content += '<tspan class="color-success">om@github</tspan><tspan class="color-primary">:</tspan><tspan class="color-blue">~$</tspan> <tspan class="color-primary">█</tspan>'
        content += '</text>\n</g>'
        
        # Responsive GitHub dimension setup handled strictly by inner bounds
        card_height = current_y + padding
        
        return create_svg(820, int(card_height), content)
