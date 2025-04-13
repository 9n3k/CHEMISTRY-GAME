import pygame
import random
import os
import sys
from acids import Acid, get_acids_for_stage, name_acid_lab1, name_acid_lab2
import json
import subprocess
import pygame
import numpy as np
from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader

pygame.init()

FULLSCREEN = False
SCREEN_SIZE = (1280, 720)

def toggle_fullscreen():
    global FULLSCREEN, SCREEN_SIZE
    FULLSCREEN = not FULLSCREEN
    if FULLSCREEN:
        screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(SCREEN_SIZE)
    return screen

def play_intro_video(video_path):
    try:
        # Initialize fresh audio context (still needed for game audio later)
        pygame.mixer.quit()
        pygame.time.delay(50)
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        
        # Create display with fullscreen capability
        screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN if FULLSCREEN else 0)
        pygame.display.set_caption("Intro Video")
        
        # Start external audio player for MP3
        audio_path = os.path.splitext(video_path)[0] + ".mp3"
        try:
            if sys.platform == "win32":
                subprocess.Popen(['start', audio_path], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(['afplay', audio_path])
            else:
                subprocess.Popen(['mpg123', audio_path])
        except Exception as e:
            print(f"Couldn't start external audio player: {e}")

        # Load video (without audio)
        try:
            video_reader = FFMPEG_VideoReader(video_path)
            print("Video loaded successfully")
        except Exception as e:
            print(f"Failed to load video: {e}")
            return False

        clock = pygame.time.Clock()
        running = True
        
        while running:
            try:
                frame = video_reader.read_frame()
                if frame is None:
                    break

                # Process video frame
                frame_rgb = frame[..., ::-1]  # BGR to RGB
                frame_rgb = np.fliplr(frame_rgb)
                frame_rgb = np.rot90(frame_rgb, k=5)
                frame_surface = pygame.surfarray.make_surface(frame_rgb)
                frame_resized = pygame.transform.scale(frame_surface, (1280, 720))
                
                # Display frame
                screen.blit(frame_resized, (0, 0))
                pygame.display.flip()
                
                # Maintain frame rate
                clock.tick(video_reader.fps)
                
                # Check for quit events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F11:
                            screen = toggle_fullscreen()
                        elif event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                            running = False
            
            except Exception as e:
                print(f"Video playback error: {e}")
                running = False

        return True
        
    except Exception as e:
        print(f"Video playback error: {e}")
        return False

def main():
    # Initialize pygame
    pygame.init()
    
    # Play video (no screen parameter needed)
    video_played = play_intro_video("assets/cutscene.mp4")
    
    if video_played:
        # Start game music
        try:
            pygame.mixer.music.load("assets/2ENDING3.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Could not load game music: {e}")
        
        # Start the game
        start_game(1)  # No screen parameter needed here either


if __name__ == "__main__":
    main()
    
def start_game(stage):
    pygame.mixer.init()
    pygame.mixer.music.load("assets/2ENDING3.mp3")  # or .ogg
    pygame.mixer.music.set_volume(0.2)  # Optional: Volume from 0.0 to 1.0
    pygame.mixer.music.play(-1)
    
    pygame.init()
    width, height = 1280, 720
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN if FULLSCREEN else 0)
    pygame.display.set_caption("Acid Game Project")

    rules_box_img = pygame.image.load("assets/box_rules.png").convert_alpha()
    rules_box_rect = rules_box_img.get_rect(center=(width // 2, height // 2))

    title_font = pygame.font.Font("assets/font.ttf", 45)
    rules_title = title_font.render("RULES", True, (255, 255, 255))
    rules_title_rect = rules_title.get_rect(midtop=(rules_box_rect.centerx, rules_box_rect.top + 120))

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
    
    monsters_by_stage[3] = stage3
    
    PRELOADED_ACIDS = {
            1: {"Ethanol": 30},
            2: {"Ethanol": 30, "H₂CO₃": 10, "[Al(H₂O)₂Cl₃(OH)]⁻": 5, "H₃PO₃": 3},
            3: {"HCl": 5, "HNO₃": 5, "H₂SO₄": 5, "H₂F⁺SbF₆⁻": 3},
    }

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
            self.rect.inflate_ip(-50, -30)
            self.speed = speed
            self.last_update = pygame.time.get_ticks()
            self.animation_delay = 400
            self.is_hit = False
            self.hit_timer = 0
            self.hit_duration = 1000

        def draw(self):
            screen.blit(self.image, self.rect.topleft)

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

        def move(self, left, right):
            if left and self.rect.x > 0:
                self.rect.x -= self.speed
            if right and self.rect.x < width - self.rect.width:
                self.rect.x += self.speed
                
        def preload_inventory(stage):
        # Load acids for the current stage
            inventory = PRELOADED_ACIDS.get(stage, {})
            acid_damage = {acid: 12 for acid in inventory}  # Default damage, you can adjust based on acid type
            return inventory, acid_damage

    class AcidProjectile(pygame.sprite.Sprite):
        def __init__(self, x, y, speed=47):
            super().__init__()
            self.image = pygame.image.load('assets/acid_shoot.png')
            self.rect = self.image.get_rect(midleft=(x, y))
            self.speed = speed
            self.hit_timer = 0
            self.kill_delay = 5

        def update(self, monster_group):
            self.rect.x += self.speed
            if self.rect.left > width:
                self.kill()
            for monster in monster_group:
                if self.rect.colliderect(monster.rect):
                    if self.hit_timer == 0:
                        self.hit_timer = pygame.time.get_ticks()
                    if pygame.time.get_ticks() - self.hit_timer >= self.kill_delay * 16:
                        monster.take_damage(1)
                        self.kill()
                    break

    class Monsters(pygame.sprite.Sprite):
        def __init__(self, images, x, y, hp):
            super().__init__()
            self.images = [pygame.image.load(img).convert_alpha() for img in images]
            self.image_index = 0
            self.image = self.images[self.image_index]
            self.rect = self.image.get_rect(midbottom=(x, y))
            self.bob_timer = 0
            self.hp = hp  # Variable HP depending on the monster type
            self.hit_number = 0
            self.hit_text = pygame.font.Font("assets/font.ttf", 30)

        def update(self):
            self.bob_timer += 1
            if self.bob_timer >= 30:
                self.bob_timer = 0
                self.image_index = 1 - self.image_index
                self.image = self.images[self.image_index]
            self.rect.x -= 5

        def take_damage(self, damage):
            self.hp -= damage
            if self.hp <= 0:
                self.kill() 
            self.hit_number += 1  

        def draw_hit_number(self):
            """Draws the hit number above the monster."""
            if self.hit_number > 0:  # Only draw if it's been hit at least once
                hit_surface = self.hit_text.render(str(self.hit_number), True, (255, 0, 0))
                hit_rect = hit_surface.get_rect(center=(self.rect.centerx, self.rect.top - 20))
                screen.blit(hit_surface, hit_rect)
    


    last_monster_images = None  # Add this outside the function (global or nonlocal)
    def spawn_monster(stage, spawn_x, ground_y):
        nonlocal last_monster_images

        # Regular monsters for Stages 1–3
        if stage == 1:
            monster_list = monsters_by_stage[1]
            monster_hp = random.randint(1, 2)
        elif stage == 2:
            monster_list = monsters_by_stage[2]
            monster_hp = random.randint(5, 6)
        elif stage == 3:
            monster_list = monsters_by_stage[3] 
            monster_hp = random.randint(7, 8)
        else:
            return None  # Invalid stage fallback

        # Random monster image (avoid repeats)
        available = [m for m in monster_list if m != last_monster_images]
        if not available:
            available = monster_list
        monster_images = random.choice(available)
        last_monster_images = monster_images

        return Monsters(monster_images, spawn_x, ground_y, monster_hp)


    def draw_everything():
        screen.fill((0, 0, 0))
        screen.blit(bimg, (0, 0))
        player.draw()
        ph.draw()
        inv.draw()
        for icon in inventory_icons:
            icon.draw()

        acid_text_rects.clear()
        font = pygame.font.Font("assets/font.ttf", 6)
        
        box_width = 58  # Width of each box
        box_height = 51   # Height of each box
        start_x = 329      # Starting X position (same as Ethanol's original position)
        start_y = 640      # Starting Y position
        
            # Draw each acid in its own box
        for i, acid in enumerate(inventory):
            # Calculate box position
           # Calculate box position
            box_x = start_x + i * (box_width + 3)  # 10 = spacing between boxes
            box_y = start_y
       
            
            # Draw the box (optional - visual representation)
            pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height), 1)
            
            # Prepare text
            text_str = f"{acid} ({inventory[acid]})"

            if font.size(text_str)[0] > box_width:
                midpoint = len(acid) // 2
                first_line = acid[:midpoint] + "-"
                second_line = acid[midpoint:] + f" ({inventory[acid]})"

                line1_surface = font.render(first_line, True, (255, 255, 255))
                line2_surface = font.render(second_line, True, (255, 255, 255))

                line1_x = box_x + (box_width - line1_surface.get_width()) // 2
                line2_x = box_x + (box_width - line2_surface.get_width()) // 2
                line1_y = box_y + 5
                line2_y = box_y + box_height // 2

                screen.blit(line1_surface, (line1_x, line1_y))
                screen.blit(line2_surface, (line2_x, line2_y))
            else:
                acid_name_surface = font.render(text_str, True, (255, 255, 255))
                text_x = box_x + (box_width - acid_name_surface.get_width()) // 2
                text_y = box_y + (box_height - acid_name_surface.get_height()) // 2
                screen.blit(acid_name_surface, (text_x, text_y))

            # Store collision rectangle (using the box dimensions)
            acid_text_rects[acid] = pygame.Rect(box_x, box_y, box_width, box_height)

            heart.draw()
            heart2.draw()
            help_icon.draw()
            question_text = font_help.render("?", True, (255, 255, 255))
            question_rect = question_text.get_rect(center=help_icon.rect.center)
            question_rect.y += 1
            screen.blit(question_text, question_rect)
            monster_group.draw(screen)
            for monster in monster_group:
                monster.update()
                monster.draw_hit_number()

            if show_rules:
                screen.blit(rules_box_img, rules_box_rect)
                screen.blit(rules_title, rules_title_rect)
                rule_surfaces = [rules_font.render(line, True, (255, 255, 255)) for line in rules_list]
                total_height = len(rule_surfaces) * 35
                start_y = rules_box_rect.centery - total_height // 2
                for i, surface in enumerate(rule_surfaces):
                    surface_rect = surface.get_rect(center=(rules_box_rect.centerx, start_y + i * 35))
                    screen.blit(surface, surface_rect)
                


    def stage_transition(stage_number, initial_delay=False):
        font = pygame.font.Font("assets/font.ttf", 150)
        overlay = pygame.Surface((width, height))
        overlay.fill((0, 0, 0))
        text_surface = font.render(f"Stage: {stage_number}", False, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        fade_speed = 10
        delay_per_step = 20
        if stage_number == 2:
            inventory.clear()  # Clear the old inventory
            inventory["Ethanol"] = 30
            inventory["H2CO3"] = 120
            inventory["[Al(H2O)2Cl3(OH)]-"] = 20
            inventory["H3PO3"] = 50
            acid_damage["Ethanol"] = 12
            acid_damage["H2CO3"] = 8  # Example damage value
            acid_damage["[Al(H2O)2Cl3(OH)]-"] = 10
            acid_damage["H3PO3"] = 6
        elif stage_number == 3:
            inventory.clear()  # Clear the old inventory
            inventory["HCl"] = 20
            inventory["HNO3"] = 610
            inventory["H2SO4"] = 200
            inventory["H2F+SbF6-"] = 6
            acid_damage["HCl"] = 15  # Example damage value
            acid_damage["HNO3"] = 12
            acid_damage["H2SO4"] = 12
            acid_damage["H2F+SbF6-"] = 12

        for alpha in range(0, 215, fade_speed):
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

    def reset_game():
        nonlocal player, player_health, death_triggered, spawn_timer, stage
        nonlocal monsters_spawned, final_stage_monster_list
        nonlocal inventory, acid_damage, selected_acid
        player = Player(100, 400, 15)
        heart.image = pygame.image.load('assets/heart_health1.png')
        heart2.image = pygame.image.load('assets/heart_health1.png')
        player_health = 2
        death_triggered = False
        spawn_timer = SPAWN_DELAY
        stage = 1
        monsters_spawned = 0
        final_stage_monster_list = []
        monster_group.empty()
        inventory = {"Ethanol": 95}
        acid_damage = {"Ethanol": 12}
        selected_acid = "Ethanol"
        stage_transition(stage, initial_delay=True)

    bimg = pygame.image.load('assets/background.png')
    player = Player(100, 400, 10)
    ph = Picture(400, 30, 60, 60, 'assets/ph_scale_14.png')
    heart = Picture(40, 610, 50, 50, 'assets/heart_health1.png')
    heart2 = Picture(124, 610, 50, 50, 'assets/heart_health1.png')
    broken_heart = pygame.image.load('assets/heart_health_damage1.png')
    death_sprite = pygame.image.load('assets/sprite_death.png')
    font_death = pygame.font.Font("assets/font.ttf", 150)
    inv = Picture(20, 0, 70, 70, 'assets/inventory.png')
    help_icon = Picture(1185, 7, 100, 100, 'assets/checkboxno.png')
    show_rules = False
    font_help = pygame.font.Font('assets/font.ttf', help_icon.rect.height - 70)
    inventory_icons = [
        Picture(20 + i * 0.5, 0, 70, 70, f'assets/inventory_{i+1}.png') for i in range(8)
    ]
    rules_font = pygame.font.Font('assets/font.ttf', 9)
    rules_list = [
     "- CLICK! CLICK! CLICK!",
     "- Create acids in the lab to learn about their strength and properties",
     "- Stronger acids have lower pH and are more effective in theory", 
     "- Use what you've learned to face the monsters in battle"
]

    clock = pygame.time.Clock()
    FPS = 60
    spawn_timer = 0
    SPAWN_DELAY = 100
    ground_y = 580
    monster_group = pygame.sprite.Group()
    acid_projectiles = pygame.sprite.Group()

    inventory = {}
    acid_damage = {}
    acid_text_rects = {}
    selected_acid = None
    if stage == 1:
        inventory["Ethanol"] = 95
        acid_damage["Ethanol"] = 12
        selected_acid = "Ethanol"

    monsters_spawned = 0
    moving_left = False
    moving_right = False
    final_stage_monster_list = []
    player_health = 2
    death_triggered = False
    stage_transition(stage)
    running = True
    death_timer = 0
    
    lab2_launched = False

    while running:
        dt = clock.tick(FPS)
        spawn_timer += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen = toggle_fullscreen()
                elif event.key == pygame.K_LEFT:  # Moved this under the same KEYDOWN check
                    moving_left = True
                elif event.key == pygame.K_RIGHT:
                    moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                elif event.key == pygame.K_RIGHT:
                    moving_right = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if help_icon.rect.collidepoint(event.pos):
                    show_rules = not show_rules
                else:
                    for acid, rect in acid_text_rects.items():
                        if rect.collidepoint(event.pos):
                            selected_acid = acid
                            if inventory.get(acid,0) > 0:
                                acid_projectile = AcidProjectile(player.rect.centerx, player.rect.centery)
                                acid_projectiles.add(acid_projectile)
                                inventory[acid] -= 1
                                if inventory[acid] <= 0:
                                    del inventory[acid]
                                    if acid in acid_damage:
                                        del acid_damage[acid]
                            break

        player.move(moving_left, moving_right)
        player.animate()
        acid_projectiles.update(monster_group)

        # Stage transition logic
        if player.rect.x >= width - player.rect.width:
            stage += 1
            player.rect.x = 0
            monsters_spawned = 0
            spawn_timer = 0
            monster_group.empty()
            final_stage_monster_list = []
            stage_transition(stage, initial_delay=True)
            
            # Stage-specific initialization
            import subprocess
            if stage == 2:
                with open("inventory.json", "w") as f:
                    json.dump(inventory, f)
                subprocess.run(["python", "lab.py"])
            elif stage == 3:
                if not lab2_launched:
                    subprocess.run(["python", "lab2.py"])
                    lab2_launched = True
            
            # Update selected acid
            selected_acid = next(iter(inventory), None)
            
        monsters_to_spawn_for_stage = {
            1: 60,
            2: 7,
            3: 5,
        }

        # Monster spawning logic
        if stage in [1, 2]:
            if spawn_timer >= SPAWN_DELAY and monsters_spawned < monsters_to_spawn_for_stage[stage]:
                new_monster = spawn_monster(stage, 1300, ground_y)
                if new_monster:
                    monster_group.add(new_monster)
                    monsters_spawned += 1
                    spawn_timer = 0
        if stage == 3:
            # Spawn monsters if not all have been spawned yet
            if spawn_timer >= SPAWN_DELAY and monsters_spawned < monsters_to_spawn_for_stage[stage]:
                monster = spawn_monster(stage, width + 100, ground_y)
                monster_group.add(monster)
                monsters_spawned += 1
                spawn_timer = 0  # Reset spawn timer after spawn

            # Check for win condition: all monsters spawned AND all defeated
            if monsters_spawned >= monsters_to_spawn_for_stage[stage] and not monster_group:
                pygame.time.delay(1000)
                font = pygame.font.Font("assets/font.ttf", 100)
                text = font.render("YOU WIN!", True, (0, 255, 0))
                text_rect = text.get_rect(center=(width // 2, height // 2))
                screen.blit(text, text_rect)
                pygame.display.update()
                pygame.time.delay(3000)
                pygame.quit()
                
                try:
                    subprocess.run(["python", "3rdENDING.py"], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running 3rdENDING.py: {e}")

                sys.exit()
                

        monster_group.update()
        if not death_triggered:
            def tighter_collision(sprite1, sprite2):
                return sprite1.rect.colliderect(sprite2.rect.inflate(-30, -30))

            collided = pygame.sprite.spritecollide(player, monster_group, False, collided=tighter_collision)
            if collided:
                if player_health == 2:
                    heart2.image = broken_heart
                    player_health -= 1
                    player.is_hit = True
                    player.hit_timer = pygame.time.get_ticks()
                elif player_health == 1:
                    heart.image = broken_heart
                    player_health -= 1
                    player.is_hit = True
                    player.hit_timer = pygame.time.get_ticks()
                elif player_health == 0:
                    death_triggered = True
                    death_timer = pygame.time.get_ticks()

        draw_everything()
        acid_projectiles.draw(screen)
        if death_triggered:
            screen.fill((0, 0, 0))
            screen.blit(death_sprite, player.rect.topleft)
            death_text = font_death.render("YOU DIED", True, (255, 0, 0))
            death_rect = death_text.get_rect(center=(width // 2, height // 2))
            screen.blit(death_text, death_rect)
            if pygame.time.get_ticks() - death_timer > 3000:
                reset_game()
            pygame.display.update()
        else:
            pygame.display.update()

    pygame.quit()
if __name__ == "__main__":
    start_game(1)