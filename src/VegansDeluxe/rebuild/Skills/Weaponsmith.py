import random

from VegansDeluxe.core import RegisterState, Weapon, PreActionsGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext, Next, EventContext, AttachedAction, OwnOnly, Entity, DeliveryPackageEvent, \
    DeliveryRequestEvent
from VegansDeluxe.core.Actions.StateAction import InstantStateAction
from VegansDeluxe.core.Question.Choice import Choice
from VegansDeluxe.core.Question.Question import Question
from VegansDeluxe.core.Question.QuestionEvents import QuestionGameEvent, AnswerGameEvent
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild import all_weapons, Fist


class Weaponsmith(Skill):
    id = 'weaponsmith'
    name = ls("rebuild.skill.weaponsmith.name")
    description = ls("rebuild.skill.weaponsmith.description")

    weapon_pool = all_weapons.copy()
    weapon_pool.remove(Fist)

    def __init__(self):
        super().__init__()
        # TODO: This is literally late init. Ideas?
        #  Even worse. Come on, not in rebuild module.
        self.other_weapon: Weapon = Fist("", "")
        self.last_switch_turn = -1


@RegisterState(Weaponsmith)
async def register(root_context: StateContext[Weaponsmith]):
    session: Session = root_context.session
    source = root_context.entity

    root_context.state.weapon_pool = [w for w in root_context.state.weapon_pool if w.id != source.weapon.id]
    root_context.state.other_weapon = Fist(session.id, source.id)

    weapon_pool: list[type[Weapon]] = []
    weapon_choice = Question(text=ls("rebuild.skill.weaponsmith.choice.text"))
    for i in range(3):
        choice_pool = [w for w in root_context.state.weapon_pool if w not in weapon_pool]
        if not choice_pool:
            continue
        weapon = random.choice(choice_pool)
        weapon_pool.append(weapon)
        choice = Choice(choice_id=str(i), text=weapon.name,
                        result_text=ls("rebuild.skill.weaponsmith.choice.result_text").format(weapon.name))
        weapon_choice.add_choice(choice)

    await session.event_manager.publish(QuestionGameEvent(session.id, session.turn, source.id, weapon_choice))

    @Next(session.id, event=AnswerGameEvent, filters=[lambda e: e.question_id == weapon_choice.id])
    async def answer(context: EventContext[AnswerGameEvent]):
        chosen_weapon_index = int(context.event.choice_id)
        chosen_weapon = weapon_pool[chosen_weapon_index](source.session_id, source.id)

        root_context.state.other_weapon = chosen_weapon


@AttachedAction(Weaponsmith)
class SwitchWeapon(InstantStateAction):
    id = 'switch_weapon'
    name = ls("rebuild.skill.weaponsmith.action.name")
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, skill: Weaponsmith):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.state.last_switch_turn == self.session.turn

    async def func(self, source: Entity, target: Entity):
        other_weapon = self.state.other_weapon
        if not other_weapon:
            return

        self.state.other_weapon = source.weapon
        source.weapon = other_weapon

        @Next(self.session.id, event=DeliveryPackageEvent)
        async def delivery(context: EventContext[DeliveryPackageEvent]):
            action_manager = context.action_manager
            await action_manager.update_entity_actions(self.session, source)
        await self.event_manager.publish(DeliveryRequestEvent(self.session.id, self.session.turn))

        @Next(self.session.id, event=PreActionsGameEvent, priority=-10)
        async def answer(context: EventContext[AnswerGameEvent]):
            self.session.say(ls("rebuild.skill.weaponsmith.action.text").format(source.name, other_weapon.name))


