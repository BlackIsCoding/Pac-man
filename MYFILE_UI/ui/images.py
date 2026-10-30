from pathlib import Path
 
import pygame
 
 

 
def load_image(path: Path, alpha: bool = False) -> pygame.Surface:
    """Load an image. Use alpha=True for images with transparency."""
    try:
        image = pygame.image.load(path)
    except (FileNotFoundError, pygame.error) as error:
        raise AssetError(f"cannot load {path.name}: {error}") from error
    return image.convert_alpha() if alpha else image.convert()