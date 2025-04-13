import pygame
import sys
from pygame.locals import *
from inventory import inventory, MAX_CHEMICAL_LIMIT
import tkinter as tk
from tkinter import messagebox, simpledialog
# Initialize pygame
pygame.init()

icon = pygame.image.load("assets/ICON.png")
# ----------------------------
# Screen Setup
# ----------------------------
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chemistry Reaction Game')

# ----------------------------
# Load and setup background image
# ----------------------------
try:
    background_image = pygame.image.load("lab assets/background.PNG").convert()
except Exception as e:
    print("Error loading background.PNG:", e)
    background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image.fill((200, 200, 200))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# ----------------------------
# Load images for other assets (if needed)
# ----------------------------
try:
    chem_panel_bg = pygame.image.load(" lab assets/box_rules.png").convert_alpha()
except Exception as e:
    print("box_rules.png:", e)
    chem_panel_bg = None

# ----------------------------
# Fonts Setup
# ----------------------------
font_path = "lab assets/font.ttf"
try:
    font = pygame.font.Font(font_path, 9)
    hover_font = pygame.font.Font(font_path, 11)
    title_font = pygame.font.Font(font_path, 20)
    chemical_font = pygame.font.Font(font_path, 8)
    guide_font = pygame.font.Font(font_path, 9)
    CaOh_font = pygame.font.Font(font_path, 9)
except Exception as e:
    print("Error loading font.ttf:", e)
    font = pygame.font.SysFont("Arial", 14)
    hover_font = pygame.font.SysFont("Arial", 11)
    title_font = pygame.font.SysFont("Arial", 24)
    chemical_font = pygame.font.SysFont("Arial", 13)
    guide_font = pygame.font.SysFont("Arial", 14)
    CaOh_font = pygame.font.SysFont("Arial", 9)

# ----------------------------
# Colors
# ----------------------------
WHITE        = (255, 255, 255)
BLACK        = (0, 0, 0)
GREY         = (200, 200, 200)
LIGHT_GREY   = (230, 230, 230)
LIGHT_BLUE   = (230, 247, 255)
RED          = (255, 70, 70)
BLUE         = (70, 130, 230)
GREEN        = (70, 200, 70)
YELLOW       = (255, 255, 0)
ORANGE       = (255, 165, 0)
PURPLE       = (128, 0, 128)
GRAY_ZINC    = (170, 170, 170)
LIGHT_YELLOW = (230, 255, 150)
LIGHT_ORANGE = (255, 200, 150)

# ----------------------------
# Chemicals definition 
# ----------------------------
chemicals = [
    {"name": "CH3CH2O-", "type": "base",    "color": BLUE, "description": "Ethoxide ion reacts with water to form ethanol + OH⁻.", "uses": 5},
    {"name": "PCl3",    "type": "acid",    "color": RED, "description": "Phosphorus Trichloride reacts with water to produce Phosphorus Acid.", "uses": 5},
    {"name": "AlCl3",   "type": "acid",    "color": RED,  "description": "Aluminum chloride hydrolyzes with water forming a complex + H⁺.", "uses": 5},
    {"name": "CH3COO-", "type": "base",    "color": BLUE, "description": "Acetate ion -- reaction in this demo is unknown.", "uses": 5},
    {"name": "CO2",     "type": "gas",     "color": LIGHT_GREY, "description": "CO₂ reacts with water forming carbonic acid.", "uses": 5},
    {"name": "H2O",     "type": "water",   "color": LIGHT_BLUE, "description": "Water -- essential reactant.", "uses": 7},
    {"name": "H+",      "type": "aqueous", "color": LIGHT_BLUE, "description": "Hydrogen ion produced in some reactions.", "uses": 5},
]

