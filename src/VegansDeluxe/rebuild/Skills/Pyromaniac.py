from VegansDeluxe.core import Session, RegisterEvent, AttachedAction, Allies, DecisiveStateAction, FreeStateAction, \
    Selfishness, Enemies, Distance
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import ls, RegisterState, AttackGameEvent, PreDamagesGameEvent
from VegansDeluxe.core.Entities.Entity import Entity
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.utils import per_cubes
from VegansDeluxe.rebuild.States.Aflame import Aflame


class Pyromaniac(Skill):
    id = 'pyromaniac'
    name = ls("rebuild.skill.pyromaniac.name")
    description = ls("rebuild.skill.pyromaniac.description")

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0


@RegisterState(Pyromaniac)
async def register(root_context: StateContext[Pyromaniac]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=AttackGameEvent)
    async def attack_handler(actions_context: EventContext[AttackGameEvent]):
        if actions_context.event.source != source:
            return

        damage_bonus = get_bonus(session, source)

        if actions_context.event.damage:
            actions_context.event.damage += damage_bonus

        if not damage_bonus or not actions_context.event.damage:
            return
        session.say(ls("rebuild.skill.pyromaniac.effect").format(source.name, damage_bonus),
                    at_next_event=PreDamagesGameEvent)

@AttachedAction(Pyromaniac)
class IgniteEnemy(DecisiveStateAction):
    id = 'ignite_enemy'
    name = ls("rebuild.skill.pyromaniac.ingite_enemy.name")
    priority = -3
    target_type = Enemies(distance=Distance.NEARBY_ONLY)

    def __init__(self, session: Session, source: Entity, skill: Pyromaniac):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    async def func(self, source, target):
        self.state.cooldown_turn = self.session.turn + 3
        if not per_cubes(1, 4, source.energy, source.outbound_accuracy_bonus+target.inbound_accuracy_bonus):
            self.session.say(ls("rebuild.skill.pyromaniac.ignite_miss.text").format(self.source.name, self.target.name))
            return
        self.session.say(ls("rebuild.skill.pyromaniac.ignite.text").format(self.source.name, self.target.name))
        self.target.get_state(Aflame).add_flame(self.session, target, source, 1)


@AttachedAction(Pyromaniac)
class IgniteAlly(FreeStateAction):
    id = 'ignite_ally'
    name = ls("rebuild.skill.pyromaniac.ingite_ally.name")
    priority = -3
    target_type = Allies(own=Selfishness.SELF_INCLUDED)

    def __init__(self, session: Session, source: Entity, skill: Pyromaniac):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return False

    async def func(self, source, target):
        self.session.say(ls("rebuild.skill.pyromaniac.ignite.text").format(self.source.name, self.target.name))
        self.target.get_state(Aflame).add_flame(self.session, target, source, 1)



def get_bonus(session: Session, source: Entity):
    bonus = 0
    for entity in session.entities:
        entity: Entity

        aflame = entity.get_state(Aflame)
        if aflame.flame:
            bonus += 1
    return bonus
