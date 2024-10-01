import pandas as pd

class WorldDatabase():
    def classes_dataframe(self)-> pd.DataFrame:
        CLASSES_DATABASE = {
            '0':{'race':'human','class':'warrior',  'strg':4.0,'agi':3.0,'vit':5.0,'int':0.5,'char':0.5},
            '1':{'race':'human','class':'wizard',   'strg':1.0,'agi':1.0,'vit':1.0,'int':5.0,'char':5.0},
            '2':{'race':'human','class':'cleric',   'strg':1.0,'agi':1.0,'vit':2.0,'int':4.0,'char':5.0},
            '3':{'race':'elf',  'class':'ranger',   'strg':5.0,'agi':5.0,'vit':1.0,'int':1.0,'char':1.0},
            '4':{'race':'elf',  'class':'sorcerer', 'strg':1.0,'agi':2.0,'vit':1.0,'int':5.0,'char':4.0},
            '5':{'race':'elf',  'class':'druid',    'strg':1.0,'agi':2.0,'vit':2.0,'int':3.0,'char':5.0},
            '6':{'race':'orc',  'class':'barbarian','strg':5.0,'agi':5.0,'vit':2.0,'int':0.5,'char':0.5},
            '7':{'race':'orc',  'class':'witch',    'strg':2.0,'agi':1.0,'vit':2.0,'int':5.0,'char':3.0},
            '8':{'race':'orc',  'class':'shaman',   'strg':2.0,'agi':1.0,'vit':2.0,'int':4.0,'char':4.0},
        }
        return pd.DataFrame.from_dict(CLASSES_DATABASE, orient='index')

    def monster_database(self)-> pd.DataFrame:
        MONSTER_DATABASE = {
            
        }
        return pd.DataFrame.from_dict(MONSTER_DATABASE, orient='index')
        
# wd = WorldDatabase()
# classes_database = wd.classes_database
# df_classe_database = pd.DataFrame.from_dict(classes_database, orient='index')
# df_classe_database['soma_atributo'] = df_classe_database.apply(lambda row: pd.to_numeric(row, errors='coerce').sum(), axis=1)
# print(df_classe_database)