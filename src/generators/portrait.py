from .base_generator import BaseGenerator
from utils.svg_builder import create_svg

class PortraitGenerator(BaseGenerator):
    @property
    def filename(self) -> str:
        return "portrait"

    def fetch_data(self):
        pass

    def render_svg(self) -> str:
        # Placeholder for portrait generation
        return create_svg(400, 300, '<text x="10" y="20" class="terminal-text">Portrait Placeholder</text>')
