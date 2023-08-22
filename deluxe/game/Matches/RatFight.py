from deluxe.game.Entities.Rat import Rat
from deluxe.game.Matches.BasicMatch import BasicMatch


class RatDungeon(BasicMatch):
    name = "Данж с крысами"

    def __init__(self, chat_id):
        super().__init__(chat_id)

        self.rats = 0

    def join_session(self, user_id, user_name):
        player = super().join_session(user_id, user_name)
        player.team = 'players'

        self.rats += 1
        rat = Rat(self.id, name=f'Крыса {self.rats}|🐭')
        rat.team = 'rats'
        self.session.entities.append(rat)
