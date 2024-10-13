from database import WorldDatabase
from .creatures_info import MonsterInfos, PlayerInfos, PlayerEquips
import math
import random
import threading
import time

class GameCore(WorldDatabase):
    def __init__(self):
        self.df_classes = self.get_database_dataframe('class_database.json')
        self.monster_df = self.get_database_dataframe('monster_database.json')
        self.df_spells = self.get_database_dataframe('spells_database.json')
        self.locations_df = self.get_database_dataframe('locations_database.json')
        self.player = None
        self.monster = None    
        self.player_itens = None
        self.equips = None 
        
    def _spells_by_class_lvl(self,player_class:str,player_lvl:int)->list:
        class_spells = self.df_spells[(self.df_spells['class'] == player_class) & (self.df_spells['lvl'] <= player_lvl)]
        return class_spells['name'].to_list()
    
    def _locations_by_lvl(self,player_lvl:int)->list:
        locations = self.locations_df[self.locations_df['min lvl'] <= player_lvl]
        return locations['name'].to_list()
    
    def _get_encounter_rate(self,location:str)->dict:
        df_encounter=self.locations_df[self.locations_df['name'] == location]
        return df_encounter.iloc[0]['monsters']
    
    def _get_encounter_monster(self, monster_rate:dict)->str:
        for monster, rate in monster_rate.items():
            dice_roll = random.randint(0, 100)
            if dice_roll <= rate:
                return monster
    
    def _generate_monster(self,monster_data:tuple):
        monster_name, monster_type, monster_str, monster_agi, monster_vit, monster_int, monster_cha, monster_life, monster_atk, monster_atk_spd, monster_def, monster_exp, monster_loot = monster_data
        self.monster = MonsterInfos(
            name=monster_name,
            type=monster_type,
            strength=monster_str,
            agility=monster_agi,
            vitality=monster_vit,
            intelligence=monster_int,
            charisma=monster_cha,
            life=monster_life,
            max_life=monster_life,
            attack=monster_atk,
            attack_speed=monster_atk_spd,
            defense=monster_def,
            experience=monster_exp,
            loot=monster_loot
        )
    
    def _update_character(self):
        self.player.attack = self.player.strength+self.player.agility/2+self.player.intelligence/20+self.player.charisma/50
        self.player.defense = self.player.vitality/2+self.player.agility/10+self.player.strength/10
        
                            
    def _generate_character(self,char_data: tuple):
        player_race, player_class, player_str, player_agi, player_vit, player_int, player_cha, player_name, player_lvl, player_exp, player_inv, player_wear = char_data
        player_atk = player_str+player_agi/2+player_int/20+player_cha/50
        player_def = player_vit/2+player_agi/10+player_str/10
        player_atk_spd = (100/(22.2222+player_agi))+0.5
        player_life = int(math.ceil(100+(player_vit*2+player_str)/2))
        player_mana = int(math.ceil(10+(player_int*2+player_vit)/2))
        spell_list = self._spells_by_class_lvl(player_class,player_lvl)
        atribute_cap = 13 + (player_lvl*7)
        self.player = PlayerInfos(
            name=player_name,
            level=player_lvl,
            race=player_race,
            class_type=player_class,
            life=player_life,
            max_life=player_life,
            mana=player_mana,
            max_mana=player_mana,
            strength=player_str,
            agility=player_agi,
            vitality=player_vit,
            intelligence=player_int,
            charisma=player_cha,
            attack=player_atk,
            attack_speed=player_atk_spd,
            defense=player_def,
            spells=spell_list,
            experience=player_exp,
            inventory=player_inv,
            wearing=player_wear,
            atribute_cap=atribute_cap
        )
    

      
    def locations_allowed(self)->list:
        return self._locations_by_lvl(self.player.level)
        
    def new_character(self, name:str, race:str, clas:str):
        inventory={}
        wearing={
                'head':None,
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
            }
        print('Starting new character.')
        print(f'Name: {name}\nRace: {race}\nClass: {clas}')
        class_info = self.df_classes[self.df_classes['class'] == clas]
        class_info_tuple = self.dataframe_to_tuple(class_info)
        new_tuple = (name, 1, 0, inventory, wearing)
        class_info_tuple = class_info_tuple + new_tuple
        self._generate_character(class_info_tuple)
    
    def load_character(self):
        print('Load saved characters.')
        
    def show_character(self):
        print('You see yourself in the mirror:')
        print(f'Your name is: {self.player.name}, you are an {self.player.race} {self.player.class_type}')
        print(f'HP: {self.player.life}/{self.player.max_life}\nMANA: {self.player.mana}/{self.player.mana}')
        print(f'You are level {self.player.level} and your atributes are:\nStrength: {self.player.strength}\nAgility: {self.player.agility}\nVitality: {self.player.vitality}\nInteligence: {self.player.intelligence}\nCharisma: {self.player.charisma}')
        print(f'Your list of spells: {self.player.spells}')
        print(f'inventory:{self.player.inventory}')
        
    def monster_encounter(self,location:str):
        monster_rate = self._get_encounter_rate(location)
        monster_name = self._get_encounter_monster(monster_rate)
        monster_info = self.monster_df[self.monster_df['monster'] == monster_name]
        monster_info_tuple = self.dataframe_to_tuple(monster_info)
        self._generate_monster(monster_info_tuple)

    def player_battle_loop(self):
        while self.player.life > 0:
            if self.monster.life <= 0:
                break
            random_damage = random.randint(0,3)
            player_damage = math.ceil(self.player.attack*0.7 + random_damage*0.3 - self.monster.defense)
            player_damage = max(player_damage, 0)
            self.monster.life = self.monster.life - player_damage
            time.sleep(self.player.attack_speed)
            print(f'You deal {player_damage} damage.')
            
    def monster_battle_loop(self):
        while self.monster.life > 0:
            if self.player.life <= 0:
                break
            random_damage = random.randint(0,3)
            monster_damage = math.ceil(self.monster.attack*0.7 + random_damage*0.3 - self.player.defense)
            monster_damage = max(monster_damage, 0)
            self.player.life = self.player.life - monster_damage
            self.player.life = max(self.player.life, 0)
            time.sleep(2)
            print(f'You take {monster_damage} damage')

    def battle_turn_loop(self):
        turn = 1
        while True:
            if self.player.life <= 0:
                print('You are defeated')
                break
            elif self.monster.life <=0:
                print('you kill the monster')
                break
            else:
                time.sleep(5)
                print(f'Turn {turn} ends.')
                turn +=1

    def random_exp_monster(self)->int:
        return random.randint(self.monster.experience)
    
    def level_up_character(self):
        self.player.level +=1
        self._update_character()
    
    def verify_experience(self):
        level_up = {1:100,2:400,3:1000,4:1800,5:2800,6:4000,7:7500,8:10000}
        if level_up[self.player.level] <= self.player.experience:
            self.level_up_character()
    
    def monster_reward(self):
        self.player.experience = self.player.experience + self.random_exp_monster()
        for item, (rate,min_qty,max_qty) in self.monster.loot.items():
            dice_roll = random.randint(0,100)
            quantity = random.randint(min_qty,max_qty)
            if rate >= dice_roll:
                self.player.inventory[item]=self.player.inventory.get(item, 0)+quantity
                print(f'you put on backpack: {quantity} x {item}')
                
        
    def battle_core(self)->bool:
        print(f'You will battle a {self.monster.name}')

        player_thread = threading.Thread(target=self.player_battle_loop)
        monster_thread = threading.Thread(target=self.monster_battle_loop)
        turn_thread = threading.Thread(target=self.battle_turn_loop)

        player_thread.start()
        monster_thread.start()
        turn_thread.start()
        player_thread.join()
        monster_thread.join()
        turn_thread.join()
        print(f'HP:{self.player.life}/{self.player.max_life}')

        if self.player.life <= 0:
            return True
        else:
            self.monster_reward()
            return False
        
    def healing_sleeping(self):
        while self.player.life < self.player.max_life:
            random_heal = random.randint(1,5)
            heal = random_heal+(self.player.vitality/2)
            self.player.life = self.player.life + heal
            if self.player.life > self.player.max_life:
                self.player.life = self.player.max_life
            print(f'You heal {heal} points of life, HP: {self.player.life}/{self.player.max_life}')
            time.sleep(2.5)
            
    def training_atributes(self,choice:str):
        while self.player.life > 0:
            sum_atributes = self.player.strength+self.player.agility+self.player.vitality+self.player.intelligence+self.player.charisma
            if sum_atributes >= self.player.atribute_cap:
                print('You reach the training cap.')
                break
            train = random.uniform(0, 0.2)
            match choice:
                case '1':
                    text = 'strength'
                    self.player.strength = self.player.strength + train 
                case '2':
                    text = 'agility'
                    self.player.agility = self.player.agility + train 
                case '3':
                    text = 'vitality'
                    self.player.vitality = self.player.vitality + train 
                case '4':
                    text = 'intelligence'
                    self.player.intelligence = self.player.intelligence + train 
                case '5':
                    text = 'charisma'
                    self.player.charisma = self.player.charisma + train 
            self.player.life = self.player.life - 10
            self.player.life = max(self.player.life, 0)
            time.sleep(1)
            print(f'You train {train} points of {text}.')
            self._update_character()