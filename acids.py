import pygame

class Acid:
    def __init__(self, name, damage, uses):
        self.name = name
        self.damage = damage
        self.uses = uses  

    def use(self):
        if self.uses > 0:
            self.uses -= 1
            return self.damage
        return 0 

    def is_usable(self):
        return self.uses > 0


def get_acids_for_stage(stage):
    if stage in [1, 2]:
        return {
            'weak': Acid('weak', 12, 10),
        }
    elif stage == 3:
        return {
            'strong': Acid('strong', 150, 3),
            'super': Acid('super', 250, 3),
        }
    else:
        return {} 
    
import pygame

def name_acid_lab1(Acid):
    acids = {
        "ethanoic_acid": {
            "object": Acid("ethanoic_acid", 12, 10),
            "image": pygame.image.load("Game project/lab_apparatus.png").convert_alpha()
        },
        "carbonic_acid": {
            "object": Acid("carbonic_acid", 15, 10),
            "image": pygame.image.load("Game project/lab_apparatus.png").convert_alpha()
        },
        "aluminium_complex": {
            "object": Acid("aluminium_complex", 20, 6),
            "image": pygame.image.load("Game project/lab_apparatus.png").convert_alpha()
        },
        "phosphoric_acid": {
            "object": Acid("phosphoric_acid", 22, 6),
            "image": pygame.image.load("Game project/lab_apparatus.png").convert_alpha()
        },
    }
    return acids


def name_acid_lab2(Acid):
    acids = {
        "HCl": {
            "object": Acid("HCl", 150, 10),
            "image": pygame.image.load("Game project/lab_apparatus.png").convert_alpha()
        },
        "HNO3": {
            "object": Acid("HNO3", 180, 10),
            "image": pygame.image.load("Game project/hno3.png").convert_alpha()
        },
        "H2SO4": {
            "object": Acid("H2SO4", 200, 10),
            "image": pygame.image.load("Game project/lab_apparatus.png").convert_alpha()
        },
        "H2F+SbF6": {
            "object": Acid("H2F+SbF6", 250, 2),
            "image": pygame.image.load("Game project/lab_apparatus.png").convert_alpha()
        },
    }
    return acids