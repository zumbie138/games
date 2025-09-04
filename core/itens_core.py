from database import GameBase, GameRepository, MessageLog
from .creatures_info import PlayerEquips
from .generation_core import GenerationCore

class ItensCore(GameBase):
    def __init__(self):
        self.itens_df = self.get_database_dataframe('itens_database.json')
        self.repository = GameRepository()
        self.generation = GenerationCore()
    
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
    
    def get_item_info(self, item_name):
        item_info = self.itens_df[self.itens_df['name'] == item_name]
        if not item_info.empty:
            return item_info.iloc[0].to_dict()
        return None
    
    def get_equippable_items(self)->list:
        equippable_items = []
        for item_name, quantity in self.player.inventory.items():
            item_info = self.get_item_info(item_name)
            if item_info and item_info['wearing'] != 'none' and quantity > 0 and item_info['type'] == 'equipment':
                equippable_items.append({
                    'name': item_name,
                    'quantity': quantity,
                    'slot_type': item_info['wearing']
                })
        return equippable_items
    
    def get_equippable_items_df(self):
        inventory_itens = self.get_keys_as_list(self.player.inventory)
        return self.filter_dataframe_with_list_in_column(inventory_itens, self.itens_df, 'name')
        
    def unequip_item(self, body_part:str):
        item_name = self.player.wearing[body_part]
        if item_name is not None:
            self.player.wearing[body_part] = None
            self.player.inventory[item_name] = self.player.inventory.get(item_name, 0) + 1
            print(f'You unequiped the item {item_name}')
            MessageLog.add_message(f'You unequiped the item {item_name}')
            self.generation.update_character()
        else:
            print('Theres nothing equiped already.')
            MessageLog.add_message('Theres nothing equiped already.')
        
    def equip_item(self, item_name:str, body_part:str):
        item_info = self.get_item_info(item_name)
        if item_info and item_info['wearing'] == body_part:
            current_item = self.player.wearing[body_part]
            if current_item:
                self.unequip_item(body_part)
                
            self.player.wearing[body_part] = item_name
            self.player.inventory[item_name] -= 1
            if self.player.inventory[item_name] <= 0:
                del self.player.inventory[item_name]
            self.generation.update_character()
            return True
        return False
    
class City(GameBase):
    def __init__(self, places_df, city):
        self.places_df = places_df
        self.current_city = city
        self.current_places = self.get_list_from_dataframe_columm('name', places_df)
        self.places_type = self.get_list_from_dataframe_columm('type', places_df)
        self.places_info = {}
    
    def _generate_places(self):
        for i, row in self.places_df.iterrow():
            self.places_info[row['name']] = {
                'type':row['type'],
                'craft':row['craft'],
                'healing_cost':row['healing_cost'],
                'buy_option':row['buy_option'],
                'sell_option':row['sell_option'],
                'mission':row['mission']
            }
            