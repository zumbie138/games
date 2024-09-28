from .world_database import WorldDatabase

class GameCore():
    def __init__(self):
        data_base = WorldDatabase()
        self.df_classes = data_base.classes_dataframe()
        
    def new_character(self, name:str, race:str, clas:str):
        print('Starting new character.')
        print(f'Name: {name}\nRace: {race}\nClass: {clas}')
        class_info = self.df_classes[self.df_classes['class'] == clas]
        print(class_info)
        
    def saved_character(self):
        print('Load saved characters.')