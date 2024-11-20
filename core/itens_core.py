from database import GameBase
from core import GameCore

class ItensCore(GameBase):
    def __init__(self):
        self.itens_df = self.get_database_dataframe('itens_database.json')
        self.game_core = GameCore()
    
    def list_wering_equipment(self, body_part:str)->list:
        inventory_itens = self.get_keys_as_list(self.player.inventory)
        df_inv_itens = self.filter_dataframe_with_list_in_column(inventory_itens, self.itens_df, 'name')
        df_wearble = self.filter_dataframe_by_name(body_part,'wearing',df_inv_itens)
        return self.get_list_from_dataframe_columm('name',df_wearble)
    
    def update_wearing_status(self):
        equiped_list = self.get_values_as_list(self.player.wearing)
        df_equiped = self.filter_dataframe_with_list_in_column(equiped_list,self.itens_df,'name')
        max_hp = df_equiped['max_life'].sum()
        max_mana = df_equiped['max_mana'].sum()
        attack = df_equiped['attack'].sum()
        attack_speed = df_equiped['attack_speed'].sum()
        defense = df_equiped['defense'].sum()
        summary_tuple = (max_hp, max_mana, attack, attack_speed, defense)
        self.game_core.generate_equipments(summary_tuple)

    def equip_item(self,iten_name:str,body_part:str):
        self.player.wearing[body_part] = iten_name
        print(self.player.wearing)