# ----------------------------
# Utility Functions
# ----------------------------
def get_reaction_products(chem1, chem2):
    """
    Returns a list of product chemicals (as dictionaries) for a matching reaction.
    Reaction equations (order-independent):
      • CH3CH2O- + H2O → CH3CH2OH + OH-
      • PCl3 + 3H2O → H3PO4 + 3HCl
      • CO2 + H2O ⇌ H2CO3
      • AlCl3 + H2O → [Al(H2O)2Cl3(OH)]- + H+
    """
    names = {chem1["name"], chem2["name"]}
    if names == {"CH3CH2O-", "H2O"}:
        product1 = {"name": "CH3CH2OH", "type": "alcohol", "color": GREEN, "description": "Ethanol produced.", "uses": None}
        product2 = {"name": "OH-", "type": "base", "color": PURPLE, "description": "Hydroxide ion produced.", "uses": None}
        return [product1, product2]
    elif names == {"PCl3", "H2O"}:
        product = {"name": "H3PO4", "type": "acid", "color": RED, "description": "Phosphorus Acid produced.", "uses": None}
        return [product]
    elif names == {"CO2", "H2O"}:
        product = {"name": "H2CO3", "type": "acid", "color": ORANGE, "description": "Carbonic acid produced.", "uses": None}
        return [product]
    elif names == {"AlCl3", "H2O"}:
        product1 = {"name": "[Al(H2O)2Cl3(OH)]-", "type": "complex", "color": GRAY_ZINC, "description": "Complex from AlCl3 hydrolysis.", "uses": None}
        product2 = {"name": "H+", "type": "aqueous", "color": LIGHT_BLUE, "description": "Hydrogen ion produced.", "uses": None}
        return [product1, product2]
    return []

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines

def get_ph_strip_color(chem):
    """
    Determine the pH strip color based on the chemical dropped.
    Mapping:
      - Ethanol ("CH3CH2OH"): Green (neutral)
      - Carbonic Acid ("H2CO3"): Orange (acidic)
      - Aqueous Aluminium Chloride ("[Al(H2O)2Cl3(OH)]-"): Yellow (slightly acidic)
      - Phosphoric Acid ("H3PO4"): Red (strongly acidic)
      - Otherwise: fallback based on chemical type.
    """
    if chem["name"] == "CH3CH2OH":
        return YELLOW
    elif chem["name"] == "H2CO3":
        return LIGHT_ORANGE
    elif chem["name"] == "[Al(H2O)2Cl3(OH)]-":
        return LIGHT_ORANGE
    elif chem["name"] == "H3PO4":
        return ORANGE
    else:
        if chem["type"] == "acid":
            return RED
        elif chem["type"] == "base":
            return LIGHT_BLUE
        elif chem["type"] == "water":
            return LIGHT_YELLOW
        else:
            return GREY
        

