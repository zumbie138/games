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

    def monster_dataframe(self)-> pd.DataFrame:
        MONSTER_DATABASE = {
            
        }
        return pd.DataFrame.from_dict(MONSTER_DATABASE, orient='index')
    
    def spell_dataframe(self)-> pd.DataFrame:
        SPELLS_DATABASE = {
    '00':{'name':'courage',    'class':'warrior',  'type':'passive',  'lvl':1, 'activation':0.3,'mana':0},
    '01':{'name':'focus',      'class':'warrior',  'type':'passive',  'lvl':5, 'activation':0.2,'mana':0},
    '02':{'name':'adrenaline', 'class':'warrior',  'type':'passive',  'lvl':10,'activation':0.1,'mana':0},
    '03':{'name':'spark',      'class':'wizard',   'type':'offensive','lvl':1, 'activation':0.3,'mana':1},
    '04':{'name':'thunder',    'class':'wizard',   'type':'offensive','lvl':5, 'activation':0.2,'mana':5},
    '05':{'name':'storm',      'class':'wizard',   'type':'offensive','lvl':10,'activation':0.1,'mana':10},
    '06':{'name':'self heal',  'class':'cleric',   'type':'healing',  'lvl':1, 'activation':0.3,'mana':2},
    '07':{'name':'protection', 'class':'cleric',   'type':'buff',     'lvl':5, 'activation':0.2,'mana':4},
    '08':{'name':'bless',      'class':'cleric',   'type':'buff',     'lvl':10,'activation':0.1,'mana':6},
    '09':{'name':'fast attack','class':'ranger',   'type':'buff',     'lvl':1, 'activation':0.3,'mana':2},
    '10':{'name':'agility',    'class':'ranger',   'type':'passive',  'lvl':5, 'activation':0.2,'mana':0},
    '11':{'name':'stealth',    'class':'ranger',   'type':'buff',     'lvl':10,'activation':0.1,'mana':5},
    '12':{'name':'fire arrow', 'class':'sorcerer', 'type':'offensive','lvl':1, 'activation':0.3,'mana':1},
    '13':{'name':'fire shower','class':'sorcerer', 'type':'offensive','lvl':5, 'activation':0.2,'mana':5},
    '14':{'name':'blaze',      'class':'sorcerer', 'type':'offensive','lvl':10,'activation':0.1,'mana':10},
    '15':{'name':'leech life', 'class':'druid',    'type':'offensive','lvl':1, 'activation':0.3,'mana':2},
    '16':{'name':'stone skin', 'class':'druid',    'type':'buff',     'lvl':5, 'activation':0.2,'mana':4},
    '17':{'name':'wild form',  'class':'druid',    'type':'buff',     'lvl':10,'activation':0.1,'mana':6},
    '18':{'name':'rage',       'class':'barbarian','type':'buff',     'lvl':1, 'activation':0.3,'mana':2},
    '19':{'name':'fatal blow', 'class':'barbarian','type':'offensive','lvl':5, 'activation':0.2,'mana':2},
    '20':{'name':'insanity',   'class':'barbarian','type':'buff',     'lvl':10,'activation':0.1,'mana':3},
    '21':{'name':'curse',      'class':'witch',    'type':'offensive','lvl':1, 'activation':0.3,'mana':2},
    '22':{'name':'poison',     'class':'witch',    'type':'offensive','lvl':5, 'activation':0.2,'mana':6},
    '23':{'name':'disease',    'class':'witch',    'type':'offensive','lvl':10,'activation':0.1,'mana':6},
    '24':{'name':'cleansing',  'class':'shaman',   'type':'healing',  'lvl':1, 'activation':0.3,'mana':2},
    '25':{'name':'hex',        'class':'shaman',   'type':'offensive','lvl':5, 'activation':0.2,'mana':5},
    '26':{'name':'spark armor','class':'shaman',   'type':'buff',     'lvl':10,'activation':0.1,'mana':5},
        }   
        return pd.DataFrame.from_dict(SPELLS_DATABASE, orient='index') 
# wd = WorldDatabase()
# classes_database = wd.classes_database
# df_classe_database = pd.DataFrame.from_dict(classes_database, orient='index')
# df_classe_database['soma_atributo'] = df_classe_database.apply(lambda row: pd.to_numeric(row, errors='coerce').sum(), axis=1)
# print(df_classe_database)