from VegansDeluxe.core import AttackGameEvent, Entity
from VegansDeluxe.core import PreMoveGameEvent, HPLossGameEvent
from VegansDeluxe.core import RegisterEvent
from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core.Skills.Skill import Skill, SkillTag
from VegansDeluxe.core.Translator.LocalizedString import ls


class Berserk(Skill):
    id = 'berserk'
    name = ls("rebuild.skill.berserk.name")
    description = ls("rebuild.skill.berserk.description")

    tags = Skill.tags + [SkillTag.MELEE_WEAPON_ONLY]

    def __init__(self):
        super().__init__()
        self.base = None


@RegisterState(Berserk)
async def register(root_context: StateContext[Berserk]):
    session: Session = root_context.session
    source: Entity = root_context.entity
    state: Berserk = root_context.state

    @RegisterEvent(session.id, PreMoveGameEvent, priority=1)
    async def pre_actions(context: EventContext[PreMoveGameEvent]):
        new_base = max(7 - source.hp, 2)

        if state.base is None:
            bonus = source.max_energy - source.base_max_energy
            source.max_energy = new_base + bonus
        else:
            source.max_energy += new_base - state.base

        state.base = new_base

        if context.event.turn == 1:
            source.energy = source.max_energy
        else:
            source.energy = min(source.energy, source.max_energy)

    @RegisterEvent(session.id, event=HPLossGameEvent, priority=2)
    async def hp_loss(context: EventContext[HPLossGameEvent]):
        if context.event.source != source:
            return
        source.max_energy += context.event.hp_loss
        source.energy = min(source.energy + context.event.hp_loss, source.max_energy)
        session.say(ls("rebuild.skill.berserk.effect").format(source.name, context.event.hp_loss))
        if source.hp-context.event.hp_loss == 1:
            session.say(ls("rebuild.skill.berserk.trance").format(source.name))

    @RegisterEvent(session.id, event=AttackGameEvent)
    async def attack_handler(attack_context: EventContext[AttackGameEvent]):
        if attack_context.event.source != source:
            return
        if source.hp != 1:
            return
        if attack_context.event.damage:
            attack_context.event.damage += 2
