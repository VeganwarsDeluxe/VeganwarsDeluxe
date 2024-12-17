from VegansDeluxe.core import Session, RegisterEvent
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import ls, RegisterState
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.rebuild.Items.FlashGrenade import FlashGrenadeAttemptEvent
from VegansDeluxe.rebuild.States.Aflame import Aflame


class GasMask(Skill):
    id = 'gas-mask'
    name = ls("rebuild.skill.gas_mask.name")
    description = ls("rebuild.skill.gas_mask.description")


@RegisterState(GasMask)
async def register(root_context: StateContext[GasMask]):
    session: Session = root_context.session
    source = root_context.entity

    source.get_state(Aflame).burn_time -= 1

    source.max_energy += 1
    source.energy += 1

    @RegisterEvent(session.id, event=FlashGrenadeAttemptEvent, priority=-1)
    async def attack_handler(actions_context: EventContext[FlashGrenadeAttemptEvent]):
        if actions_context.event.target != source:
            return

        actions_context.event.success = False
        actions_context.event.energy_lost = 1
