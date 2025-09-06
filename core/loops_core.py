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
        
        #variaveis de timer
        self.training_timer = 0
        self.healing_timer = 0
        self.combat_timers = {
            'player': 0,
            'monster': 0,
            'buffs': 0
        }
        self.combar_speed = {
            'player': 0,
            'monster': 0
        }
        self.current_turn = 0
        
        #variaveis de constantes de escolhas
        self.training_attribute = None
        self.monster_location = None
        self.monster_df = self.get_database_dataframe('monster_database.json')
        self.locations_df = self.get_database_dataframe('locations_database.json')
        
        #criando variaveis de controle
        self.training_active = False
        self.battle_active = False
        self.healing_active = False
    
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

    def _monster_encounter(self):
        monster_rate = self.get_info_by_name(self.monster_location,'name',
                                                         'monsters',self.locations_df)
        monster_name = self.get_name_by_rate_probability(monster_rate)
        monster_info = self.monster_df[self.monster_df['name'] == monster_name]
        monster_info_tuple = self.dataframe_to_tuple(monster_info)
        self.generation.generate_monster(monster_info_tuple)
        MessageLog.add_message(f'You will face a {self.monster.name}')
        self.battle_active = True
    
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
 
    def _update_buffs(self):
        self.conjuring_spell.check_active_durations()
        self.conjuring_spell.apply_turn_damage()

    def  _player_attack(self):
        player_damage = self._damage_calculator(
            self.player.attack,
            self.monster.defense,
            self.player.level
        )
        self.monster.life -= player_damage
        MessageLog.add_message(f'You deal {player_damage:.2f} damage.')

    def _monster_attack(self):
        monster_damage = self._damage_calculator(
            self.monster.attack,
            self.monster.defense,
            self.monster.level
        )
        self.player.life -= monster_damage
        MessageLog.add_message(f'You take {monster_damage:.2f} damage.')

    def _check_combat_end(self):
        if self.monster.life <=0:
            MessageLog.add_message('You kill the monster.')
            self._monster_reward()
            self.battle_active = False
            self.conjuring_spell.reset_buffs()
        if self.player.life <= 0:
            MessageLog.add_message('Youre defeated.')
            self.battle_active = False
            self.healing_active = True
            self.conjuring_spell.reset_buffs()

    def update_combat_loop(self, dt):
        if not self.battle_active and not self.healing_active:
            self.current_turn = 0
            self._monster_encounter()

        if not self.healing_active:
            self.combat_timers['player'] += dt
            self.combat_timers['monster'] += dt
            self.combat_timers['buffs'] += dt

            if self.combat_timers['player'] >= self.player.attack_speed:
                self.conjuring_spell.conjuring_core(self.player.spells, self.player.intelligence, self.player.charisma)
                self._player_attack()
                self.combat_timers['player'] = 0

            if self.combat_timers['monster'] >= self.monster.attack_speed:
                self._monster_attack()
                self.combat_timers['monster'] = 0

            if self.combat_timers['buffs'] >= 5.0:
                self._update_buffs()
                self.combat_timers['buffs'] = 0
                self.current_turn += 1
                MessageLog.add_message(f'Turn {self.current_turn} ends.')

            self._check_combat_end()
        if self.healing_active:
            self.update_healing(dt, 'passive')
            
            
    def _healing_tick(self, divisor):
        random_heal = self.get_random_in_interval((1,5))
        heal = random_heal + (self.player.vitality/divisor)
        mana_regen = random_heal / 10 + (self.player.intelligence/divisor)

        self.player.life = min(self.player.max_life, self.player.life + heal)
        self.player.mana = min(self.player.max_mana, self.player.mana + mana_regen)

        self.generation.update_character()
        MessageLog.add_message(f'You heal {heal:.2f} points of life, HP: {self.player.life:.2f}/{self.player.max_life}')
        MessageLog.add_message(f'You heal {mana_regen:.2f} points of mana, MANA: {self.player.mana:.2f}/{self.player.max_mana}')

    def update_healing(self, dt, type:str):
        healing_settings = {
            'active':{'time':1, 'divisor':2},
            'passive':{'time':2.5, 'divisor':4}
        }
        settings = healing_settings[type]

        if not self.healing_active:
            return 0

        self.healing_timer += dt

        if self.healing_timer >= settings['time']:
            self.healing_timer = 0
            self._healing_tick(settings['divisor'])

        if self.player.life == self.player.max_life and self.player.mana == self.player.max_mana:
            MessageLog.add_message(f'Your health and mana are full')
            self.healing_active = False
            if type == 'active':
                return 0
        if type == 'active':
            return 3

    def _trainig_tick(self):
        train = self.get_random_float_interval((0, 0.2))
        setattr(self.player, self.training_attribute, 
                getattr(self.player, self.training_attribute)  + train)
        self.player.life = max(self.player.life - 10, 0)
        self.generation.update_character()
        MessageLog.add_message(f'You train {train:.2f} points of {self.training_attribute}.')  

    def update_training_loop(self, dt): 
        sum_attributes = self.player.strength + self.player.agility + self.player.vitality + self.player.intelligence + self.player.charisma
        if sum_attributes >= self.player.atribute_cap:
            MessageLog.add_message('You reach the training cap.')
            self.training_active = False

        if not self.training_active:
            return 0

        if self.player.life <= 0:
            self.healing_active = True
        if self.healing_active:
            self.update_healing(dt, 'passive')

        self.training_timer += dt

        if self.training_timer >= 1.0 and not self.healing_active:
            self.training_timer = 0
            self._trainig_tick()
            return 2
        
        return 2