import math
import random

def generate_flower_svg(filename="flower.svg"):
    width, height = 500, 500
    cx, cy = width // 2, height // 2
    
    svg_content = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background-color: #f0f8ff;">',
        f'<title>Procedural Flower</title>'
    ]
    
    # Draw Stem
    svg_content.append(f'<path d="M{cx} {cy+50} Q{cx-20} {cy+150} {cx} {height-20}" stroke="#2ecc71" stroke-width="8" fill="none" />')
    
    # Draw Leaves
    svg_content.append(f'<path d="M{cx} {height-100} Q{cx-50} {height-130} {cx-60} {height-150} Q{cx-30} {height-80} {cx} {height-90}" fill="#27ae60" />')
    svg_content.append(f'<path d="M{cx} {height-120} Q{cx+50} {height-150} {cx+60} {height-170} Q{cx+30} {height-100} {cx} {height-110}" fill="#27ae60" />')

    # Draw Petals
    num_layers = 4
    petals_per_layer = 12
    
    colors = ["#3498db", "#9b59b6", "#e74c3c", "#f1c40f"]
    
    for layer in range(num_layers):
        radius = 120 - (layer * 25)
        color = colors[layer % len(colors)]
        
        for i in range(petals_per_layer):
            angle_deg = (360 / petals_per_layer) * i + (layer * 15)
            angle_rad = math.radians(angle_deg)
            
            # Petal center offset slightly from center
            px = cx + math.cos(angle_rad) * (radius * 0.2)
            py = cy + math.sin(angle_rad) * (radius * 0.2)
            
            # SVG rotate transform rotates around 0,0 by default, so we need to specify center
            transform = f'rotate({angle_deg}, {px}, {py})'
            
            svg_content.append(
                f'<ellipse cx="{px}" cy="{py}" rx="{radius}" ry="{radius * 0.3}" fill="{color}" opacity="0.9" transform="{transform}" stroke="white" stroke-width="1"/>'
            )

    # Center of the flower
    svg_content.append(f'<circle cx="{cx}" cy="{cy}" r="25" fill="#f39c12" stroke="#d35400" stroke-width="3"/>')
    
    # Add some decorative dots in the center
    for _ in range(15):
        dx = random.randint(-15, 15)
        dy = random.randint(-15, 15)
        if dx*dx + dy*dy <= 20*20:
             svg_content.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="2" fill="#d35400"/>')

    svg_content.append('</svg>')
    
    with open(filename, 'w') as f:
        f.write("\n".join(svg_content))
    
    print(f"Generated {filename} successfully.")

def print_ascii_flower():
    flower = r"""
      .-.
    __   /   \   __
   (  `'.\   /.'`  )
    '-._.(;;;)._.-'
    .-'  ,`"`,  '-.
   (__.-'/   \'-.__)
         \   /
          '-'
           |
           |
           |
         ,_|_
    """
    print("Here is a text version for you:")
    print(flower)

if __name__ == "__main__":
    print_ascii_flower()
    generate_flower_svg()
