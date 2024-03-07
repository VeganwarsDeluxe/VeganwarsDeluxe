from VegansDeluxe.core import AttachedAction, RegisterItem
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import At
from VegansDeluxe.core import Item
from VegansDeluxe.core import FreeItem
from VegansDeluxe.core import PostDamagesGameEvent
from VegansDeluxe.core import Everyone


@RegisterItem
class Hitin(Item):
    id = 'hitin'
    name = 'Хитин'


@AttachedAction(Hitin)
class HitinAction(FreeItem):
    id = 'hitin'
    name = 'Хитин'
    target_type = Everyone()
    priority = -2

    def func(self, source, target):
        target.get_state('armor').add(2, 100)
        self.session.say(f'💉|{source.name} использует хитин на {target.name}!')

        @At(self.session.id, turn=self.session.turn + 2, event=PostDamagesGameEvent)
        def hitin_knockout(context: EventContext[PostDamagesGameEvent]):
            target.get_state('armor').remove((2, 100))
            target.get_state('stun').stun += 1
            self.session.say(f'🌀|{target.name} теряет эффект хитина. Игрок оглушен!')
