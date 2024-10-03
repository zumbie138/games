import pandas as pd
import os
import json

class WorldDatabase():
    def __init__(self):
        self.class_database = self._load_json('class_database.json')
        self.monster_database = self._load_json('monster_database.json')
        self.spells_database = self._load_json('spells_database.json')
        
    def _load_json(self, file_name:str) -> dict:
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        with open(file_path) as f:
            return json.load(f)

    def get_classes_dataframe(self)-> pd.DataFrame:
        return pd.DataFrame.from_dict(self.class_database, orient='index')

    def get_monster_dataframe(self)-> pd.DataFrame:
        return pd.DataFrame.from_dict(self.monster_database, orient='index')

    def get_spell_dataframe(self)-> pd.DataFrame:
        return pd.DataFrame.from_dict(self.spells_database, orient='index') 



# wd = WorldDatabase()
# classes_database = wd.classes_database
# df_classe_database = pd.DataFrame.from_dict(classes_database, orient='index')
# df_classe_database['soma_atributo'] = df_classe_database.apply(lambda row: pd.to_numeric(row, errors='coerce').sum(), axis=1)
# print(df_classe_database)