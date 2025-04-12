class Monster:
    def __init__(self, id, hp):  # Use __init__ instead of _init_
        self.id = id
        self.hp = hp
        self.max_hp = hp

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            return True  # Monster defeated
        return False  # Monster still alive


# Define monster data with the corrected Monster constructor
monster_data = {
    1: Monster(1, 190),
    2: Monster(2, 120),
    3: Monster(3, 65),
    4: Monster(4, 40),
    5: Monster(5, 12),
    6: Monster(6, 1000),
}