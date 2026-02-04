class Character:
    def __init__(self, name, hp, mp, strength, magic, speed):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.mp = mp
        self.max_mp = mp
        self.strength = strength
        self.magic = magic
        self.speed = speed
        self.description = ""  # For enemies
        self.weakness = ""  # Elemental weakness

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp