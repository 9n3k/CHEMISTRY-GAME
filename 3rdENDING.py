import pygame
import sys
import os
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/1ENDING3.mp3")  
pygame.mixer.music.set_volume(0.02) 
pygame.mixer.music.play(-1)  

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("???")
clock = pygame.time.Clock()


bg_color = (10, 10, 10)
dialogue_color = (30, 30, 30)
dialogue_border = (255, 255, 255)


font_path = "assets/font.ttf"
dialogue_font = pygame.font.Font(font_path, 28)
question_font = pygame.font.Font(font_path, 20)
answer_font = pygame.font.Font(font_path, 22)

boss_frame1 = pygame.image.load("assets/6monster_1.png").convert_alpha()
boss_frame2 = pygame.image.load("assets/6monster_2.png").convert_alpha()
boss_frame1 = pygame.transform.scale(boss_frame1, (250, 250))
boss_frame2 = pygame.transform.scale(boss_frame2, (250, 250))

boss_frames = [boss_frame1, boss_frame2]
current_boss_frame = 0
animation_timer = pygame.time.get_ticks()
animation_interval = 500  #miliseconds


boss_rect = boss_frames[0].get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))


dialogue_box_rect = pygame.Rect(100, HEIGHT - 200, WIDTH - 200, 130)
dialogue_lines = [
    "You may have defeated me...",
    "But your knowledge... must be tested.",
    "Prepare for the final challenge!"
]
dialogue_index = 0
next_line_delay = 2300
last_dialogue_time = pygame.time.get_ticks()

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

selected_answer_index = -1
show_feedback = False
feedback_dialogue = []
feedback_index = 0
feedback_start_time = 0
feedback_delay = 2000


question_active = False
questions = [
    {
        "question": "Q: Which of the following elements forms an oxide that can be used to neutralize an alkaline solution?",
        "answers": ["A) Nitrogen", "B) Magnesium", "C) Iron", "D) Helium"],
        "correct": 0,
        "correct_feedback": ["Correct!", "Your knowledge is strong...", "Or is it?"],
        "wrong_feedback": ["Hey hey hey...", "sometimes it's just a skill issue"]
    },
    {
        "question": "Q: Which equation does not show the correct reaction of an acid?",
        "answers": ["A) CuO + 2HCL -> CuCl2 + H2O", "B) CaCO3 + HNO3 -> CaNO3 + CO2 + H2O", "C) 2KOH + H2SO4 -> K2SO4 + 2H2O", "D) Zn + H2SO4 -> ZnSO4 + H2"],
        "correct": 1,
        "correct_feedback": ["Impressive!", "You know your chemistry!"],
        "wrong_feedback": ["Wrong!", "Even basic chemistry eludes you?"]
    },
    {
        "question": "Q: Which of these compounds is amphoteric?",
        "answers": ["A) Copper(II) sulfate", "B) Zinc oxide ", "C) Sodium Chloride", "D) Magnesium hydroxide"],
        "correct": 1,
        "correct_feedback": ["Good to know you know."],
        "wrong_feedback": ["That much confidence?"]
    },
    {
        "question": "Q: What does hydrochloric acid do when it reacts with zinc?",
        "answers": ["A) Forms a pale blue precipitate", "B) Produces white precipitate with barium nitrate", "C) Releases ammonia from ammonium salts", "D) Produces hydrogen gas"],
        "correct": 3,
        "correct_feedback": ["Yaya...", "very easy right?"],
        "wrong_feedback": ["You people really are simple-minded..."]
    },
    {
        "question": "Q: How does the pH of HCl change as excess aqueous barium hydroxide is added?",
        "answers": ["A) pH drops from 14 to 7", "B) pH drops from 14 to 1", "C) pH rises from 1 to 7", "D) pH rises from 1 to 14"],
        "correct": 2,
        "correct_feedback": ["So what if you got correct?", "anyone can...", "even Dennis," "King of Chemistry..."],
        "wrong_feedback": ["Could you be more intelligent?"]
    },
    {
    "question": "Q: The oxide Pb3O4 reacts with dilute nitric acid to form lead(II) nitrate, lead(IV) oxide, and another product. What is the equation for this reaction?",
    "answers": [
        "A) Pb3O4 + 4HNO3 → 2Pb(NO3)2 + PbO2 + 2H2O",
        "B) Pb3O4 + 2HNO3 → 2PbNO3 + PbO4 + H2",
        "C) Pb3O4 + 4HNO3 → Pb(NO3)4 + 2PbO + 2H2O"
    ],
    "correct": 0,
    "correct_feedback": ["Alright alright..."],
    "wrong_feedback": ["What would've Ms Kate say...?"]
    },
    {
    "question": "Q: Which reaction of acids is correct?",
    "answers": [
        "A) With ammonium salts → salt + ammonia",
        "B) With carbonates → salt + CO2",
        "C) With hydroxides → salt + water",
        "D) With metals → salt + hydrogen + water"
    ],
    "correct": 2,
    "correct_feedback": ["Amaetur question...", "Indeed you are worthy to live...", "Or are you?"],
    "wrong_feedback": ["ARE YOU SERIOUS?!?!", "I might feel bad for you", "MIGHT"]
    },
    {
    "question": "Q: Who is considered the king of chemistry?",
    "answers": [
        "A) Dennis",
        "B) JOMARVELL",
        "C) IZAAC",
        "D) You"
    ],
    "correct": 0,
    "correct_feedback": ["Exactly! No one beats him"],
    "wrong_feedback": ["Be more confident ya know?"]
    },
    {
    "question": "Q: What colour does acids become in Thymolphthalein?",
    "answers": [
        "A) Red",
        "B) Colourless",
        "C) Yellow",
        "D) Blue"
    ],
    "correct": 1,
    "correct_feedback": ["Exactly! No one beats him"],
    "wrong_feedback": ["Be more confident ya know?"]
    },
    {
    "question": "Q: How are Acids used in daily life?",
    "answers": [
        "A) Adjusts Ph levels in swimming videos",
        "B) Make things sweeter",
        "C) Adjust saltiness in food",
        "D) Enchance the flavor of foods by adding tartness"
    ],
    "correct": 0,
    "correct_feedback": ["Exactly! No one beats him"],
    "wrong_feedback": ["Be more confident ya know?"]
    },
    {
    "question": "Q: Did you win?",
    "answers": [
        "A) No",
        "B) No",
        "C) No",
        "D) No"
    ],
    "correct": 0,
    "correct_feedback": ["THIS WAS SUCH...", "A LONG TIME TO MAKE...", "HOWEVER," "YOU MY FRIEND DID WELL...", "GOODBYE"],
    "wrong_feedback": ["ajsdnkajsdn9823r09u2jds!@# ERROR--[[G9FBA98-REACT1ON_F41L3D]bloopblop∆∆∆ SYSTEM OV3RLOAD"]
    },
]
prank_mode = False
prank_timer = 0
glitch_flash = False
glitch_interval = 200
last_glitch_time = 0
current_question_index = 0
wrapped_question_lines = wrap_text(questions[current_question_index]["question"], question_font, 800)
current_answers = questions[current_question_index]["answers"]
correct_answer_index = questions[current_question_index]["correct"]
answer_surfaces = [answer_font.render(ans, True, (200, 200, 200)) for ans in current_answers]


