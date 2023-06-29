from core.Skills.Skill import Skill


class Cherep(Skill):
    id = 'cherep'
    name = 'Крепкий череп'
    description = 'Ваш порог урона увеличивается (вам сложнее отнять больше, чем одну единицу здоровья), ' \
                  'даёт шанс заблокировать 1 урона.'

    def register(self, session_id):
        @self.source.session.event_manager.every(events='attack')
        def func(message):
            threshold = self.source.get_skill('damage-threshold')
            threshold.threshold += 1

            armor = self.source.get_skill('armor')
            armor.add(1, 50)
