import pandas as pd
class WorldDatabase():
    def __init__(self):
        self.classes_database = {
            '0':{'race':'human','class':'warrior',  'strg':4,'agi':3,'vit':5,'int':0.5,'char':0.5},
            '1':{'race':'human','class':'wizard',   'strg':1,'agi':1,'vit':1,'int':5,  'char':5},
            '2':{'race':'human','class':'cleric',   'strg':1,'agi':1,'vit':2,'int':4,  'char':5},
            '3':{'race':'elf',  'class':'ranger',   'strg':5,'agi':5,'vit':1,'int':1,  'char':1},
            '4':{'race':'elf',  'class':'sorcerer', 'strg':1,'agi':2,'vit':1,'int':5,  'char':4},
            '5':{'race':'elf',  'class':'druid',    'strg':1,'agi':2,'vit':2,'int':3,  'char':5},
            '6':{'race':'orc',  'class':'barbarian','strg':5,'agi':5,'vit':2,'int':0.5,'char':0.5},
            '7':{'race':'orc',  'class':'witch',    'strg':2,'agi':1,'vit':2,'int':5,  'char':3},
            '8':{'race':'orc',  'class':'shaman',   'strg':2,'agi':1,'vit':2,'int':4,  'char':4},
        }
        
# wd = WorldDatabase()
# classes_database = wd.classes_database
# df_classe_database = pd.DataFrame.from_dict(classes_database, orient='index')
# df_classe_database['soma_atributo'] = df_classe_database.apply(lambda row: pd.to_numeric(row, errors='coerce').sum(), axis=1)
# print(df_classe_database)