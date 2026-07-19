import os
import json
from .base_generator import BaseGenerator
from utils.svg_builder import create_svg
import config

class ProjectsGenerator(BaseGenerator):
    @property
    def filename(self) -> str:
        return "projects"

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
        
        projects = self.profile.get("projects", [])
        if not projects:
            projects = [{
                "name": "No Projects Found",
                "description": "Please add projects to profile.json",
                "technologies": [],
                "github": "",
                "demo": "",
                "status": "Unknown"
            }]

        # CSS tailored for GitHub compat: 
        # - Default state is visible (opacity 1)
        # - Keyframe animates from opacity 0 to 1
        # - 'backwards' fill-mode hides it during the delay period.
        # If GitHub strips the animation, it gracefully falls back to opacity: 1 default.
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
            a { text-decoration: none; cursor: pointer; }
            a:hover { text-decoration: underline; }
        </style>
        <g xml:space="preserve">
        '''
        
        prompt_y = padding + 14
        content += f'<text x="{padding}" y="{prompt_y}" class="cmd" style="animation-delay: 0s;">'
        content += '<tspan class="color-success">om@github</tspan><tspan class="color-primary">:</tspan><tspan class="color-blue">~$</tspan><tspan class="color-primary"> ls projects --featured</tspan>'
        content += '</text>\n'
        
        current_y = prompt_y + 40
        delay = 0.4
        stagger = 0.1
        
        for idx, p in enumerate(projects):
            if idx > 0:
                content += f'<text x="{padding}" y="{current_y}" class="r color-secondary" style="animation-delay: {delay}s;">{"-" * 60}</text>\n'
                current_y += 24
                delay += stagger
                
            # 1. Name
            name = p.get("name", "Unnamed")
            content += f'<text x="{padding}" y="{current_y}" class="r name color-primary" style="animation-delay: {delay}s;">{name}</text>\n'
            current_y += 20
            delay += stagger
            
            # 2. Description
            desc = p.get("description", "")
            if desc:
                content += f'<text x="{padding}" y="{current_y}" class="r color-secondary" style="animation-delay: {delay}s;">{desc}</text>\n'
                current_y += 24
                delay += stagger
            
            # 3. Stack
            tech = p.get("technologies", [])
            if tech:
                tech_str = " • ".join(tech)
                content += f'<text x="{padding}" y="{current_y}" class="r" style="animation-delay: {delay}s;">'
                content += f'<tspan class="color-secondary">Stack : </tspan><tspan class="color-blue">{tech_str}</tspan>'
                content += '</text>\n'
                current_y += 20
                delay += stagger
            
            # 4. Links
            gh = p.get("github", "")
            demo = p.get("demo", "")
            if gh or demo:
                content += f'<text x="{padding}" y="{current_y}" class="r" style="animation-delay: {delay}s;">'
                content += '<tspan class="color-secondary">Links : </tspan>'
                links_arr = []
                if gh:
                    href = f"https://{gh}" if not gh.startswith("http") else gh
                    links_arr.append(f'<a href="{href}" target="_blank"><tspan class="color-primary">Repository ↗</tspan></a>')
                if demo:
                    href = f"https://{demo}" if not demo.startswith("http") else demo
                    links_arr.append(f'<a href="{href}" target="_blank"><tspan class="color-primary">Live ↗</tspan></a>')
                
                content += ' | '.join(links_arr)
                content += '</text>\n'
                current_y += 20
                delay += stagger
                
            # 5. Status
            status = p.get("status", "")
            if status:
                content += f'<text x="{padding}" y="{current_y}" class="r" style="animation-delay: {delay}s;">'
                content += f'<tspan class="color-secondary">Status: </tspan><tspan class="color-success">● {status}</tspan>'
                content += '</text>\n'
                current_y += 20
                delay += stagger
                
            current_y += 12 # Gap before next project

        content += '</g>'
        card_height = current_y + padding
        
        return create_svg(820, int(card_height), content)
