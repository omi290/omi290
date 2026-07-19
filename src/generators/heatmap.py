from .base_generator import BaseGenerator
from utils.svg_builder import create_svg

import os
import json
from .base_generator import BaseGenerator
from utils.svg_builder import create_svg


class HeatmapGenerator(BaseGenerator):
    @property
    def filename(self) -> str:
        return "heatmap"

    def fetch_data(self):
        # Lightweight and GitHub-compatible.
        # No external calls to keep generation deterministic/offline.
        profile_path = os.path.join(os.path.dirname(__file__), "..", "..", "profile.json")
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                self.profile = json.load(f)
        except Exception:
            self.profile = {}

    def render_svg(self) -> str:
        # Lightweight activity-style widget (no forbidden SVG features).
        padding = 20
        header_y = padding + 14

        # 52-week x 7-day-style grid (compressed)
        cols = 12
        rows = 7
        cell = 10
        gap = 3
        width = 800

        grid_x = padding
        grid_y = header_y + 30

        seed_values = (
            len(self.profile.get("projects", []))
            + len(self.profile.get("skills", {}).get("languages", []))
            + len(self.profile.get("achievements", []))
        )

        cells = []
        for c in range(cols):
            for r in range(rows):
                idx = (c * 31 + r * 17 + seed_values) % 10
                if idx <= 1:
                    color = "#0e4429"
                elif idx <= 3:
                    color = "#006d32"
                elif idx <= 5:
                    color = "#26a641"
                elif idx <= 7:
                    color = "#39d353"
                else:
                    color = "#3fb950"

                x = grid_x + c * (cell + gap)
                y = grid_y + r * (cell + gap)
                cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{color}" />')

        legend_y = grid_y + rows * (cell + gap) + 18
        content = f"""<style>
            @keyframes fade {{ from {{opacity:0}} to {{opacity:1}} }}
            .title {{ font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; fill: #c9d1d9; animation: fade 0.3s ease-out backwards; }}
            .grid {{ animation: fade 0.3s ease-out backwards; }}
        </style>
        <text x="{padding}" y="{header_y}" class="title">om@github:~$ github activity</text>
        <text x="{padding}" y="{legend_y-6}" style="font-family: 'JetBrains Mono', monospace; font-size: 12px; fill:#8b949e;">Loading GitHub contribution data...</text>
        <g class="grid">{''.join(cells)}</g>
        """

        height = int(legend_y - padding + 30)
        return create_svg(width, height, content)

