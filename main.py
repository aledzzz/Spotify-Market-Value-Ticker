import pygame 
import requests
import webbrowser
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
        # Define the base coordinates for the covers
        rects.append(pygame.Rect(25 + (i * 155), 80, 140, 140))

    selected_index = None
    running_track = True

    state = "start"
    button_rect = pygame.Rect(300, 300, 200, 50)
    track_link_rect = pygame.Rect(0, 0, 0, 0) # Initialize hitbox for the Spotify link

    while running_track:
        screen.fill((20, 20, 20))
        
        # Track mouse position constantly for animations
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_track = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "start":
                    if button_rect.collidepoint(event.pos):
                        state = "main"
                        print("Fetching Top 5 Tracks...")
                
                elif state == "main":
                    # 1. Check if the Spotify track link was clicked
                    if selected_index is not None and track_link_rect.collidepoint(event.pos):
                        track_id = portfolio_data[selected_index]['track_id']
                        webbrowser.open(f"https://open.spotify.com/track/{track_id}")
                        
                    # 2. Check if an album cover was clicked
                    for i, j in enumerate(rects):
                        # Calculate the hitbox dynamically in case it is currently "floating"
                        hover_rect = pygame.Rect(j.x, j.y - 10 if j.collidepoint(mouse_pos) else j.y, 140, 140)
                        if hover_rect.collidepoint(event.pos):
                            selected_index = i
            
            elif event.type == pygame.KEYDOWN:
                if state == "main" and event.key == pygame.K_s:
                    db.portfolio(portfolio_data)
                    db.export()
        
        if state == "start":
            welcome_text = title_font.render("Welcome to Streamfolio", True, (255, 255, 255))
            screen.blit(welcome_text, (400 - welcome_text.get_width() // 2, 200))

            # Start button hover color animation
            start_color = (255, 100, 50) if button_rect.collidepoint(mouse_pos) else (250, 70, 22)
            pygame.draw.rect(screen, start_color, button_rect, border_radius=5)
            
            start_text = font_data.render("Press to Start", True, (255, 255, 255))
            screen.blit(start_text, (400 - start_text.get_width() // 2, 315))
        
        elif state == "main":
            info_button_rect = pygame.Rect(740, 20, 30, 30)
            pygame.draw.circle(screen, (200, 200, 200), info_button_rect.center, 15, 2)
            i_text = font_data.render("i", True, (200, 200, 200))
            screen.blit(i_text, (info_button_rect.centerx - i_text.get_width() // 2, info_button_rect.centery - i_text.get_height() // 2))
            
            if info_button_rect.collidepoint(mouse_pos):
                instruction = font_data.render("Click an album to view its metrics (Press 'S' to export)", True, (255, 255, 255))
                tooltip_bg = pygame.Rect(720 - instruction.get_width() - 10, 20, instruction.get_width() + 10, instruction.get_height() + 10)
                pygame.draw.rect(screen, (40, 40, 40), tooltip_bg, border_radius=5)
                pygame.draw.rect(screen, (250, 70, 22), tooltip_bg, 1, border_radius=5) 
                screen.blit(instruction, (tooltip_bg.x + 5, tooltip_bg.y + 5))

            for i, img in enumerate(covers):
                # Hover animation: Float the album cover up 10 pixels if mouse is over it
                is_hovered = rects[i].collidepoint(mouse_pos)
                current_y = rects[i].y - 10 if is_hovered else rects[i].y
                current_rect = pygame.Rect(rects[i].x, current_y, 140, 140)
                
                screen.blit(img, (current_rect.x, current_rect.y))
                if selected_index == i:
                    pygame.draw.rect(screen, (250, 70, 22), current_rect, 4)

            if selected_index is not None:
                track = portfolio_data[selected_index]
                y = 290
                
                # --- RENDER INTERACTIVE TRACK LINK ---
                track_text = f"TRACK: {track['name']} (Listen on Spotify)"
                is_link_hovered = track_link_rect.collidepoint(mouse_pos)
                
                # Turn text Spotify Green if hovered
                track_color = (29, 185, 84) if is_link_hovered else (255, 255, 255) 
                track_surf = font_data.render(track_text, True, track_color)
                
                # Center the text based on the surface width
                track_link_rect = track_surf.get_rect(center=(400, y))
                screen.blit(track_surf, track_link_rect)
                
                # Draw underline if hovered to emulate web link behavior
                if is_link_hovered:
                    pygame.draw.line(screen, (29, 185, 84), (track_link_rect.left, track_link_rect.bottom), (track_link_rect.right, track_link_rect.bottom), 2)
                    
                y += 40
                
                # --- RENDER REMAINING CENTERED METRICS ---
                lines = [
                    (f"ARTIST: {track['artist']}"),
                    (f"GLOBAL STREAMS: {track['est_streams']:,}"),
                    (f"EST. GROSS: ${track['finances']['gross']:.2f}"),
                    (f"PLATFORM CUT (30%): -${track['finances']['fee']:.2f}"),
                    (f"EST. NET ROYALTY POOL: ${track['finances']['net']:.2f}")
                ]
                for line in lines:
                    color = (250, 70, 22) if "NET" in line else (200, 200, 200)
                    text_surf = font_data.render(line, True, color)
                    
                    # Align to center of the screen (x = 400)
                    text_rect = text_surf.get_rect(center=(400, y))
                    screen.blit(text_surf, text_rect)
                    y += 35

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()