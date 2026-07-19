import os
import json
import logging
from config import load_config
from generators.portrait import PortraitGenerator
from generators.fastfetch_generator import FastfetchGenerator
from generators.heatmap import HeatmapGenerator
from generators.skills import SkillsGenerator
from generators.projects import ProjectsGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting SVG Generation...")
    
    # 1. Load configuration and environment
    config = load_config()
    
    # 2. Gather data (could also be done inside generators)
    logger.info("Fetching data...")
    
    # 3. Initialize generators
    generators = [
        PortraitGenerator(config),
        FastfetchGenerator(config),
        HeatmapGenerator(config),
        SkillsGenerator(config),
        ProjectsGenerator(config)
    ]
    
    # 4. Run generators
    output_base_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'generated')
    
    # Mapping generator filename to their subfolder category
    # This is a basic implementation of the new folder structure
    generator_folders = {
        "portrait": "ascii",
        "fastfetch": "ascii",
        "heatmap": "heatmap",
        "skills": "skills",
        "projects": "projects"
    }
    
    for gen in generators:
        logger.info(f"Running {gen.__class__.__name__}...")
        gen.fetch_data()
        svg_content = gen.render_svg()
        
        folder = generator_folders.get(gen.filename, "cards")
        output_dir = os.path.join(output_base_dir, folder)
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f"{gen.filename}.svg")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        logger.info(f"Saved {output_path}")

    logger.info("Generation complete.")

if __name__ == "__main__":
    main()
