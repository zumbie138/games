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
    strength: float
    agility: float
    vitality: float
    intelligence: float
    charisma: float
    attack: float
    defense: float
    spells: list

@dataclass

class PlayerEquips():
    max_life: int
    mana: int
    strength: float
    agility: float
    vitality: float
    intelligence: float
    charisma: float
    attack: float
    defense: float

@dataclass
    
class MonsterInfos():
    name: str
    type: str
    strength: float
    agility: float
    vitality: float
    intelligence: float
    charisma: float
    life: int
    max_life: int
    attack: float
    defense: float