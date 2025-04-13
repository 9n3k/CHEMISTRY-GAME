import pygame
from language import translations, current_lang, set_language, get_translation

current_lang = "English"

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
BG = pygame.image.load("assets/MENUBG.png")
BG.set_alpha(150)

checkbox_unchecked = pygame.image.load("assets/checkboxno.png")
checkbox_checked = pygame.image.load("assets/checkboxyes.png")

def darken_background(screen, opacity = 50):
    dark_overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, opacity))  
    screen.blit(dark_overlay, (0, 0))  

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

class Checkbox:
    def __init__(self, x, y, text, lang="English", checked=False):
        self.checked = checked
        self.text_key = text  
        self.lang = lang
        self.font = get_font(25)
        self.image_unchecked = checkbox_unchecked
        self.image_checked = checkbox_checked
        self.image_size = self.image_unchecked.get_size()
        self.rect = pygame.Rect(x, y, self.image_size[0], self.image_size[1])

    def draw(self, screen):
        # Draw the appropriate checkbox (checked or unchecked)
        screen.blit(self.image_checked if self.checked else self.image_unchecked, self.rect)
        
        # Get the correct translation for the checkbox label
        label = translations[self.lang][self.text_key]
        text_surface = self.font.render(label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(midleft=(self.rect.right + 15, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event, toggle_func=None):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.checked = not self.checked  
            
            if self.text_key == "Fullscreen":
                # Toggle fullscreen or windowed mode
                if self.checked:
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen with dynamic resolution
                else:
                    pygame.display.set_mode((1280, 720), pygame.RESIZABLE)  # Windowed mode with fixed resolution
                
                # Optionally, you can call a toggle function if passed
                if toggle_func:
                    toggle_func(self.checked)


class Slider:
    def __init__(self, x, y, text_key, lang="English", min_value=0, max_value=100, value=100):
        self.x, self.y = x, y
        self.text_key = text_key
        self.lang = lang
        self.min_value, self.max_value = min_value, max_value
        self.value, self.width, self.height = value, 200, 10
        self.slider_rect = pygame.Rect(self.x, self.y + 15, self.width, self.height)
        self.knob_rect = pygame.Rect(self.x + (self.value / self.max_value) * self.width - 5, self.y + 10, 10, 20)
        self.dragging = False
        self.font = get_font(25)

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.slider_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.knob_rect)
        label = translations[self.lang][self.text_key]
        text_surface = self.font.render(f"{label}: {self.value}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(midleft=(self.x + self.width + 25, self.knob_rect.centery))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.knob_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = max(self.x, min(event.pos[0], self.x + self.width))
            self.value = round(((new_x - self.x) / self.width) * self.max_value)
            self.knob_rect.x = new_x - 10

class Dropdown:
    def __init__(self, x, y, options, default):
        self.font = get_font(40)
        self.options = options
        self.selected_option = default
        self.selected = default + "▼"
        self.rect = pygame.Rect(x, y, 690, 60)
        self.expanded = False

    def draw(self, screen):
        pygame.draw.rect(screen, (80, 80, 80), self.rect)
        text_surface = self.font.render(self.selected, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def draw_expanded(self, screen):
        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * 50, 690, 60)
                pygame.draw.rect(screen, (50, 50, 50), option_rect)
                text_surface = self.font.render(option, True, (255, 255, 255))
                screen.blit(text_surface, (option_rect.x + 10, option_rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
            elif self.expanded:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * 50, 690, 50)
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = option
                        self.selected = option + "▼"
                        self.expanded = False
                        return option
                self.expanded = False
        return None

def create_checkboxes(lang):
    labels = ["Screen Shake", "Fullscreen"]
    start_y = 200
    spacing = 100
    return [Checkbox(100, start_y + i * spacing, label, lang=lang) for i, label in enumerate(labels)]

def create_sliders(lang):
    return [Slider(800, 220, "MUS", lang=lang), 
            Slider(800, 350, "SFX", lang=lang)]

def show_options(screen, checkboxes, sliders, dropdown):
    for checkbox in checkboxes:
        checkbox.draw(screen)
    for slider in sliders:
        slider.draw(screen)
    dropdown.draw(screen)

def darken_background_image(image, opacity=150):
    darkened = image.copy()
    dark_overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, opacity))  
    darkened.blit(dark_overlay, (0, 0))  
    return darkened

def options():
    global SCREEN, current_lang
    checkboxes = create_checkboxes(current_lang)
    sliders = create_sliders(current_lang)
    dropdown = Dropdown(100, 80, ["English", "Filipino", "Bahasa Indonesia"], current_lang)
    darkened_BG = darken_background_image(BG, 125) 

    SCREEN.blit(darkened_BG, (0, 0))

    running = True
    fullscreen = False
    
    while running:
        SCREEN.blit(darkened_BG, (0, 0))
        dropdown.draw(SCREEN)
        for checkbox in checkboxes:
            checkbox.draw(SCREEN)
        for slider in sliders:
            slider.draw(SCREEN)
            
        dropdown.draw_expanded(SCREEN)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for checkbox in checkboxes:
                checkbox.handle_event(event)
                if checkbox.text_key == "Fullscreen" and event.type == pygame.MOUSEBUTTONDOWN:
                    if checkbox.checked and not fullscreen:  
                        SCREEN = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                        fullscreen = True
                    elif not checkbox.checked and fullscreen:
                        saved_values = [slider.value for slider in sliders]
                        SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                        fullscreen = False

                        darkened_BG = darken_background_image(BG, 125) 
                        sliders = create_sliders(current_lang)

                        for slider, saved_value in zip(sliders, saved_values):
                            slider.value = saved_value
                            slider.knob_rect.x = slider.x + (slider.value / slider.max_value) * slider.width - 5
                        
            for slider in sliders:
                slider.handle_event(event)

            selected_lang = dropdown.handle_event(event)
            
            
        if selected_lang:
            set_language(selected_lang)
            current_lang = selected_lang  
            checkboxes = create_checkboxes(current_lang)

            saved_values = [slider.value for slider in sliders]
            sliders = create_sliders(current_lang)
            for slider, value in zip(sliders, saved_values):
                slider.value = value
                slider.knob_rect.x = slider.x + (slider.value / slider.max_value) * slider.width - 5



if __name__ == "__main__":
    options()