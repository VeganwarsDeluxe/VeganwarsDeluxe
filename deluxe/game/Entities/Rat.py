import random

import rebuild
from deluxe.game.Entities.Dummy import Dummy


class Rat(Dummy):
    def __init__(self, session_id: str, name='Крыса|🐭'):
        super().__init__(session_id, name=name)

        self.hp = 4
        self.max_hp = 4
        self.energy = 5
        self.max_energy = 5

        self.items = []

        for _ in range(2):
            self.skills.append(random.choice(rebuild.all_skills)())

        self.weapon = random.choice(rebuild.all_weapons)(session_id, self.id)

        self.team = None

    def choose_act(self, session):
        super().choose_act(session)
