from dataclasses import dataclass

@dataclass

class PlayerInfos():
    name: str
    level: int
    race: str
    class_type: str
    life: int
    max_life: int
    mana: int
    max_mana: int
    strength: float
    agility: float
    vitality: float
    intelligence: float
    charisma: float
    attack: float
    attack_speed: float
    defense: float
    spells: list
    experience: int
    inventory: dict
    wearing: dict
    atribute_cap: int

@dataclass

class PlayerEquips():
    max_life: int
    max_mana: int
    attack: float
    attack_speed: float
    defense: float

@dataclass

class PlayerBuffs():
    strength: float
    agility: float
    vitality: float
    intelligence: float
    charisma: float

@dataclass
    
class MonsterInfos():
    name: str
    type: str
    level:int
    strength: float
    agility: float
    vitality: float
    intelligence: float
    charisma: float
    life: int
    max_life: int
    attack: float
    attack_speed: float
    defense: float
    experience: int
    loot: dict

