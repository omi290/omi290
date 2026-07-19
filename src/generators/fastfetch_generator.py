from .base_generator import BaseGenerator
from utils.svg_builder import create_svg

class FastfetchGenerator(BaseGenerator):
    @property
    def filename(self) -> str:
        return "fastfetch"

    def fetch_data(self):
        pass

    def render_svg(self) -> str:
        return create_svg(400, 300, '<text x="10" y="20" class="terminal-text">Fastfetch Placeholder</text>')
