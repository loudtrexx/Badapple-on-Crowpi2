import pygame
import glob
import time

# --- Setup pygame ---
pygame.init()
screen = pygame.display.set_mode((320, 240))  # adjust resolution to your screen
pygame.display.set_caption("Bad Apple!!")

# --- Load frames ---
frames = sorted(glob.glob("frame_*.png"))
images = [pygame.image.load(f) for f in frames]

FPS = 15
clock = pygame.time.Clock()

# --- Playback loop ---
running = True
while running:
    for img in images:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(img, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
