import random

from VegansDeluxe.core import NPC, Session, ActionManager
from VegansDeluxe.rebuild.Items.Molotov import MolotovAction, Molotov


class FireAutomaton(NPC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hp = 2
        self.max_hp = 2

        self.name = "⛽️|FireAutomaton"
        self.items.append(Molotov())

    async def choose_act(self, session: Session, action_manager: ActionManager):
        ma = MolotovAction(session, self, self.items[0])
        ma.target = random.choice(ma.targets)
        action_manager.queue_action_instance(ma)
