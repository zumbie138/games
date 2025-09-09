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

    def craft_item(self, item_name, ingredients:dict):
        ingredients_test = []
        for key, values in ingredients.items():
            if key in self.player.inventory and self.player.inventory[key] >= values:
                condition = True
            else:
                condition = False
            ingredients_test.append(condition)
        craft_condition = tuple(ingredients_test)
        if all(craft_condition):
            for key, values in ingredients.items():
                self.player.inventory[key] -= values
                if self.player.inventory[key] <= 0:
                    del self.player.inventory[key]
            self.player.inventory.get(item_name, 0) + 1
            MessageLog.add_message(f'You craft the item {item_name}.')
        else:
            MessageLog.add_message('You dont have enought material to craft.')
            
            
    def buy_item(self, item_name, item_price):
        if item_price <= self.player.inventory['gold']:
            self.player.inventory['gold'] -= item_price
            if self.player.inventory['gold'] < 0:
                del self.player.invetory['gold']
            self.player.inventory[item_name] = self.player.inventory.get(item_name, 0) + 1
            MessageLog.add_message(f'You bought one {item_name}.')
        else:
            MessageLog.add_message('You dont have enough gold.')

    def sell_item(self, item_name, item_price):
        if item_name in self.player.inventory:
            self.player.inventory[item_name] -= 1
            if self.player.inventory[item_name] <= 0:
                del self.player.inventory[item_name]
            self.player.inventory['gold'] += item_price
            MessageLog.add_message(f'You sell one {item_name} and get {item_price} gold.')
        else:
            MessageLog.add_message(f'You dont have the item {item_name} in your inventory.')
    
    def verify_life_potion(self):
        inventory_itens = self.player.inventory.keys()
        filtred_df = self.filter_dataframe_with_list_in_column(inventory_itens, self.itens_df, 'name')
        filtred_df = filtred_df[filtred_df['type'] == 'life potion']
        if filtred_df.empty:
            return False
        else:
            return filtred_df.iloc[0]['name']
        
    def verify_mana_potion(self):
        inventory_itens = self.player.inventory.keys()
        filtred_df = self.filter_dataframe_with_list_in_column(inventory_itens, self.itens_df, 'name')
        filtred_df = filtred_df[filtred_df['type'] == 'mana potion']
        if filtred_df.empty:
            return False
        else:
            return filtred_df.iloc[0]['name']
        
    def drink_life_potion(self, potion_name):
        self.player.inventory[potion_name] -= 1
        if self.player.inventory[potion_name] <= 0:
            del self.player.inventory[potion_name]
        potion_row = self.itens_df[self.itens_df['name'] == potion_name]
        healing_life = potion_row['heal_life'].values[0]
        self.player.life = min(healing_life + self.player.life, self.player.max_life)
        MessageLog.add_message(f'You heal {healing_life} life with potion')
        
    def drink_mana_potion(self, potion_name):
        self.player.inventory[potion_name] -= 1
        if self.player.inventory[potion_name] <= 0:
            del self.player.inventory[potion_name]
        potion_row = self.itens_df[self.itens_df['name'] == potion_name]
        healing_mana = potion_row['heal_mana'].values[0]
        self.player.mana = min(healing_mana + self.player.mana, self.player.max_mana)
        MessageLog.add_message(f'You heal {healing_mana} mana with potion')