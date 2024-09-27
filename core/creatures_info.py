from dataclasses import dataclass

@dataclass

class PlayerInfos():
    char_name: str
    char_class: str
    char_race: str
    char_strg: float
    char_agi: float
    char_vit: float
    char_int: float
    char_char: float
    char_level: int
    char_life: int

    
class MonsterInfos():
    monster_name: str
    monster_strg: float
    monster_agi: float
    monster_vit: float
    monster_int: float
    monster_char: float
    monster_life: int