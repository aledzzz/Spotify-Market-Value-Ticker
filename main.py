import pygame 
import requests
from io import BytesIO
from database import Database
from music_data import MusicData

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Streamfolio")
title_font = pygame.font.SysFont("Arial", 48, bold = True)
font_data = pygame.font.SysFont("Arial", 18)

def load_image(url):
    response = requests.get(url)
    image = pygame.image.load(BytesIO(response.content))
    return pygame.transform.scale(image, (140, 140))


def main():
    engine = MusicData()
    db = Database()

    portfolio_data = engine.get_portfolio_data()
    screen = pygame.display.set_mode((800, 600))

    covers = []
    rects = []
    for i, j in enumerate(portfolio_data):
        covers.append(load_image(j['album_img']))
        rects.append(pygame.Rect(25 + (i * 155), 80, 140, 140))

    selected_index = None
    running_track = True

    state = "start"
    button_rect = pygame.Rect(300, 300, 200, 50)

    while running_track:
        screen.fill((20, 20, 20))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_track = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "start":
                    if button_rect.collidepoint(event.pos):
                        state = "main"
                        print("Fetching Top 5 Tracks...")
                elif state == "main":
                    for i, j in enumerate(rects):
                        if j.collidepoint(event.pos):
                            selected_index = i
            
            elif event.type == pygame.KEYDOWN:
                if state == "main" and event.key == pygame.K_s:
                    db.portfolio(portfolio_data)
                    db.export()
        
        if state == "start":
            welcome_text = title_font.render("Welcome to Streamfolio", True, (255, 255, 255))
            screen.blit(welcome_text, (400 - welcome_text.get_width() // 2, 200))

            pygame.draw.rect(screen, (250, 70, 22), button_rect, border_radius=5)
            start_text = font_data.render("Press to Start", True, (255, 255, 255))
            screen.blit(start_text, (400 - start_text.get_width() // 2, 315))
        
        elif state == "main":
            instruction = font_data.render("Click an album to view metrics (Press 'S' to Export)", True, (255, 255, 255))
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
                    (f"GLOBAL STREAMS: {track['est_streams']:,}"),
                    (f"EST. GROSS: ${track['finances']['gross']:.2f}"),
                    (f"PLATFORM CUT (30%): -${track['finances']['fee']:.2f}"),
                    (f"EST. NET ROYALTY POOL: ${track['finances']['net']:.2f}")
                ]
                for line in lines:
                    color = (250, 70, 22) if "NET" in line else (255, 255, 255)
                    screen.blit(font_data.render(line, True, color), (50, y))
                    y += 35

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()