import pygame 
import requests
from io import BytesIO
from database import Database
from music_data import MusicData

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400,300))
pygame.display.set_caption("Streamfolio")
title_font = pygame.font.SysFont("Arial", 24, bold = True)
font_data = pygame.font.SysFont("Arial", 18)

def load_image(url):
    response = requests.get(url)
    image = pygame.image.load(BytesIO(response.content))
    return pygame.transform.scale(image, (200, 400))

def audio_preview(url):
    if url:
        response = requests.get(url)
        audio_file = BytesIO(requests.content)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.stop()
        print("No preview available for this track.")

def main():



if __name__ == "__main__":
    main()