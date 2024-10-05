import pandas as pd
import os
import json

class WorldDatabase():    
    def _load_json(self, file_name:str) -> dict:
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        with open(file_path) as f:
            return json.load(f)

    def get_database_dataframe(self,file_name:str)-> pd.DataFrame:
        database = self._load_json(file_name)
        return pd.DataFrame.from_dict(database, orient='index')
    
    def dataframe_to_tuple(self, dataframe:pd.DataFrame)->tuple:
        return tuple(dataframe.iloc[0])
    
# wd = WorldDatabase()
# classes_database = wd.classes_database
# df_classe_database = pd.DataFrame.from_dict(classes_database, orient='index')
# df_classe_database['soma_atributo'] = df_classe_database.apply(lambda row: pd.to_numeric(row, errors='coerce').sum(), axis=1)
# print(df_classe_database)