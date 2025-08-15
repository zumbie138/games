from database import GameBase, GameRepository, MessageLog
from .creatures_info import PlayerEquips

class ItensCore(GameBase):
    def __init__(self):
        self.itens_df = self.get_database_dataframe('itens_database.json')
        self.repository = GameRepository()
    
    @property
    def player(self):
        return self.repository.get_resource('Player')    
    @player.setter
    def player(self, value):
        self.repository.set_resource('Player', value)

    def list_wearing_equipment(self, body_part:str)->list:
        inventory_itens = self.get_keys_as_list(self.player.inventory)
        df_inv_itens = self.filter_dataframe_with_list_in_column(inventory_itens, self.itens_df, 'name')
        df_wearble = self.filter_dataframe_by_name(body_part,'wearing',df_inv_itens)
        return self.get_list_from_dataframe_columm('name',df_wearble)

    def unequip_item(self, body_part:str):
        item_name = self.player.wearing[body_part]
        if item_name is not None:
            self.player.wearing[body_part] = None
            self.player.inventory[item_name] = self.player.inventory.get(item_name, 0)+1
            print(f'You unequiped the item {item_name}')
            MessageLog.add_message(f'You unequiped the item {item_name}')
        else:
            print('Theres nothing equiped already.')
            MessageLog.add_message('Theres nothing equiped already.')
    
    def equip_item(self,iten_name:str,body_part:str):
        self.player.wearing[body_part] = iten_name
        self.player.inventory[iten_name] -= 1
        if self.player.inventory[iten_name] <= 0:
            del self.player.inventory[iten_name]
        print(self.player.wearing)