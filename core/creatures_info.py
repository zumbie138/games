from dataclasses import dataclass

@dataclass

class PlayerInfos():
    name: str
    level: int
    race: str
    class_type: str
    life: int
    mana: int
    strength: float
    agility: float
    vitality: float
    intelligence: float
    charisma: float
    attack: float
    defense: float
    spells: list

    
class MonsterInfos():
    name: str
    type: str
    life: int
    mana: int
    strength: float
    agility: float
    vitality: float
    intelligence: float
    charisma: float
    attack: float
    defense: float
    spells: list