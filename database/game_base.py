import pandas as pd
import os
import json
import random
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
    
    def list_keys_dictonary(self,dict_in:dict)->list:
        return list(dict_in.keys())

    def filter_dataframe_with_list_in_column(self,list_in:list,dataframe_in:pd.DataFrame,columm_name:str)->pd.DataFrame:
        return dataframe_in[dataframe_in[columm_name].isin(list_in)]
    
    def filter_dataframe_by_name(dataframe_in:pd.DataFrame,name:str,columm_name:str)->pd.DataFrame:
        return dataframe_in[dataframe_in[columm_name] == name]
    
    def get_list_by_name_and_number(self,name:str,number:int,columm_name:str,columm_number:str,columm_list:str,dataframe:pd.DataFrame)->list:
        class_spells = dataframe[(dataframe[columm_name] == name) & (dataframe[columm_number] <= number)]
        return class_spells[columm_list].to_list()
    
    def get_list_by_number(self,number:int,columm_number:str,columm_list:str,dataframe:pd.DataFrame)->list:
        locations = dataframe[dataframe[columm_number] <= number]
        return locations[columm_list].to_list()
    
    def get_dict_by_name_from_column(self,name:str,columm_name:str,columm_dict:str,dataframe:pd.DataFrame)->dict:
        df_encounter=dataframe[dataframe[columm_name] == name]
        return df_encounter.iloc[0][columm_dict]
    
    def get_name_by_rate_probability(self, dict_rate:dict)->str:
        for name, rate in dict_rate.items():
            percent_roll = random.randint(0, 100)
            if percent_roll <= rate:
                return name
    
    def get_list_from_dataframe_columm(self,columm_name:str,dataframe:pd.DataFrame)->list:
        return dataframe[columm_name].to_list()
# wd = WorldDatabase()
# classes_database = wd.classes_database
# df_classe_database = pd.DataFrame.from_dict(classes_database, orient='index')
# df_classe_database['soma_atributo'] = df_classe_database.apply(lambda row: pd.to_numeric(row, errors='coerce').sum(), axis=1)
# print(df_classe_database)