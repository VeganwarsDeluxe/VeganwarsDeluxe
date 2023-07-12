from uuid import uuid4

from core.Entities.Entity import Entity
from core.Events.EventManager import event_manager
from core.Events.Events import HPLossGameEvent, PreActionsGameEvent, \
    PostActionsGameEvent, PreDamagesGameEvent, PostDamagesGameEvent, PostTickGameEvent, PostDeathsGameEvent, \
    DeathGameEvent, CallActionsGameEvent, AttachStateEvent, PreDeathGameEvent


class Session:
    ALIVE_ENTITIES_MSG = '💨|{name} теряет излишек энергии.'
    HP_LOSS_MSG = "{hearts}|{name} теряет {hp_loss} ХП. Остается {hp} ХП."
    DEATH_MSG = '☠️|{name} теряет сознание.'

    def __init__(self):
        self.id = uuid4()
        self.turn = 1
        self.active = True
        self.entities: list[Entity] = []

    def get_entity(self, entity_id: str) -> Entity:
        """
        Get an entity by its ID.
        """
        result = [entity for entity in self.entities if entity.id == entity_id]
        return result[0] if result else None

    def say(self, text: str, n: bool = True) -> None:
        """
        Print a given text with optional newline at the end.
        """
        print(text, end=('\n' if n else ''))

    @property
    def alive_entities(self) -> list:
        """
        Get the list of entities which are not dead.
        """
        return [entity for entity in self.entities if not entity.dead]

    @property
    def alive_teams(self) -> set:
        """
        Get the set of teams which have alive entities.
        """
        return {entity.team for entity in self.alive_entities}

    def tick(self):
        for entity in self.entities:
            entity.tick_turn()

    def pre_move(self):
        for entity in self.entities:
            entity.pre_move()

    def start(self):
        for entity in self.entities:
            for state in entity.skills:
                event_manager.publish(AttachStateEvent(self.id, entity.id, state))

    def cancel_damages(self, source):
        for entity in self.entities:
            entity.inbound_dmg.cancel(source)

    def lose_hp(self, entity: Entity, damage: int) -> None:
        """
        Deduct HP from the entity and print a message.
        """
        hp_loss = (damage // 6) + 1

        message = HPLossGameEvent(self.id, self.turn, entity, damage, hp_loss)
        event_manager.publish(message)

        entity.hp -= message.hp_loss
        self.say(self.HP_LOSS_MSG.format(hearts=entity.hearts, name=entity.name, hp_loss=message.hp_loss, hp=entity.hp))

    def calculate_damages(self):
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

    def death(self) -> None:
        """
        Handle the death of entities.
        """
        for entity in self.alive_entities:
            if entity.hp > 0:
                continue

            event_manager.publish(PreDeathGameEvent(self.id, self.turn, entity))

            if entity.hp > 0:
                continue

            self.say(self.DEATH_MSG.format(name=entity.name))
            entity.dead = True
            for alive_entity in self.entities:
                alive_entity.nearby_entities.remove(entity) if entity in alive_entity.nearby_entities else None

            event_manager.publish(DeathGameEvent(self.id, self.turn, entity))

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

    def move(self):  # 0. Pre-move stage
        event_manager.publish(PreActionsGameEvent(self.id, self.turn))  # 1. Pre-action stage
        event_manager.publish(CallActionsGameEvent(self.id, self.turn))  # 2. Action stage
        event_manager.publish(PostActionsGameEvent(self.id, self.turn))  # 3. Post-action stage
        self.say(f'\nЭффекты {self.turn}:')
        event_manager.publish(PreDamagesGameEvent(self.id, self.turn))
        self.say(f'\nРезультаты хода {self.turn}:')
        self.calculate_damages()  # 4. Damages stage
        event_manager.publish(PostDamagesGameEvent(self.id, self.turn))  # 5. Post-damages stage
        self.tick()  # 6. Tick stage
        event_manager.publish(PostTickGameEvent(self.id, self.turn))  # 7. Post-tick stage
        self.death()  # 8. Death stage
        event_manager.publish(PostDeathsGameEvent(self.id, self.turn))  # 9. Post-death stage
        self.finish()  # 10. Finish stage

        self.turn += 1
