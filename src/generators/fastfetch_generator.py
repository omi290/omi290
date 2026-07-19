import os
import json
from .base_generator import BaseGenerator
from utils.svg_builder import create_svg
import config
from utils.theme import ACTIVE_THEME

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
        
        # Mapping to required fields
        os_val = personal.get("os", "GitHub")
        host_val = personal.get("host", "N/A")
        role_val = personal.get("role", "N/A")
        spec_val = personal.get("specialization", "N/A")
        
        langs_val = " ".join(skills.get("languages", []))
        frames_val = " ".join(skills.get("frameworks", []))
        db_val = " ".join(skills.get("databases", []))
        ai_val = " ".join(skills.get("ai_stack", []))
        cs_val = " ".join(skills.get("core_cs", []))
        
        proj_val = " | ".join(projects)
        achieve_val = achievements[0] if achievements else "N/A"
        leetcode_val = personal.get("leetcode", "N/A")
        status_val = personal.get("status", "N/A")
        
        # Key-value mapping
        stats = [
            ("OS", os_val),
            ("Host", host_val),
            ("Role", role_val),
            ("Specialization", spec_val),
            ("Languages", langs_val),
            ("Frameworks", frames_val),
            ("Databases", db_val),
            ("AI Stack", ai_val),
            ("Core CS", cs_val),
            ("Projects", proj_val),
            ("Achievements", achieve_val),
            ("LeetCode", leetcode_val),
            ("Status", status_val)
        ]
        
        # Setup animation CSS
        content = '''
        <style>
            @keyframes typing {
                from { clip-path: inset(0 100% 0 0); }
                to { clip-path: inset(0 0 0 0); }
            }
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
            .ff-row {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                white-space: pre;
                clip-path: inset(0 100% 0 0);
                animation: typing 0.4s steps(50, end) forwards;
            }
            .cursor {
                animation: blink 1s infinite;
            }
        </style>
        '''
        
        prompt_y = padding + 14
        content += f'<text x="{padding}" y="{prompt_y}" class="ff-row" style="animation-delay: 0s;">'
        content += f'<tspan class="color-success">om@github</tspan><tspan class="color-primary">:</tspan><tspan class="color-blue">~$</tspan><tspan class="color-primary"> fastfetch</tspan>'
        content += '</text>\n'
        
        current_y = prompt_y + 42 # Add gap after prompt
        stagger_delay = 0.1
        start_delay = 0.5 # Wait for prompt to finish typing
        
        # Calculate max key length for proper alignment
        max_key_len = max(len(k) for k, v in stats)
        # Pad slightly
        label_width = max_key_len + 2
        
        for i, (key, value) in enumerate(stats):
            delay = start_delay + (i * stagger_delay)
            # We construct the line as a single text element to animate cleanly
            content += f'<text x="{padding}" y="{current_y}" class="ff-row" style="animation-delay: {delay}s;" xml:space="preserve">'
            # Label
            content += f'<tspan class="color-success">{key.ljust(label_width)}</tspan>'
            # Value
            content += f'<tspan class="color-primary">{value}</tspan>'
            content += '</text>\n'
            current_y += 24 # Standard line height

        total_rows = len(stats)
        cursor_delay = start_delay + (total_rows * stagger_delay) + 0.4
        current_y += 12
        content += f'<text x="{padding}" y="{current_y}" class="ff-row cursor" style="animation-delay: {cursor_delay}s;" xml:space="preserve">'
        content += f'<tspan class="color-success">om@github</tspan><tspan class="color-primary">:</tspan><tspan class="color-blue">~$</tspan> <tspan class="color-primary">█</tspan>'
        content += '</text>\n'
        
        # Set dimension dynamically based on content height
        card_height = current_y + padding
        
        return create_svg(820, int(card_height), content)
