from core.Actions.ActionManager import AttachedAction
from core.Items.Item import Item
from core.Actions.ItemAction import FreeItem
from core.Events.Events import PostDamagesGameEvent
from core.TargetType import Everyone


class Hitin(Item):
    id = 'hitin'
    name = 'Хитин'


@AttachedAction(Hitin)
class HitinAction(FreeItem):
    id = 'hitin'
    name = 'Хитин'
    target_type = Everyone()

    def func(self, source, target):
        target.get_skill('armor').add(2, 100)
        self.session.say(f'💉|{source.name} использует хитин на {target.name}!')

        @self.session.event_manager.at(self.session.id, turn=self.session.turn + 2, event=PostDamagesGameEvent)
        def hitin_knockout(message: PostDamagesGameEvent):
            target.get_skill('armor').remove((2, 100))
            target.get_skill('stun').stun += 1
            self.session.say(f'🌀|{target.name} теряет эффект хитина. Игрок оглушен!')
