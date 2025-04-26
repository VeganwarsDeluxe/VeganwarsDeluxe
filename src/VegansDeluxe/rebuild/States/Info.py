from VegansDeluxe.core import AttachedAction
from VegansDeluxe.core import Entity
from VegansDeluxe.core import OwnOnly
from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core import StateContext
from VegansDeluxe.core.Actions.StateAction import InstantStateAction
from VegansDeluxe.core.Question.Question import Question
from VegansDeluxe.core.Question.QuestionEvents import QuestionGameEvent
from VegansDeluxe.core.Translator.LocalizedList import LocalizedList
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild import DamageThreshold


class Info(State):
    id = 'info'


@RegisterState(Info)
async def register(root_context: StateContext[Info]):
    session: Session = root_context.session
    state = root_context.state


@AttachedAction(Info)
class InfoAction(InstantStateAction):
    id = 'info'
    name = ls("rebuild.skill.info.action.name")
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, state: Info):
        super().__init__(session, source, state)
        self.state = state

    @property
    def hidden(self) -> bool:
        return False

    async def func(self, source: Entity, target: Entity):
        visor_message = Question(text=ls("rebuild.skill.visor.message").format(
            player_name=target.name,
            hp_emojies=target.hearts,
            hp=target.hp,
            max_hp=target.max_hp,

            energy_emojies=target.energies,
            energy=target.energy,
            max_energy=target.max_energy,

            damage_threshold=target.get_state(DamageThreshold).threshold,
            skill_names=LocalizedList([s.name for s in target.skills]),

            weapon_name=target.weapon.name,
            energy_cost=target.weapon.energy_cost,
            hit_chance=target.hit_chance,

            notifications=LocalizedList(target.notifications, separator="\n")
        ))
        await self.session.event_manager.publish(
            QuestionGameEvent(self.session.id, self.session.turn, source.id, visor_message)
        )

        self.state.cooldown_turn = self.session.turn + 3
