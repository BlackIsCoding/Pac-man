"""The start menu: logo and four buttons."""
import pygame

from config import (EXIT_BUTTON, HIGHSCORES_BUTTON, INSTRUCTIONS_BUTTON,
                    MENU_LOGO, START_BUTTON, WIDTH)
from ui.button import Button
from ui.images import load_image
from ui.screens.screen import Screen


class StartMenuScreen(Screen):
    """The first screen. Each button leads to another screen."""

    def __init__(self) -> None:
        """Load the logo and create the buttons."""
        super().__init__()
        logo = load_image(MENU_LOGO, alpha=True)
        width, height = logo.get_size()
        self.logo = pygame.transform.scale(
            logo, (int(width * 1.9), int(height * 1.9)))
        self.logo_rect = self.logo.get_rect(midtop=(WIDTH // 2, 90))

        middle = WIDTH // 2
        # screen name to go to -> the button that leads there
        self.buttons = {
            "game": Button(START_BUTTON, (middle, 600)),
            "highscores": Button(HIGHSCORES_BUTTON, (middle, 700)),
            "instructions": Button(INSTRUCTIONS_BUTTON, (middle, 800)),
            "quit": Button(EXIT_BUTTON, (middle, 900)),
        }

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Return the screen of the clicked button. ESC quits."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "quit"
        for target, button in self.buttons.items():
            if button.is_clicked(event):
                return target
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the background, the logo and the buttons."""
        super().draw(surface)
        surface.blit(self.logo, self.logo_rect)
        for button in self.buttons.values():
            button.draw(surface)