"""Character classes for the RPG Engine."""
from typing import Dict, Optional


class Character:
    """Base character class with stats and methods."""
    
    def __init__(self, name: str, hp: int, mp: int, strength: int, magic: int, speed: int):
        """Initialize a character with stats.
        
        Args:
            name: Character name
            hp: Health Points
            mp: Magic Points
            strength: Physical attack power
            magic: Magical attack power
            speed: Determines turn order in ATB system
        """
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.strength = strength
        self.magic = magic
        self.speed = speed
        self.atb_gauge = 0  # Active Time Battle gauge
        self.weakness: Optional[str] = None
        
    def is_alive(self) -> bool:
        """Check if character is still alive."""
        return self.hp > 0
    
    def take_damage(self, damage: int) -> int:
        """Apply damage to character.
        
        Args:
            damage: Amount of damage to take
            
        Returns:
            Actual damage taken
        """
        actual_damage = min(damage, self.hp)
        self.hp = max(0, self.hp - damage)
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """Heal character.
        
        Args:
            amount: Amount to heal
            
        Returns:
            Actual amount healed
        """
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    
    def use_mp(self, cost: int) -> bool:
        """Use MP for spells.
        
        Args:
            cost: MP cost
            
        Returns:
            True if enough MP available, False otherwise
        """
        if self.mp >= cost:
            self.mp -= cost
            return True
        return False
    
    def restore_mp(self, amount: int) -> int:
        """Restore MP.
        
        Args:
            amount: Amount to restore
            
        Returns:
            Actual amount restored
        """
        old_mp = self.mp
        self.mp = min(self.max_mp, self.mp + amount)
        return self.mp - old_mp
    
    def update_atb(self, increment: int = 1) -> bool:
        """Update ATB gauge.
        
        Args:
            increment: Amount to increment gauge
            
        Returns:
            True if gauge is full (100), False otherwise
        """
        self.atb_gauge += increment * self.speed
        if self.atb_gauge >= 100:
            self.atb_gauge = 100
            return True
        return False
    
    def reset_atb(self):
        """Reset ATB gauge after taking a turn."""
        self.atb_gauge = 0
    
    def get_stats(self) -> Dict[str, int]:
        """Get character stats as dictionary."""
        return {
            "HP": self.hp,
            "Max HP": self.max_hp,
            "MP": self.mp,
            "Max MP": self.max_mp,
            "Strength": self.strength,
            "Magic": self.magic,
            "Speed": self.speed,
            "ATB": self.atb_gauge
        }
    
    def __str__(self) -> str:
        """String representation of character."""
        return f"{self.name} - HP: {self.hp}/{self.max_hp} MP: {self.mp}/{self.max_mp}"


class Spell:
    """Spell class for magic attacks and abilities."""
    
    def __init__(self, name: str, mp_cost: int, power: int, element: Optional[str] = None):
        """Initialize a spell.
        
        Args:
            name: Spell name
            mp_cost: MP cost to cast
            power: Base power/damage
            element: Element type (fire, ice, thunder, etc.)
        """
        self.name = name
        self.mp_cost = mp_cost
        self.power = power
        self.element = element
    
    def calculate_damage(self, caster_magic: int, target_weakness: Optional[str] = None) -> int:
        """Calculate spell damage.
        
        Args:
            caster_magic: Magic stat of caster
            target_weakness: Target's elemental weakness
            
        Returns:
            Calculated damage
        """
        base_damage = self.power + (caster_magic * 2)
        
        # Double damage if hitting weakness
        if self.element and target_weakness and self.element.lower() == target_weakness.lower():
            base_damage *= 2
            
        return base_damage
    
    def __str__(self) -> str:
        """String representation of spell."""
        element_str = f" ({self.element})" if self.element else ""
        return f"{self.name}{element_str} - MP: {self.mp_cost}, Power: {self.power}"


# Predefined spells
SPELLS = {
    "Fire": Spell("Fire", mp_cost=10, power=20, element="fire"),
    "Ice": Spell("Blizzard", mp_cost=10, power=20, element="ice"),
    "Thunder": Spell("Thunder", mp_cost=10, power=20, element="thunder"),
    "Cure": Spell("Cure", mp_cost=8, power=30, element="healing"),
}
