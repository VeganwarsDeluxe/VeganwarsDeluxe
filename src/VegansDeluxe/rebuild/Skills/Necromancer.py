import random

from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core import AttachedAction, Next, DeliveryPackageEvent, DeliveryRequestEvent, ActionTag, Aliveness
from VegansDeluxe.core import RegisterEvent, RegisterState, After, At
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import Entity
from VegansDeluxe.core import PreDeathGameEvent, PostDamagesGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core import Everyone
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.States.Stun import Stun


class Necromancer(Skill):
    id = 'necromancer'
    name = ls("skill_necromancer_name")
    description = ls("skill_necromancer_description")

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0


@RegisterState(Necromancer)
async def register(root_context: StateContext[Necromancer]):
    session: Session = root_context.session
    source = root_context.entity
    state: Necromancer = root_context.state


@AttachedAction(Necromancer)
class RaiseUndead(DecisiveStateAction):
    id = 'raise_undead'
    name = ls("skill_necromancer_action_name")
    priority = 2
    target_type = Everyone(aliveness=Aliveness.DEAD_ONLY)

    def __init__(self, session: Session, source: Entity, skill: Necromancer):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    async def func(self, source: Entity, target: Entity):
        self.state.cooldown_turn = self.session.turn + 3

        target.dead = False
        target.hp = 1
        self.session.say(ls("skill_necromancer_action_text").format(source.name, target.name))
