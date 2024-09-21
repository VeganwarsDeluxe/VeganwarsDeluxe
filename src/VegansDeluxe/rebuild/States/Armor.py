from VegansDeluxe.core import Entity
from VegansDeluxe.core import PostDamageGameEvent
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import percentage_chance
from VegansDeluxe.core.Translator.LocalizedString import ls


class Armor(State):
    id = 'armor'

    def __init__(self):
        super().__init__()
        self.armor = []

    def negate_damage(self, session: Session, source: Entity, message: PostDamageGameEvent):
        if not message.damage:
            return
        armor = min(message.damage, self.roll_armor())
        if not armor:
            return
        session.say(ls("rebuild.state.armor.effect").format(source.name, armor))
        message.damage -= armor

    def add(self, value: int, chance=100):
        self.armor.append((value, chance))

    def remove(self, armor):
        if armor in self.armor:
            self.armor.remove(armor)

    def roll_armor(self):
        result = 0
        for armor, chance in self.armor:
            for _ in range(armor):
                if percentage_chance(chance):
                    result += 1
        return result


@RegisterState(Armor)
async def register(root_context: StateContext[Armor]):
    session: Session = root_context.session
    source = root_context.entity
    state = root_context.state

    @RegisterEvent(session.id, event=PostDamageGameEvent)
    async def func(context: EventContext[PostDamageGameEvent]):
        if context.event.target == source:
            state.negate_damage(session, source, context.event)
