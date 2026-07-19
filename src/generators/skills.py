from .base_generator import BaseGenerator
from utils.svg_builder import create_svg

class SkillsGenerator(BaseGenerator):
    @property
    def filename(self) -> str:
        return "skills"

    def fetch_data(self):
        pass

    def render_svg(self) -> str:
        return create_svg(800, 200, '<text x="10" y="20" class="terminal-text">Skills Placeholder</text>')
