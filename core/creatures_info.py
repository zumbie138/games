from dataclasses import dataclass

@dataclass

class PlayerInfos():
    player_name: str
    player_lvl: int
    player_race: str
    player_class: str
    player_life: int
    player_mana: int
    player_str: float
    player_agi: float
    player_vit: float
    player_int: float
    player_cha: float
    player_atk: float
    player_def: float
    player_spell: list
    player_inventory: dict

    
class MonsterInfos():
    monster_name: str
    monster_strg: float
    monster_agi: float
    monster_vit: float
    monster_int: float
    monster_player: float
    monster_life: int