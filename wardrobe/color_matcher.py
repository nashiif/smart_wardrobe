# wardrobe/color_matcher.py

from typing import List, Tuple
import colorsys

class ColorMatcher:
    def __init__(self):
        # Define basic color harmonies
        self.color_harmonies = {
            'monochromatic': self.get_monochromatic,
            'complementary': self.get_complementary,
            'analogous': self.get_analogous,
            'triadic': self.get_triadic
        }
        
    def hex_to_hsv(self, hex_color: str) -> Tuple[float, float, float]:
        """Convert hex color to HSV."""
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')
        
        # Convert hex to RGB
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB to HSV
        hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        return hsv
    
    def hsv_to_hex(self, hsv: Tuple[float, float, float]) -> str:
        """Convert HSV to hex color."""
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        return '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
    
    def get_monochromatic(self, base_color: str, variations: int = 5) -> List[str]:
        """Generate monochromatic color scheme."""
        base_hsv = self.hex_to_hsv(base_color)
        colors = []
        
        for i in range(variations):
            # Vary brightness while keeping hue and saturation constant
            new_value = max(0.2, min(1.0, base_hsv[2] * (0.5 + i * 0.25)))
            new_hsv = (base_hsv[0], base_hsv[1], new_value)
            colors.append(self.hsv_to_hex(new_hsv))
            
        return colors
    
    def get_complementary(self, base_color: str) -> List[str]:
        """Generate complementary color scheme."""
        base_hsv = self.hex_to_hsv(base_color)
        
        # Complementary color is opposite on the color wheel (180 degrees or 0.5 in HSV)
        complementary_hsv = ((base_hsv[0] + 0.5) % 1.0, base_hsv[1], base_hsv[2])
        
        return [base_color, self.hsv_to_hex(complementary_hsv)]
    
    def get_analogous(self, base_color: str) -> List[str]:
        """Generate analogous color scheme."""
        base_hsv = self.hex_to_hsv(base_color)
        colors = []
        
        # Generate colors 30 degrees (0.083 in HSV) apart
        for angle in [-0.083, 0, 0.083]:
            new_hue = (base_hsv[0] + angle) % 1.0
            colors.append(self.hsv_to_hex((new_hue, base_hsv[1], base_hsv[2])))
            
        return colors
    
    def get_triadic(self, base_color: str) -> List[str]:
        """Generate triadic color scheme."""
        base_hsv = self.hex_to_hsv(base_color)
        colors = []
        
        # Generate colors 120 degrees (0.333 in HSV) apart
        for i in range(3):
            new_hue = (base_hsv[0] + (i * 0.333)) % 1.0
            colors.append(self.hsv_to_hex((new_hue, base_hsv[1], base_hsv[2])))
            
        return colors
    
    def suggest_matching_colors(self, base_color: str, harmony_type: str = 'complementary') -> List[str]:
        """Suggest matching colors based on color harmony type."""
        if harmony_type in self.color_harmonies:
            return self.color_harmonies[harmony_type](base_color)
        return []