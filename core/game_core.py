from database import GameBase, GameRepository
from .creatures_info import MonsterInfos, PlayerInfos, PlayerBuffs
from .itens_core import ItensCore
import math
import random

class GameCore(GameBase):
    def __init__(self):
        self.df_classes = self.get_database_dataframe('class_database.json')
        self.monster_df = self.get_database_dataframe('monster_database.json')
        self.df_spells = self.get_database_dataframe('spells_database.json')
        self.locations_df = self.get_database_dataframe('locations_database.json')
        self.itens_core = ItensCore()
        self.repository = GameRepository()

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
    
    def _generate_character(self,char_data: tuple):
        player_race, player_class, player_str, player_agi, player_vit, player_int, player_cha, player_name, player_lvl, player_exp, player_inv, player_wear = char_data
        player_atk = player_str+player_agi/2+player_int/20+player_cha/50
        player_def = player_vit/2+player_agi/10+player_str/10
        player_atk_spd = (100/(22.2222+player_agi))+0.5
        player_life = int(math.ceil(100+(player_vit*2+player_str)/2))
        player_mana = int(math.ceil(10+(player_int*2+player_vit)/2))
        spell_list = self.get_list_by_name_and_number(player_class,player_lvl,'class','lvl','name',self.df_spells)
        atribute_cap = 13 + (player_lvl*7)
        self.buffs = PlayerBuffs(0, 0, 0, 0, 0)
        player = PlayerInfos(
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
        self.repository.set_resource('Player', player)
        
    def _generate_monster(self,monster_data:tuple):
        monster_name, monster_type, monster_lvl, monster_str, monster_agi, monster_vit, monster_int, monster_cha, monster_life, monster_atk, monster_atk_spd, monster_def, monster_exp, monster_loot = monster_data
        monster = MonsterInfos(
            name=monster_name,
            type=monster_type,
            level=monster_lvl,
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
        self.repository.set_resource('Monster', monster)
        
    def _generate_buffs(self, buff_tuple:tuple):
        strength, agility, vitality, intelligence, charisma = buff_tuple
        buffs = PlayerBuffs(
            strength=strength,
            agility=agility,
            vitality=vitality,
            intelligence=intelligence,
            charisma=charisma
        )
        self.repository.set_resource('Buffs', buffs)

    def update_character(self):
        self.itens_core.update_wearing_status()
        strength = self.player.strength + self.buffs.strength
        agility = self.player.agility + self.buffs.agility
        vitality = self.player.vitality + self.buffs.vitality
        intelligence = self.player.intelligence + self.buffs.intelligence
        charisma = self.player.intelligence + self.buffs.charisma
        self.player.attack = strength + agility/2 + intelligence/20 + charisma/50 + self.equips.attack
        self.player.defense = vitality/2 + agility/10 + strength/10 + self.equips.defense
        self.player.attack_speed = (100 / (22.2222 + agility)) + 0.5 + self.equips.attack_speed
        self.player.max_life = int(math.ceil(100+(vitality*2 + strength)/2)) + self.equips.max_life
        self.player.max_mana = int(math.ceil(10+(intelligence*2 + vitality)/2)) + self.equips.max_mana
        self.player.spells = self.get_list_by_name_and_number(self.player.class_type,self.player.level,'class','lvl','name',self.df_spells)
        self.player.atribute_cap = 13 + (self.player.level * 7)   
        self.save_character(self.player)
        
    def new_character(self, name:str, race:str, clas:str):
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
        self._generate_character(class_info_tuple)
        self.save_character(self.player)

    def load_character(self,char_data:dict):
        print('Load saved character.')
        player = PlayerInfos(**char_data)
        buffs = PlayerBuffs(0, 0, 0, 0, 0)
        self.repository.set_resource('Player', player)
        self.repository.set_resource('Buffs', buffs)
        self.update_character()

    def show_character(self):

        print('You see yourself in the mirror:')
        print(f'Your name is: {self.player.name}, you are an {self.player.race} {self.player.class_type}')
        print(f'HP: {self.player.life:.2f}/{self.player.max_life}\nMANA: {self.player.mana}/{self.player.max_mana}')
        print(f'You are level {self.player.level}, with {self.player.experience} of experience and your atributes are:\nStrength: {self.player.strength:.2f}\nAgility: {self.player.agility:.2f}\nVitality: {self.player.vitality:.2f}\nInteligence: {self.player.intelligence:.2f}\nCharisma: {self.player.charisma:.2f}')
        print(f'Attack:{self.player.attack:.2f} Defense:{self.player.defense:.2f} attack speed:{self.player.attack_speed:.2f}')
        print(f'Your list of spells: {self.player.spells}')
        print(f'inventory:{self.player.inventory}')
        print(f'Equipped itens:\nMax Life: {self.equips.max_life}\nMax Mana: {self.equips.max_mana}\nAttack: {self.equips.attack}\nAttack speed: {self.equips.attack_speed}\nDefense: {self.equips.defense}')

    def level_up_character(self):
        self.player.level +=1
        self.repository.set_resource('Player', self.player)
        self.update_character()

    def verify_experience(self):
        level_up = {1:100,2:400,3:1000,4:1800,5:2800,6:4000,7:7500,8:10000}
        if level_up[self.player.level] <= self.player.experience:
            self.level_up_character()

    def locations_allowed(self)->list:
        return self.get_list_by_number(self.player.level, 'min lvl', 'name', self.locations_df)

    def monster_reward(self):
        monster_exp = self.get_random_in_interval(self.monster.experience)
        self.player.experience = self.player.experience + monster_exp
        print(f'You gain {monster_exp} experience.')       
        for item, (rate,min_qty,max_qty) in self.monster.loot.items():
            dice_roll = random.randint(0,100)
            quantity = random.randint(min_qty,max_qty)
            if rate >= dice_roll:
                self.player.inventory[item]=self.player.inventory.get(item, 0)+quantity
                print(f'you put on backpack: {quantity} x {item}')
        self.repository.set_resource('Player', self.player)
        self.verify_experience()
        self.save_character(self.player)

    def monster_encounter(self,location:str):
        monster_rate = self.get_info_by_name(location,'name',
                                                         'monsters',self.locations_df)
        monster_name = self.get_name_by_rate_probability(monster_rate)
        monster_info = self.monster_df[self.monster_df['name'] == monster_name]
        monster_info_tuple = self.dataframe_to_tuple(monster_info)
        self._generate_monster(monster_info_tuple)
    
    def healing_sleeping(self):
        while self.player.life < self.player.max_life or self.player.mana < self.player.max_mana:
            random_heal = random.randint(1,5)
            heal = random_heal + (self.player.vitality/2)
            mana_regen = random_heal + (self.player.intelligence/2)
            self.player.life = self.player.life + heal
            self.player.mana = self.player.mana + mana_regen
            if self.player.life > self.player.max_life:
                self.player.life = self.player.max_life
            if self.player.mana > self.player.max_mana:
                self.player.mana = self.player.max_mana
            print(f'You heal {heal} points of life, HP: {self.player.life}/{self.player.max_life}')
            # time.sleep(2.5)
        
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
            # self.player.life = self.player.life - 10
            # self.player.life = max(self.player.life, 0)
            # time.sleep(1)
            print(f'You train {train} points of {text}.')
            self.update_character()
            
    