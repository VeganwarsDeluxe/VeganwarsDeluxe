import random

from VegansDeluxe.core import StateContext, Next, EventContext, AttachedAction, DecisiveStateAction, FreeStateAction, \
    OwnOnly, Entity, DeliveryPackageEvent, DeliveryRequestEvent
from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core.Question.Choice import Choice
from VegansDeluxe.core.Question.Question import Question
from VegansDeluxe.core.Question.QuestionEvents import QuestionGameEvent, AnswerGameEvent
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild import all_weapons


class Weaponsmith(Skill):
    id = 'weaponsmith'
    name = ls("skill_weaponsmith_name")
    description = ls("skill_weaponsmith_description")

    weapon_pool = all_weapons

    def __init__(self):
        super().__init__()
        self.other_weapon = None


@RegisterState(Weaponsmith)
def register(root_context: StateContext[Weaponsmith]):
    session: Session = root_context.session
    source = root_context.entity

    pool = []
    weapon_choice = Question(text=ls("skill_weaponsmith_choice_text"))
    for i in range(3):
        weapon = random.choice(root_context.state.weapon_pool)
        pool.append(weapon_choice)
        choice = Choice(choice_id=str(i), text=weapon.name)
        weapon_choice.choices.append(choice)

    session.event_manager.publish(QuestionGameEvent(session.id, session.turn, source.id, weapon_choice))

    @Next(session.id, event=AnswerGameEvent, filters=[lambda e: e.question.id == weapon_choice.id])
    def answer(context: EventContext[AnswerGameEvent]):
        chosen_weapon_index = int(context.event.choice_id)
        chosen_weapon = pool[chosen_weapon_index]

        root_context.state.other_weapon = chosen_weapon


@AttachedAction(Weaponsmith)
class SwitchWeapon(FreeStateAction):
    id = 'switch_weapon'
    name = ls("skill_weaponsmith_action_name")
    priority = -3
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, skill: Weaponsmith):
        super().__init__(session, source, skill)
        self.state = skill

    def func(self, source: Entity, target: Entity):
        other_weapon = self.state.other_weapon

        self.state.other_weapon = source.weapon
        source.weapon = other_weapon

        @Next(self.session.id, event=DeliveryPackageEvent)
        def delivery(context: EventContext[DeliveryPackageEvent]):
            action_manager = context.action_manager
            action_manager.update_entity_actions(self.session, source)
        self.event_manager.publish(DeliveryRequestEvent(self.session.id, self.session.turn))

        self.session.say(ls("skill_weaponsmith_action_text").format(source.name, other_weapon.name))
