from database import GameBase, GameRepository
from .generation_core import GenerationCore

class ConjuringSpell(GameBase):
    def __init__(self):
        self.df_spells = self.get_database_dataframe('spells_database.json')
        self.repository = GameRepository()
        self.generation = GenerationCore()
        self.attributes = ['strength', 'agility', 'vitality', 'intelligence', 'charisma']
        self.spells_cooldown = {}
        self.spells_duration = {}
    
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
    def buffs(self):
        return self.repository.get_resource('Buffs')
    @buffs.setter
    def buffs(self, value):
        self.repository.set_resource('Buffs', value)
    
    def add_spell_timers(self, name:str, cooldown:int, duration:int):
        self.spells_cooldown[name] = cooldown
        count = sum(1 for key in self.spells_duration if key.startswith(name))
        self.spells_duration[f'{name}{count+1}'] = duration
    
    def _decrement_and_clean(self,spell_timer:dict):
        for spell in list(spell_timer.keys()):
            spell_timer[spell] -= 1
    
    def check_duration_spell(self):
        for spell in list(self.spells_duration.keys()):
            if self.spells_duration[spell] <= 0:
                del self.spells_duration[spell]
                return spell.rstrip("0123456789")
    
    def update_spell_timer(self):
        self._decrement_and_clean(self.spells_cooldown)
        self._decrement_and_clean(self.spells_duration)
        
    def calculate_conjured_spell(self,damage_base:int, healing_base:int, vitality:float, intelligence:float, charisma:float):
        spell_damage = damage_base * (1 + (((intelligence  +(charisma/2)) * 3) / 10))
        healing_done = healing_base * (1 + (((intelligence + (vitality/2) + (charisma/5)) * 3) / 10))
        final_damage = self.get_random_min_max(spell_damage)
        final_healing = self.get_random_min_max(healing_done)
        return final_damage, final_healing
        
    def check_active_durations(self):
        self.update_spell_timer()
        effect_over = self.check_duration_spell()
        if effect_over is not None:
            buff_removed = self.get_info_by_name(effect_over,'name','buff',self.df_spells)
            # print(buff_removed)
            # print(self.buffs)
            self.remove_buff(buff_removed)
            self.generation.update_character()
    
    def reset_buffs(self):
        self.spells_cooldown = {}
        self.spells_duration = {}
        for attr in self.attributes:
            setattr(self.buffs, attr, 0)
            
    def _apply_buff(self, buff: tuple, multiplier: int):
        for attr, value in zip(self.attributes, buff):
            setattr(self.buffs, attr, getattr(self.buffs, attr) + value * multiplier)

    def remove_buff(self, buff_removed:tuple):
        self._apply_buff(buff_removed, -1)
    
    def add_buff(self, buff_added:tuple):
        self._apply_buff(buff_added, 1)
        
    def conjuring_core(self,spell_list:list,inteligence:float,charisma:float):
        for spell in reversed(spell_list):
            spell_info = self.filter_dataframe_by_name(spell,'name',self.df_spells)
            rate = spell_info['rate'].item()
            mana_spell = spell_info['mana'].item()
            if spell in self.spells_cooldown:
                cooldown = self.spells_cooldown[spell]
            else:
                cooldown = 0
            if cooldown <= 0:
                if self.player.mana >= mana_spell:
                    final_rate = rate + charisma*1.3 + inteligence*0.3
                    roll_dice = self.get_random_in_interval((0, 100))
                    if roll_dice <= final_rate:
                        print(f'You conjure {spell} !')
                        self.conjure_spell(spell, spell_info)
                        break
                
    def conjure_spell(self, spell_name:str, spell_info):
        mana_spell = spell_info['mana'].item()
        damage_base = spell_info['damage'].item()
        heal_base = spell_info['heal'].item()
        spell_cooldown = spell_info['cooldown'].item()
        spell_duration = spell_info['duration'].item()
        buff_tuple = spell_info['buff'].item()
        self.add_spell_timers(spell_name, spell_cooldown, spell_duration)
        self.player.mana = self.player.mana - mana_spell
        if spell_info['type'].item() == 'passive' or spell_info['type'].item() == 'buff':
            self.add_buff(buff_tuple)
            # print(buff_tuple)
            # print(self.buffs)
            self.generation.update_character()
        elif spell_info['type'].item() == 'offensive' or spell_info['type'].item() == 'healing':
            spell_result = self.calculate_conjured_spell(damage_base,heal_base,self.player.vitality,self.player.intelligence,self.player.charisma)           
            self.apply_magic_damage(*spell_result)
    
    def apply_turn_damage(self):
        for key, item in self.spells_duration.items():
            key = key.rstrip("0123456789")
            spell = self.filter_dataframe_by_name(key, 'name', self.df_spells)
            turn_damage_base = spell['turn_damage'].item()
            turn_heal_base = spell['turn_heal'].item()
            turn_damage, turn_heal = self.calculate_conjured_spell(turn_damage_base, turn_heal_base,
                                                                   self.player.vitality, self.player.intelligence,
                                                                   self.player.charisma)
            if turn_damage > 0:
                self.monster.life -= turn_damage
                print(f'Your spell deal {turn_damage:.2f} hits points and will last {item} turns.')
            if turn_heal > 0:
                self.player.life -= turn_heal
                print(f'Your spell heal {turn_heal:.2f} hits points and will last {item} turns.')
            
    def apply_magic_damage(self,magic_damage:float, healing_done:float):
        self.monster.life = self.monster.life - magic_damage
        self.player.life = self.player.life + healing_done
        if self.player.life > self.player.max_life:
            self.player.life = self.player.max_life
        if magic_damage > 0:
            print(f'Your magic deals {magic_damage:.2f} hit points.')
        if healing_done > 0:
            print(f'You heal yourself {healing_done:.2f} hit points.')
