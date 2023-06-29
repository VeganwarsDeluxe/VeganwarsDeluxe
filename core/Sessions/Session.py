from uuid import uuid4

from core.Entities.Entity import Entity
from core.Events.EventManager import EventManager
from core.Events.Events import PreUpdatesEvent, PostUpdatesEvent, HPLossEvent, PreActionsEvent, \
    PostActionsEvent, PreDamagesEvent, PostDamagesEvent, PostTickEvent, PostDeathsEvent, DeathEvent


class Session:
    def __init__(self):
        self.id = uuid4()
        self.turn = 1
        self.active = True

        self.entities: list[Entity] = []

        self.event_manager: EventManager = EventManager()

    def say(self, text, n=True):
        print(text, end=('\n' if n else ''))

    @property
    def alive_entities(self) -> list[Entity]:
        return list(filter(lambda e: not e.dead, self.entities))

    @property
    def alive_teams(self) -> set:
        teams = set()
        for entity in self.alive_entities:
            teams.add(entity.team)
        return teams

    def tick(self):
        for entity in self.entities:
            entity.tick_turn()

    def update_actions(self):
        self.event_manager.publish(PreUpdatesEvent(self.id, self.turn))
        for entity in self.entities:
            entity.update_actions()
        self.event_manager.publish(PostUpdatesEvent(self.id, self.turn))

    def pre_move(self):
        for entity in self.entities:
            entity.pre_move()

    def start(self):
        for entity in self.entities:
            for state in entity.skills:
                state.register(self.id)

    def cancel_damages(self, source):
        for entity in self.entities:
            entity.inbound_dmg.cancel(source)

    def lose_hp(self, entity, damage):
        hp_loss = (damage // 6) + 1

        message = HPLossEvent(self.id, self.turn, entity, damage, hp_loss)
        self.event_manager.publish(message)

        entity.hp -= message.hp_loss
        self.say(f"{entity.hearts}|{entity.name} теряет {message.hp_loss} ХП. Остается {entity.hp} ХП.")

    def calculate_damages(self):  # TODO: Revise just in case, I am worried
        for entity in self.entities:  # Cancelling round
            if entity.energy > entity.max_energy:
                self.say(f'💨|{entity.name} теряет излишек энергии.')
                entity.energy = entity.max_energy
            if entity.inbound_dmg.sum() > entity.outbound_dmg.sum():
                entity.outbound_dmg.clear()
                self.cancel_damages(entity)

        for entity in self.entities:
            if entity.inbound_dmg.sum() == 0:
                continue
            entity.inbound_dmg.cancel(entity)

            self.lose_hp(entity, entity.inbound_dmg.sum())

    def stop(self):
        self.active = False

    def death(self):
        for entity in self.alive_entities:
            if entity.hp > 0:
                continue

            self.say(f'☠️|{entity.name} теряет сознание.')
            entity.dead = True
            for alive_entity in self.entities:
                alive_entity.nearby_entities.remove(entity) if entity in alive_entity.nearby_entities else None

            self.event_manager.publish(DeathEvent(self.id, self.turn, entity))

    def finish(self):
        if not len(self.alive_teams):  # If everyone is dead
            self.stop()
            return

        if len(self.alive_teams) > 1:  # If there is more than 1 team alive (no-team is also a team)
            return
        if len(self.alive_teams) == 1 and None in self.alive_teams:  # If there is only no-team entities
            if len(list(self.alive_entities)) > 1:  # If there is more than one player
                return
        self.stop()

    def call_actions(self):  # TODO: Revise action calling
        all_actions = []
        for entity in self.alive_entities:
            for item in entity.item_queue:
                all_actions.append(item)
            for action in entity.action_queue:
                all_actions.append(action)
            all_actions.append(entity.action)
        for action in sorted(all_actions, key=lambda e: e.priority):
            action() if not action.canceled else None

    def move(self):  # 0. Pre-move stage
        self.event_manager.publish(PreActionsEvent(self.id, self.turn))  # 1. Pre-action stage
        self.call_actions()  # 2. Action stage
        self.event_manager.publish(PostActionsEvent(self.id, self.turn))  # 3. Post-action stage
        self.say(f'\nЭффекты {self.turn}:')
        self.event_manager.publish(PreDamagesEvent(self.id, self.turn))
        self.say(f'\nРезультаты хода {self.turn}:')
        self.calculate_damages()  # 4. Damages stage
        self.event_manager.publish(PostDamagesEvent(self.id, self.turn))  # 5. Post-damages stage
        self.tick()  # 6. Tick stage
        self.event_manager.publish(PostTickEvent(self.id, self.turn))  # 7. Post-tick stage
        self.death()  # 8. Death stage
        self.event_manager.publish(PostDeathsEvent(self.id, self.turn))  # 9. Post-death stage
        self.finish()  # 10. Finish stage

        self.turn += 1