panel_width, panel_height = 500, 220
chemical_panel_rect = pygame.Rect((SCREEN_WIDTH - panel_width) // 2, 80, panel_width, panel_height)

reaction_area_rect = pygame.Rect((SCREEN_WIDTH - 740) // 2, 320, 740, 160)

result_box_rect = pygame.Rect((SCREEN_WIDTH - 700) // 2, 560, 700, 100)
product_area_rect = pygame.Rect(result_box_rect.x + 20, result_box_rect.y + result_box_rect.height - 90,
                                result_box_rect.width - 40, 40)

inventory_area_rect = pygame.Rect(SCREEN_WIDTH - 380, 100, 360, 200)

guide_panel_rect = pygame.Rect(10, 120, 280, 150)

trash_area_rect = pygame.Rect(SCREEN_WIDTH - 110, (SCREEN_HEIGHT - 100) // 2, 100, 100)

ph_strip_rect = pygame.Rect(10, 350, 140, 50)
ph_strip_color = LIGHT_YELLOW  # default color
ph_strip_chem = None  # holds chemical stored in the PH strip

exit_button_rect = pygame.Rect(SCREEN_WIDTH - 70, 10, 60, 30)

scroll_offset = 0
cols = 5
spacing_y = 90
padding_x = 20

placed_chems = []      # reactants in Reaction Area
product_items = []     # products created in the Result Box
free_items = []        # items dropped on board freely
inventory_items = []   # items stored in inventory (max 10)
dragging_chem = None   # currently dragged item

no_reaction = False

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(background_image, (0, 0))
    
    if ph_strip_chem is not None:
        if ph_strip_chem["name"] == "CH3CH2OH":
            pH_str = "7.3"
        elif ph_strip_chem["name"] == "H2CO3":
            pH_str = "4.7"
        elif ph_strip_chem["name"] == "[Al(H2O)2Cl3(OH)]-":
            pH_str = "2.5"
        elif ph_strip_chem["name"] == "H3PO4":
            pH_str = "2.5"
        else:
            if ph_strip_chem["type"] == "acid":
                pH_str = "-.-"
            elif ph_strip_chem["type"] == "base":
                pH_str = "-.-"
            elif ph_strip_chem["type"] == "water":
                pH_str = "7.0"
            else:
                pH_str = "-.-"
    else:
        pH_str = "--"
    ph_number_text = title_font.render("pH: " + pH_str, True, WHITE)
    ph_number_rect = ph_number_text.get_rect(midbottom=(ph_strip_rect.centerx, ph_strip_rect.y - 5))
    screen.blit(ph_number_text, ph_number_rect)
    
    # ----------------------------
    # PH Strip
    # ----------------------------
    pygame.draw.rect(screen, ph_strip_color, ph_strip_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, ph_strip_rect, 2, border_radius=10)
    ph_strip_label = title_font.render("PH", True, BLACK)
    ph_strip_label_rect = ph_strip_label.get_rect(center=(ph_strip_rect.centerx, ph_strip_rect.centery))
    screen.blit(ph_strip_label, ph_strip_label_rect)
    if ph_strip_chem is not None:
        chem_text = chemical_font.render(ph_strip_chem["name"], True, BLACK)
        chem_text_rect = chem_text.get_rect(center=(ph_strip_rect.centerx, ph_strip_rect.centery + 25))
        screen.blit(chem_text, chem_text_rect)
    
    # ----------------------------
    # Exit Button
    # ----------------------------
    pygame.draw.rect(screen, LIGHT_GREY, exit_button_rect, border_radius=5)
    pygame.draw.rect(screen, BLACK, exit_button_rect, 2, border_radius=5)
    exit_text = font.render("Exit", True, BLACK)
    exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
    screen.blit(exit_text, exit_text_rect)
    
    guide_title = title_font.render("Reactions", True, BLACK)
    screen.blit(guide_title, (guide_panel_rect.x + 20, guide_panel_rect.y + 2))
    reactions_text = [
        "Ethoxide + H2O → ethanol + OH-",
        "Phosphorus + H2O → Phosphorus acid",
        "Carbon dioxide + H2O → carbonic acid",
        "Aluminium Chloride + H2O →",
        "Hydrated Aluminium chloride"
    ]
    for i, line in enumerate(reactions_text):
        txt = guide_font.render(line, True, BLACK)
        screen.blit(txt, (guide_panel_rect.x + 15, guide_panel_rect.y + 30 + i * 20))
    
    inv_label = title_font.render("Inventory", True, WHITE)
    screen.blit(inv_label, (inventory_area_rect.x + 10, inventory_area_rect.y - 10))
    
    trash_label = title_font.render("Trash", True, BLACK)
    trash_label_rect = trash_label.get_rect(center=trash_area_rect.center)
    screen.blit(trash_label, trash_label_rect)
    
    reaction_label = title_font.render("Reaction Area", True, BLACK)
    screen.blit(reaction_label, (reaction_area_rect.x + 35, reaction_area_rect.y - 2))
    
    result_label = title_font.render("Result", True, BLACK)
    screen.blit(result_label, (result_box_rect.x + 25, result_box_rect.y - 10))
    if no_reaction and not product_items:
        no_rxn_text = title_font.render("No reaction", True, BLACK)
        no_rxn_rect = no_rxn_text.get_rect(center=(product_area_rect.centerx, product_area_rect.centery))
        screen.blit(no_rxn_text, no_rxn_rect)
        
    def run_lab():
        global inventory  # Ensure the inventory is accessible
        
        # List of chemicals that will be added after completing the lab
        new_chemicals = [
            'CH3CH2OH',  # Stage 1 chemicals
            'H2CO3',     # Stage 2 chemicals
            '[Al(H2O)2Cl3(OH)]⁻',
            'H3PO3',
            'HCl',       # Stage 3 chemicals
            'HNO3',
            'H2SO4',
            'H2F+SbF6'
        ]
        
        # Add chemicals to the inventory, ensuring the count does not exceed the max limit
        for chem in new_chemicals:
            if inventory[chem] < MAX_CHEMICAL_LIMIT:
                inventory[chem] += 1  # Increment the chemical count
            else:
                print(f"Cannot add more {chem}, limit reached!")

        # After adding chemicals, you could proceed with other logic like transitioning to the next stage
        print("Lab completed, chemicals added to inventory.")
        
    # ----------------------------
    # Draw inventory items 
    # ----------------------------
    inv_icon_size = 60  
    inv_padding = 10
    icons_per_row = (inventory_area_rect.width - 2 * inv_padding) // (inv_icon_size + 5)
    for idx, chem in enumerate(inventory_items):
        col = idx % icons_per_row
        row = idx // icons_per_row
        icon_x = inventory_area_rect.x + inv_padding + (inv_icon_size + 5) * col
        icon_y = inventory_area_rect.y + inv_padding + (inv_icon_size + 5) * row
        icon_rect = pygame.Rect(icon_x, icon_y, inv_icon_size, inv_icon_size)
        pygame.draw.rect(screen, chem["color"], icon_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, icon_rect, 1, border_radius=10)
        text = chemical_font.render(chem["name"], True, BLACK)
        text_rect = text.get_rect(center=icon_rect.center)
        screen.blit(text, text_rect)
    
    screen.set_clip(chemical_panel_rect)
    cell_width = (chemical_panel_rect.width - padding_x * 2) // cols
    total_rows = (len(chemicals) - 1) // cols + 1
    total_chem_height = total_rows * spacing_y
    avail_height = chemical_panel_rect.height
    padding_y = max((avail_height - total_chem_height) // 2, 10)
    panel_chem_rects = []
    for i, chem in enumerate(chemicals):
        row_idx = i // cols
        col_idx = i % cols
        x = chemical_panel_rect.x + padding_x + col_idx * cell_width + (cell_width - 70) // 2
        extra_top = 10
        y = chemical_panel_rect.y + padding_y + extra_top + row_idx * spacing_y + scroll_offset
        rect = pygame.Rect(x, y, 70, 70)
        panel_chem_rects.append(rect)
        # Draw the chemical rectangle
        if chem["uses"] > 0:
            pygame.draw.rect(screen, chem["color"], rect, border_radius=10)
        else:
            greyed = tuple(min(255, c + 100) for c in chem["color"])
            pygame.draw.rect(screen, greyed, rect, border_radius=10)
            overlay = pygame.Surface((70, 70))
            overlay.set_alpha(150)
            overlay.fill((200, 200, 200))
            screen.blit(overlay, rect.topleft)
        pygame.draw.rect(screen, BLACK, rect, 1, border_radius=10)
        text = chemical_font.render(chem["name"], True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        uses_text = hover_font.render(str(chem["uses"]), True, BLACK)
        use_rect = uses_text.get_rect(bottomright=(rect.right - 2, rect.bottom - 2))
        screen.blit(uses_text, use_rect)
    screen.set_clip(None)
    
    if total_chem_height > chemical_panel_rect.height:
        scrollbar_height = max(int(chemical_panel_rect.height * (chemical_panel_rect.height / total_chem_height)), 20)
        scroll_ratio = -scroll_offset / (total_chem_height - chemical_panel_rect.height)
        scrollbar_y = chemical_panel_rect.y + scroll_ratio * (chemical_panel_rect.height - scrollbar_height)
        scrollbar_rect = pygame.Rect(chemical_panel_rect.right - 10, scrollbar_y, 6, scrollbar_height)
        pygame.draw.rect(screen, LIGHT_GREY, scrollbar_rect, border_radius=3)
    
    for item in placed_chems:
        pygame.draw.rect(screen, item["chemical"]["color"], item["rect"], border_radius=10)
        pygame.draw.rect(screen, BLACK, item["rect"], 1, border_radius=10)
        text = chemical_font.render(item["chemical"]["name"], True, BLACK)
        text_rect = text.get_rect(center=item["rect"].center)
        screen.blit(text, text_rect)
    
    for item in free_items:
        pygame.draw.rect(screen, item["chemical"]["color"], item["rect"], border_radius=10)
        pygame.draw.rect(screen, BLACK, item["rect"], 1, border_radius=10)
        text = chemical_font.render(item["chemical"]["name"], True, BLACK)
        text_rect = text.get_rect(center=item["rect"].center)
        screen.blit(text, text_rect)
    
    for item in product_items:
        pygame.draw.rect(screen, item["chemical"]["color"], item["rect"], border_radius=10)
        pygame.draw.rect(screen, BLACK, item["rect"], 1, border_radius=10)
        text = chemical_font.render(item["chemical"]["name"], True, BLACK)
        text_rect = text.get_rect(center=item["rect"].center)
        screen.blit(text, text_rect)
    
    if len(placed_chems) == 2 and not product_items and not no_reaction:
        prods = get_reaction_products(placed_chems[0]["chemical"], placed_chems[1]["chemical"])
        if prods:
            count = len(prods)
            spacing_x = product_area_rect.width // (count + 1)
            for i, prod in enumerate(prods):
                prod_rect = pygame.Rect(product_area_rect.x + (i + 1) * spacing_x - 35,
                                        product_area_rect.y + (product_area_rect.height - 70) // 2, 70, 70)
                product_items.append({"chemical": prod, "rect": prod_rect})
            placed_chems = []
            no_reaction = False
        else:
            no_reaction = True
            
    if dragging_chem is not None:
        pygame.draw.rect(screen, dragging_chem["chemical"]["color"], dragging_chem["rect"], border_radius=10)
        pygame.draw.rect(screen, BLACK, dragging_chem["rect"], 1, border_radius=10)
        text = chemical_font.render(dragging_chem["chemical"]["name"], True, BLACK)
        text_rect = text.get_rect(center=dragging_chem["rect"].center)
        screen.blit(text, text_rect)
    
    mouse_pos = pygame.mouse.get_pos()
    # ----------------------------
    # Hover Description for Product Items and Panel Chemicals
    # ----------------------------
    if dragging_chem is None:
        # First, check if the mouse is hovering over any product item.
        hover_found = False
        for item in product_items:
            if item["rect"].collidepoint(mouse_pos):
                desc = item["chemical"]["description"]
                wrapped_lines = wrap_text(desc, hover_font, 220)
                line_height = hover_font.get_height() + 2
                box_height = line_height * len(wrapped_lines) + 8
                box_width = 400
                desc_bg = pygame.Surface((box_width, box_height))
                desc_bg.fill(GREY)
                pygame.draw.rect(desc_bg, BLACK, desc_bg.get_rect(), 1)
                desc_rect = desc_bg.get_rect()
                desc_rect.topleft = (mouse_pos[0] + 10, mouse_pos[1] + 10)
                if desc_rect.right > SCREEN_WIDTH:
                    desc_rect.right = SCREEN_WIDTH - 10
                if desc_rect.bottom > SCREEN_HEIGHT:
                    desc_rect.bottom = SCREEN_HEIGHT - 10
                screen.blit(desc_bg, desc_rect)
                for j, line in enumerate(wrapped_lines):
                    line_surf = hover_font.render(line, True, BLACK)
                    screen.blit(line_surf, (desc_rect.x + 6, desc_rect.y + 4 + j * line_height))
                hover_found = True
                break
        # If not hovering over a product, then check the panel chemicals.
        if not hover_found:
            for i, rect in enumerate(panel_chem_rects):
                if rect.collidepoint(mouse_pos):
                    desc = chemicals[i]["description"]
                    wrapped_lines = wrap_text(desc, hover_font, 220)
                    line_height = hover_font.get_height() + 2
                    box_height = line_height * len(wrapped_lines) + 8
                    box_width = 400
                    desc_bg = pygame.Surface((box_width, box_height))
                    desc_bg.fill(GREY)
                    pygame.draw.rect(desc_bg, BLACK, desc_bg.get_rect(), 1)
                    desc_rect = desc_bg.get_rect()
                    desc_rect.topleft = (mouse_pos[0] + 10, mouse_pos[1] + 10)
                    if desc_rect.right > SCREEN_WIDTH:
                        desc_rect.right = SCREEN_WIDTH - 10
                    if desc_rect.bottom > SCREEN_HEIGHT:
                        desc_rect.bottom = SCREEN_HEIGHT - 10
                    screen.blit(desc_bg, desc_rect)
                    for j, line in enumerate(wrapped_lines):
                        line_surf = hover_font.render(line, True, BLACK)
                        screen.blit(line_surf, (desc_rect.x + 6, desc_rect.y + 4 + j * line_height))
                    break

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and no_reaction:
            item_found = False
            for idx in range(len(placed_chems) - 1, -1, -1):
                item = placed_chems[idx]
                if item["rect"].collidepoint(event.pos):
                    # Only return the use if it came from the panel.
                    if item.get("source") == "panel":
                        item["chemical"]["uses"] += 1
                    placed_chems.pop(idx)
                    item_found = True
            if not placed_chems:
                no_reaction = False
            if item_found:
                continue

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if exit_button_rect.collidepoint(event.pos):
                root = tk.Tk()
                root.withdraw()

                # Ask user to confirm exit
                confirm = messagebox.askyesno("GAME ERROR!", "Please be kind to take what we give...")
                if confirm:
                    # Optional: Ask for feedback or a reason
                    reason = simpledialog.askstring("Feedback", "How is it so far? ")
                    print("User reason:", reason)
                    running = False
                root.destroy()
                running = False
                continue

            if ph_strip_rect.collidepoint(event.pos) and ph_strip_chem is not None:
                dragging_chem = {
                    "chemical": ph_strip_chem,
                    "rect": ph_strip_rect.copy(),
                    "offset": (event.pos[0] - ph_strip_rect.x, event.pos[1] - ph_strip_rect.y),
                    "source": "ph_strip",
                    "orig_rect": ph_strip_rect.copy()
                }
                ph_strip_chem = None
                ph_strip_color = LIGHT_YELLOW
                continue

            dragging_chem = None
            item_found = False
            for idx in range(len(free_items) - 1, -1, -1):
                item = free_items[idx]
                if item["rect"].collidepoint(event.pos):
                    dragging_chem = {
                        "chemical": item["chemical"],
                        "rect": item["rect"].copy(),
                        "offset": (event.pos[0] - item["rect"].x, event.pos[1] - item["rect"].y),
                        "source": "free",
                        "orig_rect": item["rect"].copy()
                    }
                    free_items.pop(idx)
                    item_found = True
                    break
            if item_found:
                continue

            for idx in range(len(product_items) - 1, -1, -1):
                item = product_items[idx]
                if item["rect"].collidepoint(event.pos):
                    dragging_chem = {
                        "chemical": item["chemical"],
                        "rect": item["rect"].copy(),
                        "offset": (event.pos[0] - item["rect"].x, event.pos[1] - item["rect"].y),
                        "source": "product",
                        "orig_rect": item["rect"].copy()
                    }
                    product_items.pop(idx)
                    item_found = True
                    break
            if item_found:
                continue

            for idx in range(len(placed_chems) - 1, -1, -1):
                item = placed_chems[idx]
                if item["rect"].collidepoint(event.pos):
                    dragging_chem = {
                        "chemical": item["chemical"],
                        "rect": item["rect"].copy(),
                        "offset": (event.pos[0] - item["rect"].x, event.pos[1] - item["rect"].y),
                        "source": "placed",
                        "orig_rect": item["rect"].copy()
                    }
                    placed_chems.pop(idx)
                    item_found = True
                    break
            if item_found:
                continue

            if inventory_area_rect.collidepoint(event.pos):
                inv_icon_size = 60
                inv_padding = 10
                icons_per_row = (inventory_area_rect.width - 2 * inv_padding) // (inv_icon_size + 5)
                for idx in range(len(inventory_items) - 1, -1, -1):
                    col = idx % icons_per_row
                    row = idx // icons_per_row
                    icon_x = inventory_area_rect.x + inv_padding + (inv_icon_size + 5) * col
                    icon_y = inventory_area_rect.y + inv_padding + (inv_icon_size + 5) * row
                    icon_rect = pygame.Rect(icon_x, icon_y, inv_icon_size, inv_icon_size)
                    if icon_rect.collidepoint(event.pos):
                        chem_item = inventory_items.pop(idx)
                        dragging_chem = {
                            "chemical": chem_item,
                            "rect": icon_rect.copy(),
                            "offset": (event.pos[0] - icon_rect.x, event.pos[1] - icon_rect.y),
                            "source": "inventory"
                        }
                        item_found = True
                        break
                if item_found:
                    continue

            if chemical_panel_rect.collidepoint(event.pos):
                for i, rect in enumerate(panel_chem_rects):
                    if rect.collidepoint(event.pos):
                        if chemicals[i]["uses"] > 0:
                            dragging_chem = {
                                "chemical": chemicals[i],
                                "rect": rect.copy(),
                                "offset": (event.pos[0] - rect.x, event.pos[1] - rect.y),
                                "source": "panel"
                            }
                            chemicals[i]["uses"] -= 1
                        break

        elif event.type == pygame.MOUSEWHEEL:
            total_chem_height = total_rows * spacing_y
            min_scroll = min(0, chemical_panel_rect.height - total_chem_height)
            scroll_offset += event.y * 20
            scroll_offset = max(min_scroll, min(0, scroll_offset))
        
        elif event.type == pygame.MOUSEMOTION:
            if dragging_chem is not None:
                new_x = event.pos[0] - dragging_chem["offset"][0]
                new_y = event.pos[1] - dragging_chem["offset"][1]
                dragging_chem["rect"].topleft = (new_x, new_y)
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragging_chem is not None:
                if trash_area_rect.collidepoint(dragging_chem["rect"].center):
                    dragging_chem = None
                    continue
                if ph_strip_rect.collidepoint(dragging_chem["rect"].center):
                    ph_strip_chem = dragging_chem["chemical"]
                    ph_strip_color = get_ph_strip_color(ph_strip_chem)
                    dragging_chem = None
                    continue
                # Allow duplicate entries in the inventory by simply appending
                if inventory_area_rect.collidepoint(dragging_chem["rect"].center):
                    if len(inventory_items) < 10:
                        inventory_items.append(dragging_chem["chemical"])
                    else:
                        free_items.append({"chemical": dragging_chem["chemical"], "rect": dragging_chem["rect"].copy()})
                    dragging_chem = None
                    continue
                if reaction_area_rect.collidepoint(dragging_chem["rect"].center):
                    placed_chems.append({
                        "chemical": dragging_chem["chemical"],
                        "rect": dragging_chem["rect"].copy(),
                        "source": dragging_chem["source"],
                        "orig_rect": dragging_chem.get("orig_rect", dragging_chem["rect"].copy())
                    })
                    dragging_chem = None
                    continue
                else:
                    free_items.append({
                        "chemical": dragging_chem["chemical"],
                        "rect": dragging_chem["rect"].copy()
                    })
                    dragging_chem = None

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()