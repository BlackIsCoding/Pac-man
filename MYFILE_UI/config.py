"""Settings shared by every screen: window size, colours, image files."""
from pathlib import Path

WIDTH, HEIGHT = 1900, 1300
FPS = 60

ASSETS = Path(__file__).parent / "assets"

# shared
BACKGROUND_IMAGE = ASSETS / "background-image.png"

# start menu
MENU_LOGO = ASSETS / "pac_man.png"
START_BUTTON = ASSETS / "start_game_button.png"
HIGHSCORES_BUTTON = ASSETS / "highscores_button.png"
INSTRUCTIONS_BUTTON = ASSETS / "instructions_button.png"
EXIT_BUTTON = ASSETS / "exit_button.png"

# instructions screen
INSTRUCTIONS_LOGO = ASSETS / "instructions.png"
BACK_BUTTON = ASSETS / "back_button.png"

# final score screen
RED_GHOST_LOGO = ASSETS / "GO_log_Blinky.webp"
THUMB_UP_PAC_MAN = ASSETS / "THUMB_UP_PAC_MAC.png"
SAVE_BUTTON = ASSETS / "save_button_ui.png"
INPUT_NAME_IMAGE = ASSETS / "name_input.png"
MAX_NAME_LENGTH = 15