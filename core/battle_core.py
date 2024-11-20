from database import GameBase
from core import ConjuringSpell, GameCore
import time
import random
import threading

class BattleCore(GameBase):
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.game_core = GameCore()
        self.conjuring_spell = ConjuringSpell()
    
    def _damage_calculator(self,attack:float,defense:float,level:int)->float:
        damage = ((level * 5) / 10) + ((attack**2) / (attack + (2*defense)))
        min_damage = damage * 0.7
        max_damage = damage * 1.3
        final_damage = random.uniform(min_damage, max_damage)
        return final_damage
    
    def _apply_buff(self, buff: tuple, multiplier: int):
        attributes = ['strength', 'agility', 'vitality', 'intelligence', 'charisma']
        for attr, value in zip(attributes, buff):
            setattr(self.buffs, attr, getattr(self.buffs, attr) + value * multiplier)

    def remove_buff(self, buff_removed:tuple):
        self._apply_buff(buff_removed, -1)
    
    def add_buff(self, buff_added:tuple):
        self._apply_buff(buff_added, 1)
    
    def player_battle_loop(self):
        while self.player.life > 0 and self.monster.life > 0:
            self.conjuring_core(self.player.spells, self.player.intelligence, self.player.charisma)
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

        if self.player.life <= 0:
            print('Youre defeated.')
            return True
        else:
            print('You kill the monster.')
            self.monster_reward()
            return False
        
        