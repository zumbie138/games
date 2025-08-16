from database import GameBase, GameRepository, MessageLog
from .spells_core import ConjuringSpell
from .generation_core import GenerationCore
import time
import keyboard
import threading

class GameloopsCore(GameBase):
    def __init__(self):
        #instaciando classes
        self.conjuring_spell = ConjuringSpell()
        self.repository = GameRepository()
        self.generation = GenerationCore()
        
        #criando variaveis de controle
        self.battle_timer = 0
        self.training_timer = 0
        self.healing_timer = 0
        self.current_turn = 1
        self.training_attribute = None
        self.batte_active = True
    
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

    def _stop_battle(self):
        self.batte_active = False

    def _damage_calculator(self,attack:float,defense:float,level:int)->float:
        damage = ((level * 5) / 10) + ((attack**2) / (attack + (2*defense)))
        final_damage = self.get_random_min_max(damage)
        return final_damage

    def _monster_reward(self):
        monster_exp = self.get_random_in_interval(self.monster.experience)
        self.player.experience = self.player.experience + monster_exp
        print(f'You gain {monster_exp} experience.')       
        MessageLog.add_message(f'You gain {monster_exp} experience.')       
        for item, (rate,min_qty,max_qty) in self.monster.loot.items():
            dice_roll = self.get_random_in_interval((0,100))
            quantity = self.get_random_in_interval((min_qty,max_qty))
            if rate >= dice_roll:
                self.player.inventory[item]=self.player.inventory.get(item, 0)+quantity
                print(f'you put on backpack: {quantity} x {item}')
                MessageLog.add_message(f'you put on backpack: {quantity} x {item}')
        self.repository.set_resource('Player', self.player)
        self.generation.verify_experience()
        self.save_character(self.player)

    def player_battle_loop(self):
        while self.batte_active:
            self.conjuring_spell.conjuring_core(self.player.spells, self.player.intelligence, self.player.charisma)
            player_damage = self._damage_calculator(self.player.attack,self.monster.defense,self.player.level)
            self.monster.life = self.monster.life - player_damage
            time.sleep(self.player.attack_speed)
            print(f'You deal {player_damage:.2f} damage.')
            MessageLog.add_message(f'You deal {player_damage:.2f} damage.')
            if self.player.life <= 0 or self.monster.life <= 0:
                break

    def monster_battle_loop(self):
        while self.batte_active:
            monster_damage = self._damage_calculator(self.monster.attack, self.player.defense, self.monster.level)
            self.player.life = self.player.life - monster_damage
            self.player.life = max(self.player.life, 0)
            time.sleep(self.monster.attack_speed)
            print(f'You take {monster_damage:.2f} damage.')
            MessageLog.add_message(f'You take {monster_damage:.2f} damage.')
            if self.monster.life <= 0 or self.player.life <= 0:
                break

    def battle_healing_loop(self):
        while self.batte_active:
            random_heal = self.get_random_in_interval((1,5))
            heal = random_heal + (self.player.vitality/4)
            mana_regen = random_heal + (self.player.intelligence/4)
            self.player.life = self.player.life + heal
            self.player.mana = self.player.mana + mana_regen
            if self.player.life > self.player.max_life:
                self.player.life = self.player.max_life
            if self.player.mana > self.player.max_mana:
                self.player.mana = self.player.max_mana
            print(f'You heal {heal:.2f} points of life, HP: {self.player.life:.2f}/{self.player.max_life}')
            print(f'You heal {mana_regen:.2f} points of mana, MANA: {self.player.mana:.2f}/{self.player.max_mana}')
            
            MessageLog.add_message(f'You heal {heal:.2f} points of life, HP: {self.player.life:.2f}/{self.player.max_life}')
            MessageLog.add_message(f'You heal {mana_regen:.2f} points of mana, MANA: {self.player.mana:.2f}/{self.player.max_mana}')
            time.sleep(2.5)
            if self.player.life == self.player.max_life and self.player.mana == self.player.max_mana:
                break

    def keyboard_control(self):
        while self.batte_active:
            if keyboard.is_pressed('r'):
                self._stop_battle()

    def battle_turn_loop(self):
        turn = 1
        while self.batte_active:
            if self.player.life <= 0:
                break
            elif self.monster.life <= 0:
                break
            else:
                self.conjuring_spell.check_active_durations()
                self.conjuring_spell.apply_turn_damage()
                time.sleep(5)
                print(f'Turn {turn} ends.')
                MessageLog.add_message(f'Turn {turn} ends.')
                turn +=1

    def battle_loop_manage(self) -> bool:
        print(f'You will battle a {self.monster.name}')
        MessageLog.add_message(f'You will battle a {self.monster.name}')

        player_thread = threading.Thread(target=self.player_battle_loop)
        monster_thread = threading.Thread(target=self.monster_battle_loop)
        turn_thread = threading.Thread(target=self.battle_turn_loop)
       

        player_thread.start()
        monster_thread.start()
        turn_thread.start()
        
        
        player_thread.join()
        monster_thread.join()
        turn_thread.join()
        
        print(f'HP:{self.player.life:.2f}/{self.player.max_life}')
        print(f'MANA:{self.player.mana:.2f}/{self.player.max_mana}')
        
        MessageLog.add_message(f'HP:{self.player.life:.2f}/{self.player.max_life}')
        MessageLog.add_message(f'MANA:{self.player.mana:.2f}/{self.player.max_mana}')
        
        self.conjuring_spell.reset_buffs()
        if self.monster.life <= 0:
            print('You kill the monster.')
            MessageLog.add_message('You kill the monster.')
            self._monster_reward()
        self.generation.update_character()
        if self.player.life <= 0:
            print('Youre defeated.')
            MessageLog.add_message('Youre defeated.')
            battle_heal = threading.Thread(target=self.battle_healing_loop)
            battle_heal.start()
            battle_heal.join()
        if not self.batte_active:
            return True
        else:
            return False
    
    def training_loop(self,choice:str):
        while self.batte_active:
            train_thread = threading.Thread(target=self.training_atributes_loop,args=(choice,))
            keyboard_thread = threading.Thread(target=self.keyboard_control)
            keyboard_thread.start()
            train_thread.start()
            train_thread.join()
            if self.player.life <= 0:
                battle_heal = threading.Thread(target=self.battle_healing_loop)
                battle_heal.start()
                battle_heal.join()
        
    def training_atributes_loop(self,choice:str):
        while self.batte_active:
            sum_atributes = self.player.strength + self.player.agility + self.player.vitality + self.player.intelligence + self.player.charisma
            if sum_atributes >= self.player.atribute_cap:
                print('You reach the training cap.')
                MessageLog.add_message('You reach the training cap.')
                self.batte_active = False
                break
            train = self.get_random_float_interval((0, 0.2))
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
            if self.player.life <= 0:
                break
            time.sleep(1)
            print(f'You train {train:.2f} points of {text}.')
            MessageLog.add_message(f'You train {train:.2f} points of {text}.')
            self.generation.update_character()
            
    def healing_sleep_loop(self):
        print('runing sleeping loop')
        while self.player.life < self.player.max_life or self.player.mana < self.player.max_mana:
            random_heal = self.get_random_in_interval((1,5))
            heal = random_heal + (self.player.vitality/2)
            mana_regen = random_heal / 10 + (self.player.intelligence/2)
            self.player.life = self.player.life + heal
            self.player.mana = self.player.mana + mana_regen
            if self.player.life > self.player.max_life:
                self.player.life = self.player.max_life
            if self.player.mana > self.player.max_mana:
                self.player.mana = self.player.max_mana
            print(f'You heal {heal:.2f} points of life, HP: {self.player.life:.2f}/{self.player.max_life}')
            print(f'You heal {mana_regen:.2f} points of mana, MANA: {self.player.mana:.2f}/{self.player.max_mana}')
            MessageLog.add_message(f'You heal {heal:.2f} points of life, HP: {self.player.life:.2f}/{self.player.max_life}')
            MessageLog.add_message(f'You heal {mana_regen:.2f} points of mana, MANA: {self.player.mana:.2f}/{self.player.max_mana}')
            time.sleep(1)
        MessageLog.add_message(f'you are full life')
        
