import os
from dotenv import load_dotenv

# --------------------------
# Central Configuration
# --------------------------

# Output Directories
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')
GENERATED_DIR = os.path.join(ASSETS_DIR, 'generated')
STATIC_DIR = os.path.join(ASSETS_DIR, 'static')

# Animation Timings (in seconds)
ANIMATION_DURATION = 2.0
FADE_IN_DELAY = 0.5

# SVG Base Sizes
SVG_WIDTH = 800
FASTFETCH_WIDTH = 400
FASTFETCH_HEIGHT = 300

# Spacing & Layout
PADDING = 20
MARGIN = 15

# Placeholder Data
GITHUB_USERNAME_PLACEHOLDER = "your-github-username"

def load_config():
    """Loads environment variables and returns a configuration dictionary."""
    load_dotenv()
    
    gh_token = os.getenv("GH_TOKEN")
    if not gh_token:
        print("WARNING: GH_TOKEN not found in environment. Rate limits may apply.")
        
    return {
        "gh_token": gh_token,
        "assets_dir": ASSETS_DIR,
        "generated_dir": GENERATED_DIR,
        "static_dir": STATIC_DIR
    }

