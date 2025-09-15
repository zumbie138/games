from dataclasses import dataclass, field
from typing import List, Dict

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

def create_default_dict(keys:list, default_value = 0) -> Dict:
    return {key: default_value for key in keys}

@dataclass

class PlayerCounts():
    monster_kill: Dict[str, int] = field(default_factory= lambda: create_default_dict(['rat', 'bat', 'bandit']))
    gold_count: Dict[str, int] = field(default_factory= lambda: create_default_dict(['gold_looted', 'gold_from_selling', 'gold_from_quest','gold_earned','gold_spend']))
    potion_count:  Dict[str, int] = field(default_factory= lambda: create_default_dict(['potion_drink', 'potion_bought','potion_sold','mana_drink','life_drink']))
    dialogue_count: dict
    item_count: dict
    train_count: dict
    damage_count: dict
    time_count: dict
        
    quest_completed: list
    archivments_earned:  list
    
    
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

