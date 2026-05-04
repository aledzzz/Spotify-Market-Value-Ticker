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
        audio_file = BytesIO(response.content)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.stop()
        print("No preview available for this track.")

def main():
    engine = MusicData()
    db = Database()

    print("Fetching Top 5 Tracks...")
    portfolio_data = engine.get_portfolio_data()

    covers = []
    rects = []
    for i, j in enumerate(portfolio_data):
        covers.append(load_image(j['album_img']))
        rects.append(pygame.Rect(40 + (i * 100), 80, 160, 160))

    selected_index = None
    running_track = True

    while running_track:
        screen.fill((255, 255, 255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_track = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, j in enumerate(rects):
                    if j.collidepoint(event.pos):
                        selected_index = i
                        audio_preview(portfolio_data[i]['preview_url'])
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    print("Initializing pipeline...")
                    db.portfolio(portfolio_data)
                    db.export()
        
        instruction = font_data.render("Click an album to view metrics | Press 'S' to Export to Tableau", True, (255, 255, 255))
        screen.blit(instruction, (40, 20))

        for i, img in enumerate(covers):
            screen.blit(img, (rects[i].x, rects[i].y))
            if selected_index == i:
                pygame.draw.rect(screen, (250, 70, 22), rects[i], 4)

        if selected_index is not None:
            track = portfolio_data[selected_index]
            y = 300
            lines = [
                (f"TRACK: {track['name']} | ARTIST: {track['artist']}"),
                (f"SPOTIFY POPULARITY:  {track['popularity']} / 100"),
                (f"EST. GLOBAL STREAMS: {track['est_streams']:,}"),
                (f"--------------------------------------------------"),
                (f"EST. GROSS:          ${track['finances']['gross']:.2f}"),
                (f"PLATFORM CUT (30%): -${track['finances']['fee']:.2f}"),
                (f"NET ROYALTY POOL:    ${track['finances']['net']:.2f}")
            ]
            for line in lines:
                color = (250, 70, 22) if "NET" in line else (255, 255, 255)
                screen.blit(font_data.render(line, True, color), (50, y))
                y += 35

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()