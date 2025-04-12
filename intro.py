import pygame, sys

pygame.init()

def fade_intro(SCREEN):
    pygame.init()


    ORIGINAL_LOGO = pygame.image.load("assets/Buksi.png").convert()
    LOGO = pygame.transform.scale(ORIGINAL_LOGO, (1280, 720))
    BG_COLOR = (0,0,0)

    logo_alpha = 0
    fade_in = True
    fade_speed = 5

    clock = pygame.time.Clock()

    running = True

    while running:
        SCREEN.fill(BG_COLOR)  
        logo = LOGO.copy()
        logo.set_alpha(logo_alpha)
        SCREEN.blit(logo, (0, 0))  

        if fade_in:
            logo_alpha += fade_speed
            if logo_alpha >= 255:
                logo_alpha = 255
                pygame.time.delay(1000)  
                fade_in = False
        else:
            logo_alpha -= fade_speed
            if logo_alpha <= 0:
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.update()
        clock.tick(30)

    

if __name__ == "__main__":
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))  
    fade_intro(SCREEN)

    import menu
    menu.main_menu()