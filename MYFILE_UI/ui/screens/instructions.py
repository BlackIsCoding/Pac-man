"""The instructions screen: a picture and a back button."""
import pygame

from config import BACK_BUTTON, INSTRUCTIONS_LOGO, WIDTH
from ui.button import Button
from ui.images import load_image
from ui.screens.screen import Screen


class InstructionsScreen(Screen):
    """Shows how to play. Back (or ESC) returns to the menu."""

    def __init__(self) -> None:
        """Load the picture and create the back button."""
        super().__init__()
        logo = load_image(INSTRUCTIONS_LOGO, alpha=True)
        width, height = logo.get_size()
        self.logo = pygame.transform.scale(
            logo, (int(width * 1.2), int(height * 1.2)))
        self.logo_rect = self.logo.get_rect(midtop=(WIDTH // 2, 90))
        self.back_button = Button(BACK_BUTTON, (WIDTH // 2, 700))

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Go back to the menu on a Back click or ESC."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "menu"
        if self.back_button.is_clicked(event):
            return "menu"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the background, the picture and the back button."""
        super().draw(surface)
        surface.blit(self.logo, self.logo_rect)
        self.back_button.draw(surface)
