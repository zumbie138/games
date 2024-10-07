from database import WorldDatabase
from .creatures_info import MonsterInfos, PlayerInfos
import math
import random

class GameCore(WorldDatabase):
    def __init__(self):
        self.df_classes = self.get_database_dataframe('class_database.json')
        self.monster_df = self.get_database_dataframe('monster_database.json')
        self.df_spells = self.get_database_dataframe('spells_database.json')
        self.locations_df = self.get_database_dataframe('locations_database.json')
        self.player = None
        self.monster = None       
        
    def _spells_by_class_lvl(self,player_class:str,player_lvl:int)->list:
        class_spells = self.df_spells[(self.df_spells['class'] == player_class) & (self.df_spells['lvl'] <= player_lvl)]
        return class_spells['name'].to_list()
    
    def _locations_by_lvl(self,player_lvl:int)->list:
        locations = self.locations_df[self.locations_df['min lvl'] <= player_lvl]
        return locations['name'].to_list()
    
    def _get_encounter_rate(self,location:str)->dict:
        df_encounter=self.locations_df[self.locations_df['name'] == location]
        return df_encounter.iloc[0]['monsters']
    
    def _get_encounter_monster(self, monster_rate:dict)->str:
        for monster, rate in monster_rate.items():
            dice_roll = random.randint(0, 100)
            if dice_roll <= rate:
                return monster
    
    def _generate_monster(self,monster_data:tuple):
        monster_name, monster_type, monster_str, monster_agi, monster_vit, monster_int, monster_cha, monster_life, monster_atk, monster_def = monster_data
        self.monster = MonsterInfos(
            name=monster_name,
            type=monster_type,
            strength=monster_str,
            agility=monster_agi,
            vitality=monster_vit,
            intelligence=monster_int,
            charisma=monster_cha,
            life=monster_life,
            max_life=monster_life,
            attack=monster_atk,
            defense=monster_def
        )
                    
    def _generate_character(self,char_data: tuple):
        player_race, player_class, player_str, player_agi, player_vit, player_int, player_cha = char_data
        player_atk = player_str/2+player_agi/10+player_int/20+player_cha/50
        player_def = player_vit/2+player_agi/10+player_str/10
        player_life = int(math.ceil(100+(player_vit*2+player_str)/2))
        player_mana = int(math.ceil(10+(player_int*2+player_vit)/2))
        player_lvl = 1
        spell_list = self._spells_by_class_lvl(player_class,player_lvl)
        self.player = PlayerInfos(
            name=self.player_name,
            level=player_lvl,
            race=player_race,
            class_type=player_class,
            life=player_life,
            max_life=player_life,
            mana=player_mana,
            strength=player_str,
            agility=player_agi,
            vitality=player_vit,
            intelligence=player_int,
            charisma=player_cha,
            attack=player_atk,
            defense=player_def,
            spells=spell_list
        )
      
    
    def locations_allowed(self)->list:
        return self._locations_by_lvl(self.player.level)
        
    def new_character(self, name:str, race:str, clas:str):
        print('Starting new character.')
        self.player_name = name
        print(f'Name: {name}\nRace: {race}\nClass: {clas}')
        class_info = self.df_classes[self.df_classes['class'] == clas]
        class_info_tuple = self.dataframe_to_tuple(class_info)
        self._generate_character(class_info_tuple)
    
    def load_character(self):
        print('Load saved characters.')
        
    def show_character(self):
        print('You see yourself in the mirror:')
        print(f'Your name is: {self.player.name}, you are an {self.player.race} {self.player.class_type}')
        print(f'HP: {self.player.life}/{self.player.life}\nMANA: {self.player.mana}/{self.player.mana}')
        print(f'You are level {self.player.level} and your atributes are:\nStrength: {self.player.strength}\nAgility: {self.player.agility}\nVitality: {self.player.vitality}\nInteligence: {self.player.intelligence}\nCharisma: {self.player.charisma}')
        print(f'Your list of spells: {self.player.spells}')
        
    def monster_encounter(self,location:str):
        monster_rate = self._get_encounter_rate(location)
        monster_name = self._get_encounter_monster(monster_rate)
        monster_info = self.monster_df[self.monster_df['monster'] == monster_name]
        monster_info_tuple = self.dataframe_to_tuple(monster_info)
        self._generate_monster(monster_info_tuple)

    
