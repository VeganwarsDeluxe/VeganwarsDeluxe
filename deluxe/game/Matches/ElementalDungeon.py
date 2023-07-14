from deluxe.game.Entities.Elementalis import Elemental
from deluxe.game.Matches.BasicMatch import BasicMatch


class ElementalDungeon(BasicMatch):
    name = "Данж с Елементалем"

    def __init__(self, chat_id):
        super().__init__(chat_id)

        self.elementals = 0

    def join_session(self, user_id, user_name):
        player = super().join_session(user_id, user_name)
        player.team = 'players'
        if self.elementals == 1:
            return

        self.elementals += 1
        self.session.entities.append(Elemental(self.id, name=f'Веган Елементаль {self.elementals}|🌪'))
