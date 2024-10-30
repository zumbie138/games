
class ConjuringSpell():
    def __init__(self):
        self.spells_cooldown = {}
        self.spells_duration = {}
        
    def add_spell_timers(self, name:str, cooldown:int, duration:int):
        self.spells_cooldown[name] = cooldown
        self.spells_duration[name] = duration
    
    def _decrement_and_clean(self,spell_timer:dict):
        for spell in list(spell_timer.keys()):
            spell_timer[spell] -= 1
            if spell_timer[spell] <= 0:
                del spell_timer[spell]
    
    def update_spell_timer(self):
        self._decrement_and_clean(self.spells_cooldown)
        self._decrement_and_clean(self.spells_duration)
        
    def conjure_passive(self):
        print('')
        
    def conjure_offensive(self):
        print('')
        
    def conjure_buff(self):
        print('')
        
    def conjure_healing(self):
        print('')
