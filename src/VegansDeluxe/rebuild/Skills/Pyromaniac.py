from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import ls, RegisterState, At, AttackGameEvent, PreDamagesGameEvent
from VegansDeluxe.core.Entities.Entity import Entity
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.rebuild.States.Aflame import Aflame


class Pyromaniac(Skill):
    id = 'pyromaniac'
    name = ls("rebuild.skill.pyromaniac.name")
    description = ls("rebuild.skill.pyromaniac.description")


@RegisterState(Pyromaniac)
async def register(root_context: StateContext[Pyromaniac]):
    session: Session = root_context.session
    source = root_context.entity

    @At(session.id, turn=session.turn, event=AttackGameEvent)
    async def attack_handler(actions_context: EventContext[AttackGameEvent]):
        if actions_context.event.source != source:
            return

        damage_bonus = get_bonus(session, source)

        if actions_context.event.damage:
            actions_context.event.damage += damage_bonus

        @At(session.id, turn=session.turn, event=PreDamagesGameEvent)
        async def post_actions(damages_context: EventContext[PreDamagesGameEvent]):
            session.say(ls("rebuild.skill.pyromaniac.effect").format(source.name, damage_bonus))


def get_bonus(session: Session, source: Entity):
    bonus = 0
    for entity in session.entities:
        if entity.is_ally(source):
            continue
        aflame = entity.get_state(Aflame.id)
        if aflame.flame:
            bonus += 1
    return bonus
