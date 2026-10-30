import pygame

from config import BACKGROUND_IMAGE, HEIGHT, WIDTH
from ui.images import load_image


class Screen:
    """A screen knows how to react to events and how to draw itself.

    It never opens a window or runs a loop: the App does that.
    """

    def __init__(self) -> None:
        """Load the background that all screens share."""
        self.background = pygame.transform.scale(
            load_image(BACKGROUND_IMAGE), (WIDTH, HEIGHT))

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """React to one event.

        Return the name of the screen to go to next, or None to stay here.
        """
        return None

    def update(self, elapsed_ms: int) -> None:
        """Advance animations or game logic (most screens do nothing)."""

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the screen. Subclasses call this first for the background."""
        surface.blit(self.background, (0, 0))