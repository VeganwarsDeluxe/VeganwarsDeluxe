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
                entity.hp -= 1  # TODO: Implement Axe
                print(f"{entity.hp * '♥️'}|{entity.name} damaged by 1 HP. {entity.hp} is left.")

    def stop(self):
        self.active = False

    def trigger_skills(self, stage):
        """
        stages: post-death, pre-action, post-action, post-damages, post-tick, pre-move, attack
        """
        self.stage = stage
        for entity in self.entities:
            for skill in filter(lambda s: s.stage == stage, entity.skills):
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
        self.trigger_skills('pre-action')                                                     # 1. Pre-action stage
        self.call_actions()                                                                   # 2. Action stage
        self.trigger_skills('post-action')                                                    # 3. Post-action stage
        print(f'Results of turn {self.turn}:')
        self.calculate_damages()                                                              # 4. Damages stage
        self.trigger_skills('post-damages')                                                   # 5. Post-damages stage
        self.tick()                                                                           # 6. Tick stage
        self.trigger_skills('post-tick')                                                      # 7. Post-tick stage
        self.death()                                                                          # 8. Death stage
        self.trigger_skills('post-death')                                                     # 9. Post-death stage
        self.finish()                                                                         # 10. Finish stage
