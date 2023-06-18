from core.Entities.Entity import Entity
from modern import all_states


class TelegramEntity(Entity):
    def __init__(self, session, user_name, user_id):
        super().__init__(session)
        self.init_states()

        self.id = user_id
        self.name = user_name
        self.npc = False                                   # to differentiate humans and bots

        self.chose_weapon = False
        self.chose_skills = False
        self.skill_cycle = 0
        self.chose_items = False
        self.ready = False

    def choose_act(self):  # method for AI
        pass

    def init_states(self):
        for state in all_states:
            self.skills.append(state(self))

    def pre_move(self):
        super().pre_move()
        if not self.dead:
            self.ready = False
