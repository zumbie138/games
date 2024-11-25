from database import GameBase, GameRepository
from .spells_core import ConjuringSpell
from .game_core import GameCore
import time
import random
import threading

class BattleCore(GameBase):
    def __init__(self):
        self.game_core = GameCore()
        self.conjuring_spell = ConjuringSpell()
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
    
    def _damage_calculator(self,attack:float,defense:float,level:int)->float:
        damage = ((level * 5) / 10) + ((attack**2) / (attack + (2*defense)))
        final_damage = self.get_random_min_max(damage)
        return final_damage
    
    def player_battle_loop(self):
        while self.player.life > 0 and self.monster.life > 0:
            self.conjuring_spell.conjuring_core(self.player.spells, self.player.intelligence, self.player.charisma)
            player_damage = self._damage_calculator(self.player.attack,self.monster.defense,self.player.level)
            self.monster.life = self.monster.life - player_damage
            time.sleep(self.player.attack_speed)
            print(f'You deal {player_damage:.2f} damage.')
            
    def monster_battle_loop(self):
        while self.monster.life > 0 and self.player.life > 0:
            monster_damage = self._damage_calculator(self.monster.attack, self.player.defense, self.monster.level)
            self.player.life = self.player.life - monster_damage
            self.player.life = max(self.player.life, 0)
            time.sleep(self.monster.attack_speed)
            print(f'You take {monster_damage:.2f} damage.')
            
    def battle_turn_loop(self):
        turn = 1
        while True:
            if self.player.life <= 0:
                break
            elif self.monster.life <= 0:
                break
            else:
                self.conjuring_spell.check_active_durations()
                time.sleep(5)
                print(f'Turn {turn} ends.')
                turn +=1
                
    def _apply_turn_damage(self):
        self.conjuring_spell.spells_duration
    
    def battle_status(self)->bool:
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
        self.game_core.update_character()
        if self.player.life <= 0:
            print('Youre defeated.')
            self.conjuring_spell.reset_buffs()
            return True
        else:
            print('You kill the monster.')
            self.conjuring_spell.reset_buffs()
            self.game_core.monster_reward()
            return False
        
        