running = True
while running:
    
    question_phase_done = False
    
    screen.fill(bg_color)

   
    now = pygame.time.get_ticks()
    if now - animation_timer > animation_interval:
        current_boss_frame = (current_boss_frame + 1) % len(boss_frames)
        animation_timer = now

    screen.blit(boss_frames[current_boss_frame], boss_rect)

    if not question_active:
        pygame.draw.rect(screen, dialogue_color, dialogue_box_rect)
        pygame.draw.rect(screen, dialogue_border, dialogue_box_rect, 3)

        if not question_active:
            current_text = dialogue_font.render(dialogue_lines[dialogue_index], True, (255, 255, 255))
            screen.blit(current_text, (dialogue_box_rect.x + 20, dialogue_box_rect.y + 40))

        if pygame.time.get_ticks() - last_dialogue_time > next_line_delay:
            if dialogue_index < len(dialogue_lines) - 1:
                dialogue_index += 1
                last_dialogue_time = pygame.time.get_ticks()
            else:
                question_active = True

    elif question_active and not show_feedback and selected_answer_index == -1:
        # Draw the question and answers
        line_height = 30
        answer_height = 40
        block_width = 700  
        total_question_height = len(wrapped_question_lines) * line_height
        total_answer_height = len(answer_surfaces) * answer_height
        total_block_height = total_question_height + total_answer_height + 20

        start_y = HEIGHT // 2 - total_block_height // 2 + 130
        start_x = WIDTH // 2 - block_width // 2

        for i, line in enumerate(wrapped_question_lines):
            line_surface = question_font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (start_x, start_y + i * line_height))

        answer_y_start = start_y + total_question_height + 20
        for i, ans_surface in enumerate(answer_surfaces):
            ans_x = WIDTH // 2 - ans_surface.get_width() // 2
            ans_y = answer_y_start + i * answer_height
            screen.blit(ans_surface, (ans_x, ans_y))

    elif show_feedback:
        pygame.draw.rect(screen, dialogue_color, dialogue_box_rect)
        pygame.draw.rect(screen, dialogue_border, dialogue_box_rect, 3)

        current_feedback = dialogue_font.render(feedback_dialogue[feedback_index], True, (255, 255, 255))
        screen.blit(current_feedback, (dialogue_box_rect.x + 20, dialogue_box_rect.y + 40))

        if now - feedback_start_time > feedback_delay:
            if feedback_index < len(feedback_dialogue) - 1:
                feedback_index += 1
                feedback_start_time = now
            else:
                show_feedback = False
                question_phase_done = True

                current_question_index += 1  
                if current_question_index < len(questions):
                    wrapped_question_lines = wrap_text(questions[current_question_index]["question"], question_font, 800)
                    current_answers = questions[current_question_index]["answers"]
                    correct_answer_index = questions[current_question_index]["correct"]
                    answer_surfaces = [answer_font.render(ans, True, (200, 200, 200)) for ans in current_answers]

                    selected_answer_index = -1
                    question_active = True
                else:
                    pygame.quit()
                    os.system("python creditroll.py")
                    sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and question_active and not show_feedback:
            mouse_x, mouse_y = event.pos
            for i, ans_surface in enumerate(answer_surfaces):
                ans_x = WIDTH // 2 - ans_surface.get_width() // 2
                ans_y = answer_y_start + i * answer_height
                ans_rect = pygame.Rect(ans_x, ans_y, ans_surface.get_width(), ans_surface.get_height())
                if ans_rect.collidepoint(mouse_x, mouse_y):
                    selected_answer_index = i
                    feedback_index = 0
                    feedback_start_time = pygame.time.get_ticks()

                    # Prepare the feedback BEFORE showing it next frame SO HTAT IT WORKS FOR ALL NOT JST MANUALLY 1 By  1
                    if i == questions[current_question_index]["correct"]:
                        feedback_dialogue = questions[current_question_index]["correct_feedback"]
                    else:
                        feedback_dialogue = questions[current_question_index]["wrong_feedback"]


                    show_feedback = True
                    

    pygame.display.flip()
    clock.tick(60)

