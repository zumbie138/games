from .world_database import WorldDatabase
from .creatures_info import MonsterInfos, PlayerInfos
import pandas as pd
import math
class GameCore(WorldDatabase):
    def __init__(self):
        self.df_classes = self.classes_dataframe()
        self.player = None
        self.monster = None
        
    def _dataframe_to_tuple(self, dataframe:pd.DataFrame)->tuple:
        return tuple(dataframe.iloc[0])
        
    def _spells_by_class_lvl(self,player_class:str,player_lvl:int)->list:
        df_spells = self.spell_dataframe()
        class_spells = df_spells[(df_spells['class'] == player_class) & (df_spells['lvl'] <= player_lvl)]
        return class_spells['name'].to_list()
    
    def _generate_character(self,char_data: tuple):
        player_race, player_class, player_str, player_agi, player_vit, player_int, player_cha = char_data
        player_atk = player_str/2+player_agi/10+player_int/20+player_cha/50
        player_def = player_vit/2+player_agi/10+player_str/10
        player_life = int(math.ceil(100+(player_vit*2+player_str)/2))
        player_mana = int(math.ceil(10+(player_int*2+player_vit)/2))
        player_lvl = 1
        spell_list = self._spells_by_class_lvl(player_class,player_lvl)
        self.player = PlayerInfos(
            player_name=self.player_name,
            player_lvl=player_lvl,
            player_race=player_race,
            player_class=player_class,
            player_life=player_life,
            player_mana=player_mana,
            player_str=player_str,
            player_agi=player_agi,
            player_vit=player_vit,
            player_int=player_int,
            player_cha=player_cha,
            player_atk=player_atk,
            player_def=player_def,
            player_spell=spell_list,
            player_inventory={}
        )
      
    def _generate_monster(self):
        monster_df = self.monster_dataframe()
        self._dataframe_to_tuple(monster_df)
    
    def new_character(self, name:str, race:str, clas:str):
        print('Starting new character.')
        self.player_name = name
        print(f'Name: {name}\nRace: {race}\nClass: {clas}')
        class_info = self.df_classes[self.df_classes['class'] == clas]
        class_info_tuple = self._dataframe_to_tuple(class_info)
        self._generate_character(class_info_tuple)
    
    def load_character(self):
        print('Load saved characters.')
        
    def show_character(self):
        print('You see yourself in the mirror:')
        print(f'Your name is: {self.player.player_name}, you are an {self.player.player_race} {self.player.player_class}')
        print(f'HP: {self.player.player_life}/{self.player.player_life}\nMANA: {self.player.player_mana}/{self.player.player_mana}')
        print(f'You are level {self.player.player_lvl} and your atributes are:\nStrength: {self.player.player_str}\nAgility: {self.player.player_agi}\nVitality: {self.player.player_vit}\nInteligence: {self.player.player_int}\nCharisma: {self.player.player_cha}')
        print(f'Your list of spells: {self.player.player_spell}')