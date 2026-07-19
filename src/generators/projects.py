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
            # Fallback
            projects = [{
                "name": "No Projects Found",
                "description": "Please add projects to profile.json",
                "technologies": [],
                "github": "",
                "demo": "",
                "status": "Unknown"
            }]

        content = '''
        <style>
            @keyframes t {
                from { clip-path: inset(0 100% 0 0); }
                to { clip-path: inset(0 0 0 0); }
            }
            @keyframes f {
                from { opacity: 0; transform: translateY(5px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .cmd {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                clip-path: inset(0 100% 0 0);
                animation: t 0.3s linear forwards;
            }
            .r {
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                opacity: 0;
                animation: f 0.2s ease-out forwards;
            }
            .name { font-weight: bold; }
        </style>
        <g xml:space="preserve">
        '''
        
        prompt_y = padding + 14
        content += f'<text x="{padding}" y="{prompt_y}" class="cmd" style="animation-delay: 0s;">'
        content += '<tspan class="color-success">om@github</tspan><tspan class="color-primary">:</tspan><tspan class="color-blue">~$</tspan><tspan class="color-primary"> ls projects --featured</tspan>'
        content += '</text>\n'
        
        current_y = prompt_y + 40
        delay = 0.4  # Start after command finishes
        stagger = 0.08 # Very fast line by line to keep under 3 seconds
        
        for idx, p in enumerate(projects):
            # 1. Separator (optional, or just top padding)
            if idx > 0:
                content += f'<text x="{padding}" y="{current_y}" class="r color-secondary" style="animation-delay: {delay}s;">{"-" * 65}</text>\n'
                current_y += 24
                delay += stagger
                
            # 2. Name
            name = p.get("name", "Unnamed")
            content += f'<text x="{padding}" y="{current_y}" class="r name color-primary" style="animation-delay: {delay}s;">{name}</text>\n'
            current_y += 20
            delay += stagger
            
            # 3. Description
            desc = p.get("description", "")
            content += f'<text x="{padding}" y="{current_y}" class="r color-secondary" style="animation-delay: {delay}s;">{desc}</text>\n'
            current_y += 26
            delay += stagger
            
            # 4. Tech Stack
            tech = p.get("technologies", [])
            tech_str = " • ".join(tech)
            content += f'<text x="{padding}" y="{current_y}" class="r" style="animation-delay: {delay}s;">'
            content += f'<tspan class="color-secondary">Stack:  </tspan><tspan class="color-blue">{tech_str}</tspan>'
            content += '</text>\n'
            current_y += 20
            delay += stagger
            
            # 5. GitHub
            gh = p.get("github", "")
            if gh:
                content += f'<text x="{padding}" y="{current_y}" class="r" style="animation-delay: {delay}s;">'
                content += f'<tspan class="color-secondary">GitHub: </tspan><tspan class="color-primary">{gh}</tspan>'
                content += '</text>\n'
                current_y += 20
                delay += stagger
                
            # 6. Demo
            demo = p.get("demo", "")
            if demo:
                content += f'<text x="{padding}" y="{current_y}" class="r" style="animation-delay: {delay}s;">'
                content += f'<tspan class="color-secondary">Demo:   </tspan><tspan class="color-primary">{demo}</tspan>'
                content += '</text>\n'
                current_y += 20
                delay += stagger
                
            # 7. Status
            status = p.get("status", "")
            if status:
                content += f'<text x="{padding}" y="{current_y}" class="r" style="animation-delay: {delay}s;">'
                content += f'<tspan class="color-secondary">Status: </tspan><tspan class="color-success">{status}</tspan>'
                content += '</text>\n'
                current_y += 20
                delay += stagger
                
            current_y += 16 # Extra gap before next project

        content += '</g>'
        
        card_height = current_y + padding
        
        return create_svg(820, int(card_height), content)
