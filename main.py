import pygame 
import requests
import webbrowser
from io import BytesIO
from database import Database
from music_data import MusicData

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Streamfolio")

available_fonts = pygame.font.get_fonts()
font_name = "segoeui" if "segoeui" in available_fonts else ("helvetica" if "helvetica" in available_fonts else "arial")
title_font = pygame.font.SysFont(font_name, 42, bold=True)
header_font = pygame.font.SysFont(font_name, 22, bold=True)
font_data = pygame.font.SysFont(font_name, 16, bold=True)
small_font = pygame.font.SysFont(font_name, 14)

BG_COLOR = (15, 23, 42)          
CARD_COLOR = (30, 41, 59)        
ACCENT_COLOR = (56, 189, 248)    
TEXT_MAIN = (248, 250, 252)      
TEXT_MUTED = (148, 163, 184)     
MONEY_GREEN = (52, 211, 153)     
MONEY_RED = (248, 113, 113)      
BORDER_COLOR = (51, 65, 85)      

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
        rects.append(pygame.Rect(25 + (i * 155), 90, 140, 140))

    selected_index = None
    running_track = True

    state = "start"
    button_rect = pygame.Rect(300, 330, 200, 50)
    track_link_rect = pygame.Rect(0, 0, 0, 0) 

    while running_track:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_track = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "start":
                    if button_rect.collidepoint(event.pos):
                        state = "main"
                        print("Fetching my top 5 tracks...")
                
                elif state == "main":
                    if selected_index is not None and track_link_rect.collidepoint(event.pos):
                        track_id = portfolio_data[selected_index]['track_id']
                        webbrowser.open(f"https://open.spotify.com/track/{track_id}")
                        
                    for i, j in enumerate(rects):
                        hover_rect = pygame.Rect(j.x, j.y - 10 if j.collidepoint(mouse_pos) else j.y, 140, 140)
                        if hover_rect.collidepoint(event.pos):
                            selected_index = i
            
            elif event.type == pygame.KEYDOWN:
                if state == "main" and event.key == pygame.K_s:
                    db.portfolio(portfolio_data)
                    db.export()
        
        if state == "start":
            welcome_text = title_font.render("Streamfolio", True, TEXT_MAIN)
            sub_text = font_data.render("Music Portfolio Valuation Engine", True, TEXT_MUTED)
            
            screen.blit(welcome_text, (400 - welcome_text.get_width() // 2, 220))
            screen.blit(sub_text, (400 - sub_text.get_width() // 2, 270))

            start_color = ACCENT_COLOR if button_rect.collidepoint(mouse_pos) else (14, 165, 233)
            pygame.draw.rect(screen, start_color, button_rect, border_radius=8)
            
            start_text = font_data.render("Launch Dashboard", True, BG_COLOR)
            screen.blit(start_text, (400 - start_text.get_width() // 2, 345))
        
        elif state == "main":
            # Header
            logo_text = title_font.render("Streamfolio", True, TEXT_MAIN)
            screen.blit(logo_text, (25, 25))

            # Info Button
            info_button_rect = pygame.Rect(740, 35, 30, 30)
            pygame.draw.circle(screen, BORDER_COLOR, info_button_rect.center, 15, 2)
            i_text = font_data.render("i", True, TEXT_MUTED)
            screen.blit(i_text, (info_button_rect.centerx - i_text.get_width() // 2, info_button_rect.centery - i_text.get_height() // 2))
            
            if info_button_rect.collidepoint(mouse_pos):
                instruction = small_font.render("Click an album to view its metrics (Press 'S' to export)", True, TEXT_MAIN)
                tooltip_bg = pygame.Rect(720 - instruction.get_width() - 10, 35, instruction.get_width() + 10, instruction.get_height() + 10)
                pygame.draw.rect(screen, CARD_COLOR, tooltip_bg, border_radius=5)
                pygame.draw.rect(screen, BORDER_COLOR, tooltip_bg, 1, border_radius=5) 
                screen.blit(instruction, (tooltip_bg.x + 5, tooltip_bg.y + 5))

            # Album Row
            for i, img in enumerate(covers):
                is_hovered = rects[i].collidepoint(mouse_pos)
                current_y = rects[i].y - 10 if is_hovered else rects[i].y
                current_rect = pygame.Rect(rects[i].x, current_y, 140, 140)
                
                # Drop shadow
                shadow = pygame.Rect(current_rect.x + 5, current_rect.y + 5, 140, 140)
                pygame.draw.rect(screen, (8, 12, 22), shadow, border_radius=4)
                
                screen.blit(img, (current_rect.x, current_rect.y))
                if selected_index == i:
                    highlight_rect = pygame.Rect(current_rect.x - 3, current_rect.y - 3, 146, 146)
                    pygame.draw.rect(screen, ACCENT_COLOR, highlight_rect, 3, border_radius=4)

            # Data Card Component
            if selected_index is not None:
                track = portfolio_data[selected_index]
                
                # Main Card Background & Shadow
                shadow_rect = pygame.Rect(50, 275, 700, 290)
                pygame.draw.rect(screen, (8, 12, 22), shadow_rect, border_radius=12)
                card_rect = pygame.Rect(50, 270, 700, 290)
                pygame.draw.rect(screen, CARD_COLOR, card_rect, border_radius=12)
                pygame.draw.rect(screen, BORDER_COLOR, card_rect, width=1, border_radius=12) 
                
                # Track Header
                track_text = title_font.render(track['name'], True, TEXT_MAIN)
                screen.blit(track_text, (80, 290))
                artist_text = header_font.render(track['artist'], True, TEXT_MUTED)
                screen.blit(artist_text, (80, 335))

                # Spotify Pill Button
                link_text = small_font.render("Listen on Spotify", True, BG_COLOR)
                link_rect = pygame.Rect(0, 0, link_text.get_width() + 24, 28)
                link_rect.topright = (720, 305)
                
                is_link_hovered = link_rect.collidepoint(mouse_pos)
                link_color = (29, 185, 84) if is_link_hovered else (25, 214, 95)
                pygame.draw.rect(screen, link_color, link_rect, border_radius=14)
                screen.blit(link_text, (link_rect.x + 12, link_rect.y + 6))
                track_link_rect = link_rect 
                
                # Section Divider
                pygame.draw.line(screen, BORDER_COLOR, (80, 380), (720, 380), 1)

                lbl_streams = small_font.render("TOTAL GLOBAL STREAMS", True, TEXT_MUTED)
                val_streams = header_font.render(f"{track['est_streams']:,}", True, TEXT_MAIN)
                screen.blit(lbl_streams, (80, 410))
                screen.blit(val_streams, (80, 430))

                lbl_gross = small_font.render("EST. GROSS REVENUE", True, TEXT_MUTED)
                val_gross = header_font.render(f"${track['finances']['gross']:,.2f}", True, TEXT_MAIN)
                screen.blit(lbl_gross, (400, 410))
                screen.blit(val_gross, (400, 430))
                
                lbl_cut = small_font.render("PLATFORM CUT (30%)", True, TEXT_MUTED)
                val_cut = header_font.render(f"-${track['finances']['fee']:,.2f}", True, MONEY_RED)
                screen.blit(lbl_cut, (80, 480))
                screen.blit(val_cut, (80, 500))

                lbl_net = small_font.render("EST. NET ROYALTY POOL", True, TEXT_MUTED)
                val_net = header_font.render(f"${track['finances']['net']:,.2f}", True, MONEY_GREEN)
                screen.blit(lbl_net, (400, 480))
                screen.blit(val_net, (400, 500))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()