from .world_database import WorldDatabase

class GameCore(WorldDatabase):
    def __init__(self):
        self.df_classes = self.classes_dataframe()
        self.char_name: str = ''
        self.char_race: str = ''
        self.char_class: str = ''
        self.char_lvl: int = 1
        self.char_life: int = 0
        self.char_mana: int = 0
        self.char_str: float = 0.0
        self.char_agi: float = 0.0
        self.char_vit: float = 0.0
        self.char_int: float = 0.0
        self.char_cha: float = 0.0
        self.char_atk: float = 0.0
        self.char_def: float = 0.0
        
    def new_character(self, name:str, race:str, clas:str):
        print('Starting new character.')
        self.char_name = name
        print(f'Name: {name}\nRace: {race}\nClass: {clas}')
        class_info = self.df_classes[self.df_classes['class'] == clas]
        class_info_tuple = tuple(class_info.iloc[0])
        print(class_info_tuple)
        self.generate_character(class_info_tuple)
    
    def generate_character(self,char_data: tuple):
        self.char_race, self.char_class, self.char_str, self.char_agi, self.char_vit, self.char_int, self.char_cha = char_data
        self.char_atk = self.char_str/2+self.char_agi/10+self.char_int/20+self.char_cha/50
        self.char_def = self.char_vit/2+self.char_agi/10+self.char_str/10
        self.char_life = 100+(self.char_vit/5+self.char_str/10)
        
    def load_character(self):
        print('Load saved characters.')