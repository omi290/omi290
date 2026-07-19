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
        
        # ASCII Logo (Simple generic tech logo representation)
        ascii_logo = [
            "  ██████╗ ███╗   ███╗ ",
            " ██╔═══██╗████╗ ████║ ",
            " ██║   ██║██╔████╔██║ ",
            " ██║   ██║██║╚██╔╝██║ ",
            " ╚██████╔╝██║ ╚═╝ ██║ ",
            "  ╚═════╝ ╚═╝     ╚═╝ "
        ]
        
        # Extract fields from profile safely
        personal = self.profile.get("personal", {})
        education = self.profile.get("education", {})
        skills = self.profile.get("skills", {})
        achievements = self.profile.get("achievements", [])
        
        username = personal.get("name", config.GITHUB_USERNAME_PLACEHOLDER).lower()
        role = personal.get("role", "N/A")
        status = personal.get("status", "N/A")
        degree = education.get("degree", "N/A")
        college = education.get("college", "N/A")
        
        languages = ", ".join(skills.get("languages", ["N/A"]))
        frameworks = ", ".join(skills.get("frameworks", ["N/A"]))
        databases = ", ".join(skills.get("databases", ["N/A"]))
        ai_stack = ", ".join(skills.get("ai_stack", ["N/A"]))
        core_cs = ", ".join(skills.get("core_cs", ["N/A"]))
        achievement_str = achievements[0] if achievements else "N/A"
        
        header = f"{username}@github"
        
        # Build Stats list
        stats = [
            ("Role", role),
            ("Education", f"{degree} @ {college}"),
            ("Languages", languages),
            ("Frameworks", frameworks),
            ("Databases", databases),
            ("AI Stack", ai_stack),
            ("Core CS", core_cs),
            ("Achievement", achievement_str),
            ("Status", status)
        ]
        
        content = ""
        
        # 1. Add Prompt
        prompt_y = padding + 14
        content += f'<text x="{padding}" y="{prompt_y}" class="terminal-text">'
        content += f'<tspan class="color-success">om@github</tspan><tspan>:</tspan><tspan class="color-primary">~$</tspan> fastfetch'
        content += '</text>\n'
        
        content_start_y = prompt_y + 32
        
        # 2. Render ASCII Logo (Left Side)
        logo_x = padding
        current_y = content_start_y
        for line in ascii_logo:
            content += f'<text x="{logo_x}" y="{current_y}" class="terminal-text color-primary" xml:space="preserve">{line}</text>\n'
            current_y += 21
            
        # 3. Render Stats (Right Side)
        stats_x = logo_x + 180  # Offset to the right of the logo
        current_y = content_start_y
        
        # Header
        content += f'<text x="{stats_x}" y="{current_y}" class="terminal-text-bold color-success">{header}</text>\n'
        current_y += 10
        content += f'<text x="{stats_x}" y="{current_y}" class="terminal-text color-secondary">{"-" * len(header)}</text>\n'
        current_y += 21
        
        # Key-Value pairs
        for key, value in stats:
            # truncate value if too long to prevent overflow
            max_len = 22
            display_val = value if len(value) <= max_len else value[:max_len-3] + "..."
            
            content += f'<text x="{stats_x}" y="{current_y}" class="terminal-text" xml:space="preserve">'
            content += f'<tspan class="color-primary">{key.ljust(11)}</tspan><tspan>: </tspan><tspan>{display_val}</tspan>'
            content += '</text>\n'
            current_y += 21
            
        return create_svg(config.PORTRAIT_WIDTH, config.PORTRAIT_HEIGHT, content)
