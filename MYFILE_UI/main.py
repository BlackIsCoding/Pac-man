
from app import App
import pygame

def main() -> None:
    """Run the App. Return 0 on success, 1 on a clean error."""
    try:
        App().run()
    except Exception as error:
        print(f"Error: {error}")
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()