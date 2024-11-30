from .creatures_info import PlayerInfos, PlayerEquips, PlayerBuffs, MonsterInfos
from database import GameBase, GameRepository
import math

class GenerationCore(GameBase):
    
    def __init__(self):
        self.df_spells = self.get_database_dataframe('spells_database.json')
        self.itens_df = self.get_database_dataframe('itens_database.json')
        self.repository = GameRepository()
    
    @property
    def player(self):
        return self.repository.get_resource('Player')    
    @player.setter
    def player(self, value):
        self.repository.set_resource('Player', value) 
    @property
    def equips(self):
        return self.repository.get_resource('Equips')
    @equips.setter
    def equips(self, value):
        self.repository.set_resource('Equips', value)
    @property
    def buffs(self):
        return self.repository.get_resource('Buffs')
    @buffs.setter
    def buffs(self, value):
        self.repository.set_resource('Buffs', value)
    
    
    def _calculate_attack(self, strength:float, agility:float, intelligence:float, charisma:float) -> float:
        return strength + agility/5 + intelligence/20 + charisma/50
        
    def _calculate_defense(self, vitality:float, agility:float, strength:float) -> float:
        return vitality/2 + agility/10 + strength/10
    
    def _calculate_atk_speed(self, agility:float) -> float:
        return (100 / (22.2222 + agility)) + 0.5
    
    def _calculate_life(self, vitality:float, strength:float) -> int:
        return int(math.ceil(100 + (vitality*2 + strength) / 2))
    
    def _calculate_mana(self, intelligence:float, vitality:float) -> int:
        return int(math.ceil(10 + (intelligence*2 + vitality) / 2))
    
    def generate_character(self,char_data: tuple):
        player_race, player_class, player_str, player_agi, player_vit, player_int, player_cha, player_name, player_lvl, player_exp, player_inv, player_wear = char_data
        player_atk = self._calculate_attack(player_str, player_agi, player_int, player_cha)
        player_def = self._calculate_defense(player_vit, player_agi, player_str)
        player_atk_spd = self._calculate_atk_speed(player_agi)
        player_life = self._calculate_life(player_vit, player_str)
        player_mana = self._calculate_mana(player_int, player_vit)
        spell_list = self.get_list_by_name_and_number(player_class,player_lvl,'class','lvl','name',self.df_spells)
        atribute_cap = 13 + (player_lvl*7)
        self.buffs = PlayerBuffs(0, 0, 0, 0, 0)
        player = PlayerInfos(
            name=player_name,
            level=player_lvl,
            race=player_race,
            class_type=player_class,
            life=player_life,
            max_life=player_life,
            mana=player_mana,
            max_mana=player_mana,
            strength=player_str,
            agility=player_agi,
            vitality=player_vit,
            intelligence=player_int,
            charisma=player_cha,
            attack=player_atk,
            attack_speed=player_atk_spd,
            defense=player_def,
            spells=spell_list,
            experience=player_exp,
            inventory=player_inv,
            wearing=player_wear,
            atribute_cap=atribute_cap
        )
        self.repository.set_resource('Player', player)
        
    def generate_monster(self,monster_data:tuple):
        monster_name, monster_type, monster_lvl, monster_str, monster_agi, monster_vit, monster_int, monster_cha, monster_life, monster_atk, monster_atk_spd, monster_def, monster_exp, monster_loot = monster_data
        monster = MonsterInfos(
            name=monster_name,
            type=monster_type,
            level=monster_lvl,
            strength=monster_str,
            agility=monster_agi,
            vitality=monster_vit,
            intelligence=monster_int,
            charisma=monster_cha,
            life=monster_life,
            max_life=monster_life,
            attack=monster_atk,
            attack_speed=monster_atk_spd,
            defense=monster_def,
            experience=monster_exp,
            loot=monster_loot
        )
        self.repository.set_resource('Monster', monster)
        
    def generate_buffs(self, buff_tuple:tuple):
        strength, agility, vitality, intelligence, charisma = buff_tuple
        buffs = PlayerBuffs(
            strength=strength,
            agility=agility,
            vitality=vitality,
            intelligence=intelligence,
            charisma=charisma
        )
        self.repository.set_resource('Buffs', buffs)
    
    def generate_equipments(self,equips_tuple:tuple):
        max_life,max_mana,attack,attack_speed,defense = equips_tuple
        equips = PlayerEquips(
            max_life=max_life,
            max_mana=max_mana,
            attack=attack,
            attack_speed=attack_speed,
            defense=defense
        )
        self.repository.set_resource('Equips', equips)
    
    def update_character(self):
        self.update_wearing_status()
        strength = self.player.strength + self.buffs.strength
        agility = self.player.agility + self.buffs.agility
        vitality = self.player.vitality + self.buffs.vitality
        intelligence = self.player.intelligence + self.buffs.intelligence
        charisma = self.player.intelligence + self.buffs.charisma
        self.player.attack = self._calculate_attack(strength, agility, intelligence, charisma) + self.equips.attack
        self.player.defense = self._calculate_defense(vitality, agility, strength) + self.equips.defense
        self.player.attack_speed = self._calculate_atk_speed(agility) + self.equips.attack_speed
        self.player.max_life = self._calculate_life(vitality, strength) + self.equips.max_life
        self.player.max_mana = self._calculate_mana(intelligence, vitality) + self.equips.max_mana
        self.player.spells = self.get_list_by_name_and_number(self.player.class_type, self.player.level,
                                                              'class','lvl','name',self.df_spells)
        self.player.atribute_cap = 13 + (self.player.level * 7)   
        self.save_character(self.player)
        
    def update_wearing_status(self):
        equiped_list = self.get_values_as_list(self.player.wearing)
        df_equiped = self.filter_dataframe_with_list_in_column(equiped_list,self.itens_df,'name')
        max_hp = df_equiped['max_life'].sum()
        max_mana = df_equiped['max_mana'].sum()
        attack = df_equiped['attack'].sum()
        attack_speed = df_equiped['attack_speed'].sum()
        defense = df_equiped['defense'].sum()
        summary_tuple = (max_hp, max_mana, attack, attack_speed, defense)
        self.generate_equipments(summary_tuple)
    
    def load_character(self,char_data:dict):
        print('Load saved character.')
        player = PlayerInfos(**char_data)
        buffs = PlayerBuffs(0, 0, 0, 0, 0)
        self.repository.set_resource('Player', player)
        self.repository.set_resource('Buffs', buffs)
        self.update_character()
        
    def verify_experience(self):
        level_up = {1:100,2:400,3:1000,4:1800,5:2800,6:4000,7:7500,8:10000}
        if level_up[self.player.level] <= self.player.experience:
            self.level_up_character()
    
    def level_up_character(self):
        self.player.level +=1
        self.update_character()