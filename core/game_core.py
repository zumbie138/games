from .world_database import WorldDatabase
import math
class GameCore(WorldDatabase):
    def __init__(self):
        self.df_classes = self.classes_dataframe()
        self.char_name: str
        self.char_race: str
        self.char_class: str
        self.char_lvl: int
        self.char_life: int
        self.char_mana: int
        self.char_str: float
        self.char_agi: float
        self.char_vit: float
        self.char_int: float
        self.char_cha: float
        self.char_atk: float
        self.char_def: float
        self.char_spell: list
        self.char_inventory: dict
        
    def new_character(self, name:str, race:str, clas:str):
        print('Starting new character.')
        self.char_name = name
        print(f'Name: {name}\nRace: {race}\nClass: {clas}')
        class_info = self.df_classes[self.df_classes['class'] == clas]
        class_info_tuple = tuple(class_info.iloc[0])
        self.char_lvl = 1
        self.generate_character(class_info_tuple)
    
    def spells_class_lvl(self):
        df_spells = self.spell_dataframe()
        class_spells = df_spells[(df_spells['class'] == self.char_class) & (df_spells['lvl'] <= self.char_lvl)]
        self.char_spell = class_spells['name'].to_list()
            
    def generate_character(self,char_data: tuple):
        self.char_race, self.char_class, self.char_str, self.char_agi, self.char_vit, self.char_int, self.char_cha = char_data
        self.char_atk = self.char_str/2+self.char_agi/10+self.char_int/20+self.char_cha/50
        self.char_def = self.char_vit/2+self.char_agi/10+self.char_str/10
        self.char_life = int(math.ceil(100+(self.char_vit*2+self.char_str)/2))
        self.char_mana = int(math.ceil(10+(self.char_int*2+self.char_vit)/2))
        self.spells_class_lvl()
        
    def load_character(self):
        print('Load saved characters.')
        
    def show_character(self):
        print('You see yourself in the mirror:')
        print(f'Your name is: {self.char_name}, you are an {self.char_race} {self.char_class}')
        print(f'HP: {self.char_life}/{self.char_life}\nMANA: {self.char_mana}/{self.char_mana}')
        print(f'You are level {self.char_lvl} and your atributes are:\nStrength: {self.char_str}\nAgility: {self.char_agi}\nVitality: {self.char_vit}\nInteligence: {self.char_int}\nCharisma: {self.char_cha}')
        print(f'Your list of spells: {self.char_spell}')