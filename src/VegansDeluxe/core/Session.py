from uuid import uuid4

from VegansDeluxe.core.Entities.Entity import Entity
from VegansDeluxe.core.Events.EventManager import EventManager
from VegansDeluxe.core.Events.Events import HPLossGameEvent, PreActionsGameEvent, \
    PostActionsGameEvent, PreDamagesGameEvent, PostDamagesGameEvent, PostTickGameEvent, PostDeathsGameEvent, \
    DeathGameEvent, CallActionsGameEvent, PreDeathGameEvent, StartSessionEvent, SessionStopGameEvent, \
    SessionFinishGameEvent
from VegansDeluxe.core.Translator.LocalizedString import ls


class Session[T: Entity]:
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

        self.id = uuid4()
        self.turn = 1
        self.active = True
        self.entities: list[T] = []

        self.texts = []

    def attach_entity(self, entity: T):
        self.entities.append(entity)

    def get_entity(self, entity_id: str) -> T:
        """
        Get an entity by its ID.
        """
        result = [entity for entity in self.entities if entity.id == entity_id]
        return result[0] if result else None

    def say(self, text: str | ls, n: bool = True) -> None:
        """
        Adds given text to log queue.
        """
        self.texts.append(text + ("\n" if n else ''))

    @property
    def alive_entities(self) -> list[T]:
        """
        Get the list of entities which are not dead.
        """
        return [entity for entity in self.entities if not entity.dead]

    @property
    def alive_teams(self) -> set[str]:
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
        self.texts = []

    async def start(self):
        await self.event_manager.publish(StartSessionEvent(self.id))

    def cancel_damages(self, source):
        for entity in self.entities:
            entity.inbound_dmg.cancel(source)

    async def lose_hp(self, entity: T, damage: int) -> None:
        """
        Deduct HP from the entity and print a message.
        """
        hp_loss = (damage // 6) + 1

        message = HPLossGameEvent(self.id, self.turn, entity, damage, hp_loss)
        await self.event_manager.publish(message)

        entity.hp -= message.hp_loss
        self.say(ls("core.session.message.hp_loss").format(hearts=entity.hearts, name=entity.name, hp_loss=message.hp_loss,
                                                  hp=entity.hp))

    async def calculate_damages(self):
        for entity in self.entities:  # Cancelling round
            if entity.energy > entity.max_energy:
                self.say(ls("core.session.message.alive_entities").format(entity.name))
                entity.energy = entity.max_energy
            if entity.inbound_dmg.sum() > entity.outbound_dmg.sum():
                entity.outbound_dmg.clear()
                self.cancel_damages(entity)

        for entity in self.entities:
            if entity.inbound_dmg.sum() == 0:
                continue
            entity.inbound_dmg.cancel(entity)

            await self.lose_hp(entity, entity.inbound_dmg.sum())

    async def stop(self):
        event = SessionStopGameEvent(self.id, self.turn)
        await self.event_manager.publish(event)

        self.active = False

    async def death(self) -> None:
        """
        Handle the death of entities. Publishes PreDeathGameEvent and DeathGameEvent.
        """
        for entity in self.alive_entities:
            if entity.hp > 0:
                continue

            message = PreDeathGameEvent(self.id, self.turn, entity)
            await self.event_manager.publish(message)

            if entity.hp > 0 or message.canceled:
                continue

            self.say(ls("core.session.message.death").format(name=entity.name))
            entity.dead = True
            for alive_entity in self.entities:
                alive_entity.nearby_entities.remove(entity) if entity in alive_entity.nearby_entities else None

            await self.event_manager.publish(DeathGameEvent(self.id, self.turn, entity))

    async def finish(self):
        event = SessionFinishGameEvent(self.id, self.turn)
        await self.event_manager.publish(event)
        if event.canceled:
            return

        if not len(self.alive_teams):  # If everyone is dead
            await self.stop()
            return

        if len(self.alive_teams) > 1:  # If there is more than 1 team alive (no-team is also a team)
            return
        if len(self.alive_teams) == 1 and None in self.alive_teams:  # If there is only no-team entities
            if len(list(self.alive_entities)) > 1:  # If there is more than one player
                return
        await self.stop()

    async def move(self):
        await self.event_manager.publish(
            PreActionsGameEvent(self.id, self.turn))  # 1. Pre-action stage
        await self.event_manager.publish(
            CallActionsGameEvent(self.id, self.turn))  # 2. Action stage
        await self.event_manager.publish(
            PostActionsGameEvent(self.id, self.turn))  # 3. Post-action stage

        self.say(ls("core.session.message.effects").format(self.turn))
        await self.event_manager.publish(PreDamagesGameEvent(self.id, self.turn))

        self.say(ls("core.session.message.results").format(self.turn))
        await self.calculate_damages()  # 4. Damages stage
        await self.event_manager.publish(
            PostDamagesGameEvent(self.id, self.turn))  # 5. Post-damages stage
        self.tick()  # 6. Tick stage
        await self.event_manager.publish(
            PostTickGameEvent(self.id, self.turn))  # 7. Post-tick stage
        await self.death()  # 8. Death stage
        await self.event_manager.publish(
            PostDeathsGameEvent(self.id, self.turn))  # 9. Post-death stage
        await self.finish()  # 10. Finish stage

        self.turn += 1
