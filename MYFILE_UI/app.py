
import pygame
from config import FPS, HEIGHT, WIDTH


from ui.screens.instructions import InstructionsScreen
from ui.screens.screen import Screen
from ui.screens.start_menu import StartMenuScreen


class App:
    """Opens the window, keeps the current screen, switches screens."""
    
    def __init__(self) -> None:
        """Open the window and create every screen."""
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PAC-MAN")
        self.clock = pygame.time.Clock()

        self.screens: dict[str, Screen] = {
            "menu": StartMenuScreen(),
            "instructions": InstructionsScreen(),
            # "final_score": Final_Score(),
            # "final_score": Final_Score(),
        }
        self.current: Screen = self.screens["menu"]
        self.running = True


    def run(self) -> None:
        """Main loop: events -> update -> draw, until the user quits."""
        while self.running:
            elapsed_ms = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    next_screen = self.current.handle_event(event)
                    if next_screen:
                        self.go_to(next_screen)
            
            
            self.current.update(elapsed_ms)
            
            self.current.draw(self.window)
            
            pygame.display.flip()


    def go_to(self, name: str) -> None:
        """Switch to the screen called `name` ("quit" ends the program)."""
        if name == "quit":
            self.running = False
        elif name in self.screens:
            self.current = self.screens[name]
        else:
            print(f"Screen '{name}' is not built yet")
 
