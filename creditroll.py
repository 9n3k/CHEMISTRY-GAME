import pygame
import sys
import os

pygame.init()

pygame.mixer.music.load("assets/creditroll1.mp3")  
pygame.mixer.music.set_volume(0.5) 


music_started = False
music_delay = 150


WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg_image = pygame.image.load("assets/MENUBG.png").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
bg_overlay = pygame.Surface((WIDTH, HEIGHT))
bg_overlay.set_alpha(200)  
bg_overlay.fill((0, 0, 0))
pygame.display.set_caption("Scrolling Credits")
icon = pygame.image.load("assets/ICON.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_CYAN = (0, 139, 139)
font_path = "assets/font.ttf"


title_font_size = 70
title_font = pygame.font.Font(font_path, title_font_size)
title_surface = title_font.render("ACID BREAKOUT", True, WHITE)


def scale_image_keep_aspect(image, max_width, max_height):
    width, height = image.get_size()
    scale = min(max_width / width, max_height / height)
    return pygame.transform.smoothscale(image, (int(width * scale), int(height * scale)))

# Load images
thanks_image1 = pygame.image.load("lab assets/us_1.png").convert_alpha()
thanks_image2 = pygame.image.load("lab assets/us_2.png").convert_alpha()

# Use aspect-ratio-preserving scaling
max_width = 600
max_height = 500
thanks_image1 = scale_image_keep_aspect(thanks_image1, max_width, max_height)
thanks_image2 = scale_image_keep_aspect(thanks_image2, max_width, max_height)

current_thanks_image = thanks_image1
image_switch_time = 1000  # milliseconds (1 second delay between images)
last_image_switch = 0

# Credit lines
credits = [
    "GAME DIRECTOR",
    "Allison Liman",
    "","",
    

    "LEAD ARTIST",
    "Eliana Tedja",
    "","",
    

    "LEAD PROGRAMMER",
    "Jason Aurelius Widjaja",
    "","",
    
    
    "PROGRAMMER",
    "Jennifer Cahyadi",
    "Allison Liman",
    "","",
    
    
    "Researchers",
    "Christopher Dillon",
    "Jennifer Cahyadi",
    "","",
    

    "CUTSCENE MAKER",
    "Allison Liman",
    "","",
    
    
    "TRAILER",
    "Gabrielle Danica Budiman",
    "Della Estelle Huang",
    "Allison Liman",
    "","",
    

    "MUSIC",
    "Gabrielle Danica Budiman",
    "Della Estelle Huang",
    "","",
    
    

    "Made using",
    "Python, Pygame",
    "","",
    

    "SPECIAL THANKS",
    "Everyone who supported this project!",
    "","",
    
    "THANKS FOR PLAYING!",
    "SHOW_IMAGE",
    "","",
]


sizes = []
for line in credits:
    if line.strip() == "":
        sizes.append(20)  
    elif line.isupper() or line.istitle():  
        if line == "THANKS FOR PLAYING!":
            sizes.append(60)
        elif line.isupper():  
            sizes.append(28)
        else:
            sizes.append(28)  
    else:
        sizes.append(32) 

# Render text surfaces with matching sizes
credit_surfaces = []
for line, size in zip(credits, sizes):
    if line == "SHOW_IMAGE":
        credit_surfaces.append(("image", current_thanks_image))  # store image type
    else:
        surface = pygame.font.Font(font_path, size).render(line, True, WHITE)
        credit_surfaces.append(("text", surface))
# Combine title + credits into one list with proper positioning
line_spacing = 60
title_extra_spacing = 100  # extra gap after title

# Total height includes title + spacing + all credit lines
total_height = title_surface.get_height() + title_extra_spacing + len(credit_surfaces) * line_spacing

# Start Y just below the screen
start_y = HEIGHT

delay_before_scroll = 1500
start_time = pygame.time.get_ticks()

fade_in_text = pygame.font.Font(font_path, 55).render("Back to Main Menu", True, WHITE)
fade_in_alpha = 0
fade_in_speed = 5  # Rate at which the text fades in
fade_in_displayed = False  # Flag to know when to show the button

# Button hitbox for "Back to Main Menu"
button_rect = pygame.Rect(WIDTH // 2 - fade_in_text.get_width() // 2, HEIGHT // 2, fade_in_text.get_width(), fade_in_text.get_height())


running = True
while running:
    screen.blit(bg_image, (0, 0))   
    screen.blit(bg_overlay, (0, 0)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

            
        if not music_started and pygame.time.get_ticks() - start_time > music_delay:
           pygame.mixer.music.play(loops=-1, fade_ms=3000)
           music_started = True
           
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_x, mouse_y):  # If clicked inside the button's rectangle
                
                os.system('python menu.py')  
                
                pygame.quit()
                sys.exit() 


    # Draw the big title
    title_x = WIDTH // 2 - title_surface.get_width() // 2
    title_y = start_y
    screen.blit(title_surface, (title_x, title_y))

    # Draw the rest of the credits
    for i, (content_type, surface) in enumerate(credit_surfaces):
        y_pos = start_y + title_surface.get_height() + title_extra_spacing + i * line_spacing
        if content_type == "text":
            x_pos = WIDTH // 2 - surface.get_width() // 2
            screen.blit(surface, (x_pos, y_pos))
        elif content_type == "image":
            x_pos = WIDTH // 2 - surface.get_width() // 2
            screen.blit(surface, (x_pos, y_pos + 40))

    # Move everything upward
    if pygame.time.get_ticks() - start_time > delay_before_scroll:
       elapsed = pygame.time.get_ticks() - start_time
       scroll_speed = min(0.8, 0.5 + elapsed / 5000)  
       start_y -= scroll_speed

    # Stop when the whole thing has scrolled past the top
    if start_y + total_height < 0:
        # Trigger the fade-in effect for "Back to Main Menu"
        if fade_in_alpha < 255:
            fade_in_alpha += fade_in_speed
        fade_in_displayed = True
        show_thanks_image = True
        if show_thanks_image:
            image_x = WIDTH // 2 - current_thanks_image.get_width() // 2
            image_y = HEIGHT // 2 - current_thanks_image.get_height() - 50
            screen.blit(current_thanks_image, (image_x, image_y))

    current_time = pygame.time.get_ticks()
    if current_time - last_image_switch > image_switch_time:
        current_thanks_image = (
            thanks_image2 if current_thanks_image == thanks_image1 else thanks_image1
        )
        last_image_switch = current_time

    # Draw the "Back to Main Menu" button if it's faded in
    if fade_in_displayed:
        fade_in_text.set_alpha(fade_in_alpha)
        fade_in_x = WIDTH // 2 - fade_in_text.get_width() // 2
        fade_in_y = HEIGHT // 2
        # Check if the mouse is hovering over the button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_x, mouse_y):
            fade_in_text = pygame.font.Font(font_path, 55).render("Back to Main Menu", True, DARK_CYAN)  
        else:
            fade_in_text = pygame.font.Font(font_path, 55).render("Back to Main Menu", True, WHITE) 
        screen.blit(fade_in_text, (fade_in_x, fade_in_y))
    pygame.display.flip()
    clock.tick(60)
    
pygame.mixer.music.fadeout(2000)


pygame.quit()
sys.exit()

