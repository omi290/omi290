import os
from PIL import Image, ImageEnhance
import rembg
import math
from .base_generator import BaseGenerator
from utils.svg_builder import create_svg
import config

class PortraitGenerator(BaseGenerator):
    @property
    def filename(self) -> str:
        return "portrait"

    def fetch_data(self):
        # We process the image during fetch_data
        image_path = os.path.join(config.STATIC_DIR, 'photos', 'profile.jpg')
        if not os.path.exists(image_path):
            print(f"Warning: Photo not found at {image_path}")
            self.ascii_art = ["Photo not found."]
            return

        try:
            # 1. Remove background
            with open(image_path, 'rb') as i:
                input_bytes = i.read()
            output_bytes = rembg.remove(input_bytes)
            
            # Load processed image
            import io
            img = Image.open(io.BytesIO(output_bytes))
            
            # 2. Convert to grayscale & ensure white background for alpha channel if needed
            # Actually, rembg leaves alpha. We want transparent background mapped to space ' '.
            # So we separate the alpha mask.
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            gray_img = img.convert('L')
            alpha = img.split()[3]
            
            # 3. Enhance local contrast
            enhancer = ImageEnhance.Contrast(gray_img)
            gray_img = enhancer.enhance(1.5)
            
            # 1. Detect foreground bounding box
            bbox = alpha.getbbox()
            if bbox:
                gray_img = gray_img.crop(bbox)
                alpha = alpha.crop(bbox)
            
            # 4. Resize
            # Target width/height bounds
            max_width_px = config.PORTRAIT_WIDTH - (config.PADDING * 2)
            max_height_px = config.PORTRAIT_HEIGHT - 32 - config.PADDING
            
            char_width = config.ASCII_FONT_SIZE * 0.6 # JetBrains Mono aspect ratio is ~0.6
            char_height = config.ASCII_LINE_HEIGHT
            
            max_cols = int(max_width_px / char_width)
            max_rows = int(max_height_px / char_height)
            
            # Target size: 80% of available space
            target_cols = int(max_cols * 0.8)
            target_rows = int(max_rows * 0.8)
            
            orig_width, orig_height = gray_img.size
            aspect_ratio = (orig_height / char_height) / (orig_width / char_width)
            
            if (orig_width / char_width) > (orig_height / char_height):
                new_width = target_cols
                new_height = int(target_cols * aspect_ratio)
            else:
                new_height = target_rows
                new_width = int(target_rows / aspect_ratio)
                
            new_width = min(max(new_width, 1), target_cols)
            new_height = min(max(new_height, 1), target_rows)
            
            gray_img = gray_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            alpha = alpha.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Calculate offsets to center the image
            offset_x = (max_cols - new_width) // 2
            offset_y = (max_rows - new_height) // 2
            
            # 5. Convert to ASCII centered grid
            self.ascii_art = []
            chars = config.ASCII_CHARS
            num_chars = len(chars)
            
            for r in range(max_rows):
                row = ""
                for c in range(max_cols):
                    img_x = c - offset_x
                    img_y = r - offset_y
                    
                    if 0 <= img_x < new_width and 0 <= img_y < new_height:
                        a_val = alpha.getpixel((img_x, img_y))
                        if a_val < 128:
                            row += " " # Transparent
                        else:
                            g_val = gray_img.getpixel((img_x, img_y))
                            idx = int((g_val / 255.0) * (num_chars - 1))
                            row += chars[idx]
                    else:
                        row += " " # Empty padding
                self.ascii_art.append(row)
                
        except Exception as e:
            print(f"Error processing portrait: {e}")
            self.ascii_art = ["Error processing image."]

    def render_svg(self) -> str:
        padding = config.PADDING if hasattr(config, 'PADDING') else 24
        content_start_y = 32 + padding # Header + padding
        
        content = ""
        
        # We need a CSS keyframe block for the typing animation
        # We inject this directly into the SVG
        total_rows = len(self.ascii_art) if hasattr(self, 'ascii_art') else 1
        
        content += '''
        <style>
            @keyframes typing {
                from { clip-path: inset(0 100% 0 0); }
                to { clip-path: inset(0 0 0 0); }
            }
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
            .ascii-row {
                font-family: 'JetBrains Mono', monospace;
                font-size: ''' + str(config.ASCII_FONT_SIZE) + '''px;
                white-space: pre;
                clip-path: inset(0 100% 0 0);
                animation: typing 0.5s steps(40, end) forwards;
            }
            .cursor {
                animation: blink 1s infinite;
            }
        </style>
        '''
        
        if not hasattr(self, 'ascii_art'):
            self.ascii_art = ["No image loaded."]
            
        current_y = content_start_y
        stagger_delay = 0.1
        
        from utils.theme import ACTIVE_THEME
        theme_fg = ACTIVE_THEME.foreground

        for i, row in enumerate(self.ascii_art):
            delay = i * stagger_delay
            # Add a slight delay to start
            animation_style = f"animation-delay: {delay + config.FADE_IN_DELAY}s;"
            
            content += f'<text x="{padding}" y="{current_y}" class="ascii-row" style="{animation_style} fill: {theme_fg};" xml:space="preserve">'
            content += row
            content += '</text>\n'
            current_y += config.ASCII_LINE_HEIGHT
            
        # Blinking cursor at the end
        cursor_delay = (total_rows * stagger_delay) + config.FADE_IN_DELAY + 0.5
        content += f'<text x="{padding}" y="{current_y}" class="ascii-row cursor" style="animation-delay: {cursor_delay}s; fill: {theme_fg};">█</text>\n'
        
        return create_svg(config.PORTRAIT_WIDTH, config.PORTRAIT_HEIGHT, content)
