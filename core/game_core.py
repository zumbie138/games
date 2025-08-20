from database import GameBase, GameRepository, MessageLog
from .itens_core import ItensCore
from .spells_core import ConjuringSpell
from .loops_core import GameloopsCore
from .generation_core import GenerationCore
import threading

class GameCore(GameBase):
    def __init__(self):
        
        #instaciando as classes
        self.itens_core = ItensCore()
        self.spells_core = ConjuringSpell()
        self.loops_core = GameloopsCore()
        self.generation = GenerationCore()
        self.repository = GameRepository()
        
        self.state = 0
        self.df_classes = self.get_database_dataframe('class_database.json')
        self.monster_df = self.get_database_dataframe('monster_database.json')
        self.df_spells = self.get_database_dataframe('spells_database.json')
        self.locations_df = self.get_database_dataframe('locations_database.json')

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
    
    def _monster_encounter(self,location:str):
        monster_rate = self.get_info_by_name(location,'name',
                                                         'monsters',self.locations_df)
        monster_name = self.get_name_by_rate_probability(monster_rate)
        monster_info = self.monster_df[self.monster_df['name'] == monster_name]
        monster_info_tuple = self.dataframe_to_tuple(monster_info)
        self.generation.generate_monster(monster_info_tuple)

    def locations_allowed(self)->list:
        return self.get_list_by_number(self.player.level, 'min lvl', 'name', self.locations_df)

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

    def load_character_core(self, char_choose):
        char_data = self.get_char_from_json(char_choose)
        self.generation.load_character(char_data)

    def city_status_core(self, text:str):
        print(text)
        print('Not working yet.')
    
    def battle_status_core(self, location:str):
        stop_battle = False
        control_thread = threading.Thread(target=self.loops_core.keyboard_control)
        control_thread.start()
        while not stop_battle:
            self.loops_core.batte_active = True
            self._monster_encounter(location)
            stop_battle = self.loops_core.battle_loop_manage()
    
    def show_character_core(self):
        print('You see yourself in the mirror:')
        print(f'Your name is: {self.player.name}, you are an {self.player.race} {self.player.class_type}')
        print(f'HP: {self.player.life:.2f}/{self.player.max_life}\nMANA: {self.player.mana}/{self.player.max_mana}')
        print(f'You are level {self.player.level}, with {self.player.experience} of experience and your atributes are:\nStrength: {self.player.strength:.2f}\nAgility: {self.player.agility:.2f}\nVitality: {self.player.vitality:.2f}\nInteligence: {self.player.intelligence:.2f}\nCharisma: {self.player.charisma:.2f}')
        print(f'Attack:{self.player.attack:.2f} Defense:{self.player.defense:.2f} attack speed:{self.player.attack_speed:.2f}')
        print(f'Your list of spells: {self.player.spells}')
        print(f'inventory:{self.player.inventory}')
        print(f'Equipped itens:\nMax Life: {self.equips.max_life}\nMax Mana: {self.equips.max_mana}\nAttack: {self.equips.attack}\nAttack speed: {self.equips.attack_speed}\nDefense: {self.equips.defense}')
        
        
        MessageLog.add_message('You see yourself in the mirror:')
        MessageLog.add_message(f'Your name is: {self.player.name}, you are an {self.player.race} {self.player.class_type}')
        MessageLog.add_message(f'HP: {self.player.life:.2f}/{self.player.max_life}\nMANA: {self.player.mana}/{self.player.max_mana}')
        MessageLog.add_message(f'You are level {self.player.level}, with {self.player.experience} of experience and your atributes are:\nStrength: {self.player.strength:.2f}\nAgility: {self.player.agility:.2f}\nVitality: {self.player.vitality:.2f}\nInteligence: {self.player.intelligence:.2f}\nCharisma: {self.player.charisma:.2f}')
        MessageLog.add_message(f'Attack:{self.player.attack:.2f} Defense:{self.player.defense:.2f} attack speed:{self.player.attack_speed:.2f}')
        MessageLog.add_message(f'Your list of spells: {self.player.spells}')
        MessageLog.add_message(f'inventory:{self.player.inventory}')
        MessageLog.add_message(f'Equipped itens:\nMax Life: {self.equips.max_life}\nMax Mana: {self.equips.max_mana}\nAttack: {self.equips.attack}\nAttack speed: {self.equips.attack_speed}\nDefense: {self.equips.defense}')

    def start_healing_sleeping(self):
        self.loops_core.healing_active = True
        self.state = 3
        
    def start_training(self, choice:str):
        self.loops_core.training_attribute = choice
        self.loops_core.training_active = True
        self.state = 2
    
    def start_battle(self):
        self.loops_core.batte_active = True
        self.state = 1
        
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