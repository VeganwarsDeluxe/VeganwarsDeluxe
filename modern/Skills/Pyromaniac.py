from core.Skills import Skill


class Pyromaniac(Skill):
    id = 'pyromaniac'
    name = 'Пиромант'
    description = 'За каждого горящего соперника вы получаете бонус к урону.'

    def __init__(self, source):
        super().__init__(source)
        self.flames = 0

    def register(self, session_id):
        @self.event_manager.at_event(session_id, event=PostAttackEvent)
        def func(message: PostAttackEvent):
            pass
