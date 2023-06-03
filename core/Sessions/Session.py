from core.Entities.Entity import Entity


class Session:
    def __init__(self):
        self.turn = 0
        self.started = False
        self.active = True
        self.stage = 'pre-start'

        self.entities: list[Entity] = []

    @property
    def alive_entities(self):
        for entity in self.entities:
            if not entity.dead:
                yield entity

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
                hp_loss = (entity.inbound_dmg // 6) + 1
                entity.cache.update({'hp_loss': hp_loss})
                self.trigger('hp-loss')
                hp_loss = entity.cache.get('hp_loss')
                entity.hp -= hp_loss
                print(f"{entity.hp * '♥️'}|{entity.name} damaged by {hp_loss} HP. {entity.hp} is left.")

    def stop(self):
        self.active = False

    def trigger(self, stage):
        """
        stages: post-death, pre-action, post-action, post-damages, pre-damages, post-tick, pre-move, attack, hp-loss
        """
        self.stage = stage
        for entity in self.entities:
            for skill in filter(lambda s: s.is_triggered(stage), entity.skills):
                skill(entity)

    def death(self):
        for entity in self.alive_entities:
            if entity.hp <= 0:
                print(f'{entity.name} погибает!')
                entity.dead = True

    def finish(self):
        if len(list(self.alive_entities)) <= 1:  # TODO: Normal stopping mechanism
            self.stop()
            return

    def call_actions(self):
        for entity in sorted(self.entities, key=lambda e: e.action.priority):
            entity.action(entity, entity.target)

    def move(self):                                                                           # 0. Pre-move stage
        self.trigger('pre-action')                                                     # 1. Pre-action stage
        self.call_actions()                                                                   # 2. Action stage
        self.trigger('post-action')                                                    # 3. Post-action stage
        print(f'Results of turn {self.turn}:')
        self.trigger('pre-damages')
        self.calculate_damages()                                                              # 4. Damages stage
        self.trigger('post-damages')                                                   # 5. Post-damages stage
        self.tick()                                                                           # 6. Tick stage
        self.trigger('post-tick')                                                      # 7. Post-tick stage
        self.death()                                                                          # 8. Death stage
        self.trigger('post-death')                                                     # 9. Post-death stage
        self.finish()                                                                         # 10. Finish stage
