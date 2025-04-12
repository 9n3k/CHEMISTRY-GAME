import pygame, sys
import options
from options import Checkbox, show_options, create_checkboxes
from options import Slider, create_sliders
from options import Dropdown
from button import Button
from language import translations, current_lang, set_language, get_translation, get_font_size
from intro import fade_intro
from game import start_game

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/MENUBG.png")

def darken_background_image(image, opacity=150):
    darkened = image.copy()
    dark_overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, opacity))  
    darkened.blit(dark_overlay, (0, 0))  
    return darkened

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(topleft=(100, 200))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(100, 300), 
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    return  

        pygame.display.update()



def options():
    global SCREEN, current_lang
    
    clock = pygame.time.Clock()
    
    back_text = get_translation("◀BACK")  

    OPTIONS_BACK = Button(image=None, pos=(175, 650), 
                          text_input=back_text, font=get_font(55), 
                          base_color="#dddddd", hovering_color="Dark Cyan")


    
    checkboxes = create_checkboxes(current_lang)
    sliders = create_sliders(current_lang)
    dropdown = Dropdown(100, 80, ["English", "Filipino", "Bahasa Indonesia"], current_lang)


    running = True
    while running: 
        SCREEN.blit(darken_background_image(BG), (0, 0))

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        show_options(SCREEN, checkboxes, sliders, dropdown)  

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for checkbox in checkboxes:
            checkbox.draw(SCREEN)
        for slider in sliders:
            slider.draw(SCREEN)
        dropdown.draw(SCREEN)
        dropdown.draw_expanded(SCREEN)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return  

            for checkbox in checkboxes:
                checkbox.handle_event(event)
            for slider in sliders:
                slider.handle_event(event)
                
            selected_lang = dropdown.handle_event(event)
            if selected_lang:
                lang_name = selected_lang.strip().replace("▼", "")
                set_language(lang_name)
                current_lang = lang_name
                dropdown.selected = lang_name + "▼"
                
                checkboxes = create_checkboxes(current_lang)
                sliders = create_sliders(current_lang)
                
        back_text = get_translation("◀BACK")
        back_font_size = get_font_size("◀BACK")  

        OPTIONS_BACK = Button(image=None, pos=(175, 650), 
                        text_input=back_text, font=get_font(back_font_size),
                        base_color="#dddddd", hovering_color="Dark Cyan")


            

        pygame.display.update()
        clock.tick(60)
        

def main_menu():
    running = True

    try:
        button_image = None

    except pygame.error:
        print("ERROR: Button image not found! Check the path: assets/button.png")
        pygame.quit()
        sys.exit()

    LEFT_MARGIN = 100
    BUTTON_X = LEFT_MARGIN + 145
    TOTAL_BUTTONS = 3  
    TOP_PADDING = 250  
    BOTTOM_PADDING = 150

    available_space = 720 - (TOP_PADDING + BOTTOM_PADDING)
    BUTTON_SPACING = (available_space // (TOTAL_BUTTONS - 1)) - 20
    BUTTON_Y_START = TOP_PADDING

    while running:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        title_text = get_translation("ACID BREAKOUT")
        start_text = get_translation("Play")
        options_text = get_translation("Options")
        quit_text = get_translation("Quit")
        footer_key = "© 2025 Acid Breakout | Developed by Allison, Chris Dillon, Danica, Della, Eliana, Jason AW, Jennifer of 10.3 | All rights reserved"
        footer_text = get_translation(footer_key)
        

        MENU_TEXT = get_font(get_font_size("ACID BREAKOUT")).render(title_text, True, "#dddddd")
        MENU_RECT = MENU_TEXT.get_rect(topleft=(LEFT_MARGIN, 50))

        PLAY_BUTTON = Button(image=None, pos=(BUTTON_X, BUTTON_Y_START), 
                     text_input=start_text, font=get_font(get_font_size("Play")),  
                     base_color="White", hovering_color="Dark Cyan")

        OPTIONS_BUTTON = Button(image=None, pos=(BUTTON_X, BUTTON_Y_START + BUTTON_SPACING), 
                                text_input=options_text, font=get_font(get_font_size("Options")), 
                                base_color="White", hovering_color="Dark Cyan")

        QUIT_BUTTON = Button(image=None, pos=(BUTTON_X, BUTTON_Y_START + 2 * BUTTON_SPACING), 
                            text_input=quit_text, font=get_font(get_font_size("Quit")), 
                            base_color="White", hovering_color="Dark Cyan")


        
        FOOTER_TEXT = get_font(get_font_size(footer_key)).render(footer_text, True, "#dddddd")
        FOOTER_RECT = FOOTER_TEXT.get_rect(topleft=(LEFT_MARGIN, 680))

        SCREEN.blit(FOOTER_TEXT, FOOTER_RECT)
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    start_game(1)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
   pygame.init()
   SCREEN = pygame.display.set_mode((1280, 720))
   
   fade_intro(SCREEN)
   main_menu()
   start_game(1)