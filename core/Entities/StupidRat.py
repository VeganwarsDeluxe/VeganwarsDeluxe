from .Player import Player
import random


class StupidRat(Player):
    def __init__(self, session, name):
        super().__init__(session, name)

    def choose_action(self):
        while random.randint(1, 100) > 50:
            if self.weapon.free_actions:
                random.choice(self.weapon.free_actions)(self, random.choice(self.targets) if self.targets else self)
        if self.energy != self.max_energy:
            self.action, self.action_priority = self.reload, 0
        if not self.approached:
            self.action, self.action_priority = self.approach, 4
        if not self.dodge_cooldown and self.nearby_entities and random.randint(1, 100) > 50:
            self.action, self.action_priority = self.dodge, 0
        elif self.targets and self.energy > 0:
            self.action, self.action_priority = lambda: self.attack(random.choice(self.targets)), 3
        # self.say(f'I choose {self.action} with {self.action_priority} priority.')