from deluxe.game.Entities.Elementalis import Elemental
from deluxe.game.Matches.BasicMatch import BasicMatch


class ElementalDungeon(BasicMatch):
    name = "Командная игра"

    def __init__(self, chat_id):
        super().__init__(chat_id)

        self.elementals = 0

