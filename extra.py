import pygame
from pathlib import Path
print(Path(__file__).parent / "speech.mp3")

pygame.init()
pygame.mixer.init()

try:
    pygame.mixer.music.load(Path(__file__).parent / "speech.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
except pygame.error as e:
    print(f"No se pudo reproducir el archivo: {e}")
finally:
    pygame.mixer.quit()
