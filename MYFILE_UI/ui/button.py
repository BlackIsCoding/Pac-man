"""A clickable image button."""
from pathlib import Path
 
import pygame


from ui.images import load_image

class Button:
    """An image on the screen that can be clicked with the left mouse."""

    def __init__(self, image_path: Path, midtop: tuple[int, int]) -> None:
        """Load the image and place it: midtop = (centre x, top y)."""
        self.image = load_image(image_path, alpha=True)
        self.rect = self.image.get_rect(midtop=midtop)
    
    def draw(self, surface: pygame.Surface) -> None: #???
        """Draw the button on `surface`."""
        surface.blit(self.image, self.rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """Return True if `event` is a left click inside the button."""
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))