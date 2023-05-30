from core.Entities.Entity import Entity


class Session:
    def __init__(self):
        self.turn = 0
        self.started = False
        self.active = True

        self.entities: list[Entity] = []

    @property
    def enough_players(self):
        return len(self.entities) > 2

    def tick(self):
        for entity in self.entities:
            entity.tick_turn()
        self.turn += 1

    def calculate_damages(self):
        for entity in self.entities:
            if 0 == entity.inbound_dmg and 0 == entity.outbound_dmg:
                continue
            if entity.inbound_dmg >= entity.outbound_dmg:
                entity.hp -= 1  # TODO: Implement Axe
                print(f"{entity.hp * '♥️'}|{entity.name} damaged by 1 HP. {entity.hp} is left.")

    def stop(self):
        self.active = False

    def move(self):
        self.tick()
        for entity in self.entities:
            if entity.hp <= 0:
                self.entities.remove(entity)
                continue
        if len(self.entities) <= 1:  # TODO: Normal stopping mechanism
            self.stop()
            return
        for entity in sorted(self.entities.copy(), key=lambda e: e.action.priority):
            entity.action(entity, entity.target)
        self.calculate_damages()
