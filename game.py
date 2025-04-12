import pygame
import random


# Initialize Pygame
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Acid Game Project")

# Monsters by stage
monsters_by_stage = {
    1: [("assets/4monster_1.png", "assets/4monster_2.png"),
        ("assets/5monster_1.png", "assets/5monster_2.png")],
    2: [("assets/2monster_1.png", "assets/2monster_2.png"),
        ("assets/3monster_1.png", "assets/3monster_2.png")]
}

stage3 = [
    ("assets/1monster_1.png", "assets/1monster_2.png"),
    ("assets/2monster_1.png", "assets/2monster_2.png"),
    ("assets/3monster_1.png", "assets/3monster_2.png"),
    ("assets/4monster_1.png", "assets/4monster_2.png"),
    ("assets/5monster_1.png", "assets/5monster_2.png")
]

boss_monster = ("assets/6monster_1.png", "assets/6monster_2.png")

# Classes and game logic
class Picture:
    def __init__(self, x, y, width, height, filename):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(filename)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.images = [pygame.image.load('assets/sprite_1.png'),
                       pygame.image.load('assets/sprite_2.png')]
        self.hit_image = pygame.image.load('assets/sprite_damage.png')
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.inflate_ip(-50,-30)
        self.speed = speed
        self.last_update = pygame.time.get_ticks()
        self.animation_delay = 400
        self.is_hit = False
        self.hit_timer = 0
        self.hit_duration = 1000

    def animate(self):
        if self.is_hit:
            if pygame.time.get_ticks() - self.hit_timer > self.hit_duration:
                self.is_hit = False  
            else:
                self.image = self.hit_image
                return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_delay:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.last_update = current_time

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def move(self, left, right):
        if left and self.rect.x > 0:
            self.rect.x -= self.speed
        if right and self.rect.x < width - self.rect.width:
            self.rect.x += self.speed

class Monsters(pygame.sprite.Sprite):
    def __init__(self, images, x, y):
        super().__init__()
        self.images = [pygame.image.load(img).convert_alpha() for img in images]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.bob_timer = 0

    def update(self):
        self.bob_timer += 1
        if self.bob_timer >= 30:
            self.bob_timer = 0
            self.image_index = 1 - self.image_index
            self.image = self.images[self.image_index]
        self.rect.x -= 2

def spawn_monster(stage, spawn_x, ground_y):
    if stage in monsters_by_stage:
        monster_images = random.choice(monsters_by_stage[stage])
        return Monsters(monster_images, spawn_x, ground_y)
    return None

# Game setup and initialization
bimg = pygame.image.load('assets/Background.png')
player = Player(100, 400, 10)

ph = Picture(400, 30, 60, 60, 'assets/ph_scale_14.png')
heart = Picture(40, 610, 50, 50, 'assets/heart_health1.png')
heart2 = Picture(124, 610, 50, 50, 'assets/heart_health1.png')
broken_heart = pygame.image.load('assets/heart_health_damage1.png')
player_hit = pygame.image.load('assets/sprite_damage.png')
death_sprite = pygame.image.load('assets/sprite_death.png')
font_death = pygame.font.Font("assets/font.ttf", 150)
inv = Picture(20, 0, 70, 70, 'assets/inventory.png')
help_icon = Picture(1185, 7, 1, 1, 'assets/checkboxno.png')
inventory_icons = [
    Picture(20 + i * 0.5, 0, 70, 70, f'assets/inventory_{i+1}.png') for i in range(8)
]

monster_group = pygame.sprite.Group()
spawn_timer = 0
SPAWN_DELAY = 10000
ground_y = 580
clock = pygame.time.Clock()
FPS = 60

stage = 1
monsters_spawned = 0
moving_left = False
moving_right = False

final_stage_monster_list = []

def draw_everything():
    screen.fill((0, 0, 0))
    screen.blit(bimg, (0, 0))
    player.draw()
    ph.draw()
    inv.draw()
    for icon in inventory_icons:
        icon.draw()
    heart.draw()
    heart2.draw()
    help_icon.draw()
    monster_group.draw(screen)

def stage_transition(stage_number, initial_delay=False):
    font = pygame.font.Font("assets/font.ttf", 150)
    overlay = pygame.Surface((width, height))
    overlay.fill((0, 0, 0))
    text_surface = font.render(f"Stage: {stage_number}", False, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    
    fade_speed = 10
    delay_per_step = 20
    
    for alpha in range(0, 201, fade_speed):
        pygame.event.pump()
        overlay.set_alpha(alpha)
        draw_everything()
        screen.blit(overlay, (0, 0))
        pygame.display.update()
        pygame.time.delay(delay_per_step)
        
    screen.blit(bimg, (0, 0))
    draw_everything()
    overlay.set_alpha(200)
    screen.blit(overlay, (0, 0))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)

    screen.blit(bimg, (0, 0))
    draw_everything()
    overlay.set_alpha(200)
    screen.blit(overlay, (0, 0))
    pygame.display.update()
    pygame.time.delay(300)

    for alpha in range(200, -1, -fade_speed):
        pygame.event.pump()
        overlay.set_alpha(alpha)
        screen.blit(bimg, (0, 0))
        draw_everything()
        screen.blit(overlay, (0, 0))
        pygame.display.update()
        pygame.time.delay(delay_per_step)

    if initial_delay:
        pygame.time.delay(2000)

def start_game(stage):
    # Initial stage transition
    stage_transition(stage, initial_delay=True)
    
    player_health = 2  # Initialize player health
    monsters_spawned = 0
    monster_group = pygame.sprite.Group()
    spawn_timer = 0

    # Game loop for handling gameplay
    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        draw_everything()  # Draw all game elements

        # Handle user input (movement, etc.)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(left=True, right=False)
        if keys[pygame.K_RIGHT]:
            player.move(left=False, right=True)

        # Spawn monsters periodically
        if pygame.time.get_ticks() - spawn_timer > SPAWN_DELAY:
            spawn_timer = pygame.time.get_ticks()
            monster = spawn_monster(stage, width, ground_y)
            if monster:
                monster_group.add(monster)
                monsters_spawned += 1

        # Update the monsters
        monster_group.update()

        # Check for collisions between player and monsters
        if pygame.sprite.spritecollide(player, monster_group, False):
            player.is_hit = True
            player.hit_timer = pygame.time.get_ticks()
            player_health -= 1

        # Display the health or game over if player dies
        if player_health <= 0:
            # Handle game over, e.g., display a death screen or message
            game_over_screen()
            running = False

        # Handle stage transitions
        if monsters_spawned >= 5:  # Example condition to go to the next stage
            stage += 1
            if stage > 3:  # Example condition to end the game
                game_over_screen()
                running = False
            else:
                stage_transition(stage)

        pygame.display.update()
        clock.tick(FPS)

def game_over_screen():
    # Display game over screen or death screen
    font = pygame.font.Font("assets/font.ttf", 150)
    text_surface = font.render("Game Over", False, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)