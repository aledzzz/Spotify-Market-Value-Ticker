import pygame
import requests
from io import BytesIO

def get_pygame_image(url):
    """Converts a web URL into a surface Pygame can draw."""
    if not url:
        # Fallback to a generic Gator-Blue surface if no image is found
        surf = pygame.Surface((150, 150))
        surf.fill((0, 33, 165))
        return surf

    response = requests.get(url)
    # Wrap the binary content in BytesIO so Pygame can 'read' it like a file
    img_data = BytesIO(response.content)
    img = pygame.image.load(img_data)
    
    # Standardize the size for your gallery
    return pygame.transform.scale(img, (150, 150))

if __name__ == "__main__":
    main() 