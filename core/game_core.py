from database import GameBase
from .creatures_info import MonsterInfos, PlayerInfos, PlayerEquips
import math
import random
import threading
import time

class GameCore(GameBase):
    def __init__(self):
        self.df_classes = self.get_database_dataframe('class_database.json')
        self.monster_df = self.get_database_dataframe('monster_database.json')
        self.df_spells = self.get_database_dataframe('spells_database.json')
        self.locations_df = self.get_database_dataframe('locations_database.json')
        self.itens_df = self.get_database_dataframe('itens_database.json')
        self.player = None
        self.monster = None    
        self.equips = None 

    def _generate_monster(self,monster_data:tuple):
        monster_name, monster_type, monster_lvl, monster_str, monster_agi, monster_vit, monster_int, monster_cha, monster_life, monster_atk, monster_atk_spd, monster_def, monster_exp, monster_loot = monster_data
        self.monster = MonsterInfos(
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

    def _generate_equipments(self,equips_tuple:tuple):
        max_life,max_mana,attack,attack_speed,defense = equips_tuple
        self.equips = PlayerEquips(
            max_life=max_life,
            max_mana=max_mana,
            attack=attack,
            attack_speed=attack_speed,
            defense=defense
        )
    
    def _update_character(self):
        self.player.attack = self.player.strength+self.player.agility/2+self.player.intelligence/20+self.player.charisma/50
        self.player.defense = self.player.vitality/2+self.player.agility/10+self.player.strength/10
        self.player.attack_speed = (100/(22.2222+self.player.agility))+0.5
        self.player.max_life = int(math.ceil(100+(self.player.vitality*2+self.player.strength)/2))
        self.player.max_mana = int(math.ceil(10+(self.player.intelligence*2+self.player.vitality)/2))
        self.player.spells = self.get_list_by_name_and_number(self.player.class_type,self.player.level,'class','lvl','name',self.df_spells)
        self.player.atribute_cap = 13 + (self.player.level*7)   
        self.update_wearing_status()      
        self.save_character(self.player)
        
    def _generate_character(self,char_data: tuple):
        player_race, player_class, player_str, player_agi, player_vit, player_int, player_cha, player_name, player_lvl, player_exp, player_inv, player_wear = char_data
        player_atk = player_str+player_agi/2+player_int/20+player_cha/50
        player_def = player_vit/2+player_agi/10+player_str/10
        player_atk_spd = (100/(22.2222+player_agi))+0.5
        player_life = int(math.ceil(100+(player_vit*2+player_str)/2))
        player_mana = int(math.ceil(10+(player_int*2+player_vit)/2))
        spell_list = self.get_list_by_name_and_number(player_class,player_lvl,'class','lvl','name',self.df_spells)
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
        return self.get_list_by_number(self.player.level, 'min lvl', 'name', self.locations_df)

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
        self.player = PlayerInfos(**char_data)
        self._update_character()

    def show_character(self):
        print('You see yourself in the mirror:')
        print(f'Your name is: {self.player.name}, you are an {self.player.race} {self.player.class_type}')
        print(f'HP: {self.player.life}/{self.player.max_life}\nMANA: {self.player.mana}/{self.player.max_mana}')
        print(f'You are level {self.player.level}, with {self.player.experience} of experience and your atributes are:\nStrength: {self.player.strength:.4}\nAgility: {self.player.agility:.4}\nVitality: {self.player.vitality:.4}\nInteligence: {self.player.intelligence:.4}\nCharisma: {self.player.charisma:.4}')
        print(f'Attack:{self.player.attack:.4} Defense:{self.player.defense:.4} attack speed:{self.player.attack_speed:.4}')
        print(f'Your list of spells: {self.player.spells}')
        print(f'inventory:{self.player.inventory}')
        print(f'Equipped itens:\nMax Life: {self.equips.max_life}\nMax Mana: {self.equips.max_mana}\nAttack: {self.equips.attack}\nAttack speed: {self.equips.attack_speed}\nDefense: {self.equips.defense}')

    def monster_encounter(self,location:str):
        monster_rate = self.get_dict_by_name_from_column(location,'name',
                                                         'monsters',self.locations_df)
        monster_name = self.get_name_by_rate_probability(monster_rate)
        monster_info = self.monster_df[self.monster_df['name'] == monster_name]
        monster_info_tuple = self.dataframe_to_tuple(monster_info)
        self._generate_monster(monster_info_tuple)

    def _damage_calculator(self,attack:float,defense:float,level:int)->float:
        damage = ((level * 5) / 10) + ((attack**2) / (attack + (2*defense)))
        min_damage = damage * 0.7
        max_damage = damage * 1.3
        final_damage = random.uniform(min_damage, max_damage)
        return final_damage
    
    def player_battle_loop(self):
        while self.player.life > 0 and self.monster.life > 0:
            attack = self.player.attack + self.equips.attack
            player_damage = self._damage_calculator(attack,self.monster.defense,self.player.level)
            self.monster.life = self.monster.life - player_damage
            time.sleep(self.player.attack_speed)
            print(f'You deal {player_damage:.4} damage.')

    def monster_battle_loop(self):
        while self.monster.life > 0 and self.player.life > 0:
            player_defense = self.player.defense + self.equips.defense
            monster_damage = self._damage_calculator(self.monster.attack, player_defense,self.monster.level)
            self.player.life = self.player.life - monster_damage
            self.player.life = max(self.player.life, 0)
            time.sleep(self.monster.attack_speed)
            print(f'You take {monster_damage:.4} damage.')

    def battle_turn_loop(self):
        turn = 1
        while True:
            if self.player.life <= 0:
                break
            elif self.monster.life <=0:
                break
            else:
                time.sleep(5)
                print(f'Turn {turn} ends.')
                turn +=1

    def level_up_character(self):
        self.player.level +=1
        self._update_character()

    def verify_experience(self):
        level_up = {1:100,2:400,3:1000,4:1800,5:2800,6:4000,7:7500,8:10000}
        if level_up[self.player.level] <= self.player.experience:
            self.level_up_character()

    def monster_reward(self):
        monster_exp = self.get_random_in_interval(self.monster.experience)
        self.player.experience = self.player.experience + monster_exp
        print(f'You gain {monster_exp} experience.')
        self.verify_experience()
        for item, (rate,min_qty,max_qty) in self.monster.loot.items():
            dice_roll = random.randint(0,100)
            quantity = random.randint(min_qty,max_qty)
            if rate >= dice_roll:
                self.player.inventory[item]=self.player.inventory.get(item, 0)+quantity
                print(f'you put on backpack: {quantity} x {item}')
        self.save_character(self.player)

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
            print('Youre defeated.')
            return True
        else:
            print('You kill the monster.')
            self.monster_reward()
            return False

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
            self._update_character()
            
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
        self._generate_equipments(summary_tuple)

    def equip_item(self,iten_name:str,body_part:str):
        self.player.wearing[body_part] = iten_name
        print(self.player.wearing)