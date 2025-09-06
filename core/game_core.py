from database import GameBase, GameRepository, MessageLog
from .itens_core import ItensCore
from .spells_core import ConjuringSpell
from .loops_core import GameloopsCore
from .generation_core import GenerationCore


class GameCore(GameBase):
    def __init__(self):
        
        #instaciando as classes
        self.itens_core = ItensCore()
        self.spells_core = ConjuringSpell()
        self.loops_core = GameloopsCore()
        self.generation = GenerationCore()
        self.repository = GameRepository()
        
        self.current_tier = None
        self.current_city = None
        self.locations_list = None
        self.state = GameState.MENU
        self.df_classes = self.get_database_dataframe('class_database.json')
        self.df_spells = self.get_database_dataframe('spells_database.json')
        self.locations_df = self.get_database_dataframe('locations_database.json')
        self.tiers_df = self.get_database_dataframe('place_tier_database.json')
        self.city_places_df = self.get_database_dataframe('cityplaces_database.json')

    @property
    def player(self):
        return self.repository.get_resource('Player')
    @player.setter
    def player(self, value):
        self.repository.set_resource('Player', value)
    @property
    def monster(self):
        return self.repository.get_resource('Monster')
    @monster.setter
    def monster(self, value):
        self.repository.set_resource('Monster', value)
    @property
    def equips(self):
        return self.repository.get_resource('Equips')
    @equips.setter
    def equips(self, value):
        self.repository.set_resource('Equips', value)
    @property
    def buffs(self):
        return self.repository.get_resource('Buffs')
    @buffs.setter
    def buffs(self, value):
        self.repository.set_resource('Buffs', value)
    
    def set_place_tier(self, tier):
        tier_df_filtred = self.filter_dataframe_by_name(tier, 'tier', self.tiers_df)
        city = tier_df_filtred.iloc[0]['city']
        self.tier_city_df = self.filter_dataframe_by_name(city, 'city', self.city_places_df)
        self.current_tier = tier
        self.current_city = city
        
        self.locations_list = self.filter_dataframe_by_name(tier, 'tier', self.locations_df)
        # self.locations_list = self.get_list_from_dataframe_columm('name', tier_df_locations)

    
    def locations_allowed(self)->list:
        return self.locations_list

    def itens_allowed(self, body_part:str)->list:
        return self.itens_core.list_wearing_equipment(body_part)
    
    def new_character_core(self, name:str, race:str, clas:str):
        inventory={}
        wearing={'head':None,
                'neck':None,
                'torso':None,
                'arms':None,
                'right hand':None,
                'left hand':None,
                'waist':None,
                'legs':None,
                'foot':None,
                'finger':None,
                'wrist':None,
                'ears':None,
                'back':None}
        print('Starting new character.')
        print(f'Name: {name}\nRace: {race}\nClass: {clas}')
        class_info = self.df_classes[self.df_classes['class'] == clas]
        class_info_tuple = self.dataframe_to_tuple(class_info)
        new_tuple = (name, 1, 0, inventory, wearing)
        class_info_tuple = class_info_tuple + new_tuple
        self.generation.generate_character(class_info_tuple)
        self.generation.update_wearing_status()
        self.save_character(self.player)
        self.set_place_tier('tier 1')

    def load_character_core(self, char_choose):
        char_data = self.get_char_from_json(char_choose)
        self.generation.load_character(char_data)
        self.set_place_tier('tier 1')

    def start_healing_sleeping(self):
        self.loops_core.healing_active = True
        self.state = GameState.HEALING
    
    def stop_sleeping(self):
        self.loops_core.healing_active = False
        self.state = GameState.MENU
        
    def start_training(self, choice:str):
        self.loops_core.training_attribute = choice
        self.loops_core.training_active = True
        self.state = GameState.TRAINING
    
    def stop_training(self):
        self.loops_core.training_active = False
        self.state = GameState.MENU
    
    def start_menu_state(self):
        self.state = GameState.MENU
    
    def stop_battle(self):
        self.state = GameState.MENU
        self.loops_core.battle_active = False
    
    def start_battle(self, location:str):
        self.loops_core.monster_location = location
        self.state = GameState.BATTLE
        
    def manage_equips_core(self, option:bool, item:str, body_part:str):
        if option:
            self.itens_core.equip_item(item, body_part)
        else:
            self.itens_core.unequip_item(body_part)
        self.generation.update_wearing_status()
    
    def update_states(self, dt):
        print(f"\rCurrent state: {self.state}    ", end="", flush=True)
        if self.state == GameState.BATTLE:
            self.loops_core.update_combat_loop(dt)
        if self.state == GameState.TRAINING:
            self.state = self.loops_core.update_training_loop(dt)
        if self.state == GameState.HEALING:
            self.state = self.loops_core.update_healing(dt,'active')
        if self.state == GameState.MENU:
            return
            
            

class GameState:
    MENU = 0
    BATTLE = 1
    TRAINING = 2
    HEALING = 3