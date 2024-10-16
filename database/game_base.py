import pandas as pd
import os
import json
from dataclasses import asdict

class GameBase():    
    def _load_json(self, file_name:str) -> dict:
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        with open(file_path) as f:
            return json.load(f)

    def get_database_dataframe(self,file_name:str)-> pd.DataFrame:
        database = self._load_json(file_name)
        return pd.DataFrame.from_dict(database, orient='index')
    
    def dataframe_to_tuple(self, dataframe:pd.DataFrame)->tuple:
        return tuple(dataframe.iloc[0])
    
    def get_columm_info_by_name(self, key_name:str,columm_name:str,data_base:pd.DataFrame):
        df_resulting=data_base[data_base['name'] == key_name]
        return df_resulting.iloc[0][columm_name]
    
    def dataclass_to_dict(self,dataclass_info)->dict:
        return asdict(dataclass_info)
    
    def get_list_load_character(self)->list:
        save_dirs = f'{os.getcwd()}\\save'
        return [f for f in os.listdir(save_dirs) if f.endswith('.json')]

    def get_char_from_json(self, file_name:str)->dict:
        save_dirs = f'{os.getcwd()}\\save'
        file_path = os.path.join(save_dirs,file_name)
        with open(file_path, 'r') as json_file:
            return json.load(json_file)

    def save_character(self,data_char):
        name = data_char.name
        save_dirs = f'{os.getcwd()}\\save'
        if not os.path.exists(save_dirs):
            os.makedirs(save_dirs)
        save_char = self.dataclass_to_dict(data_char)
        save_path = f'{save_dirs}\\{name}.json'
        with open(save_path, 'w') as json_file:
            json.dump(save_char, json_file)
# wd = WorldDatabase()
# classes_database = wd.classes_database
# df_classe_database = pd.DataFrame.from_dict(classes_database, orient='index')
# df_classe_database['soma_atributo'] = df_classe_database.apply(lambda row: pd.to_numeric(row, errors='coerce').sum(), axis=1)
# print(df_classe_database)