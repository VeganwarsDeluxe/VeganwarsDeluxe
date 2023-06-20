from core.Entities.Entity import Entity


class Session:
    def __init__(self):
        self.turn = 1
        self.started = False
        self.active = True
        self.current_stage = 'pre-start'

        self.entities: list[Entity] = []

    def say(self, text, n=True):
        print(text, end=('\n' if n else ''))

    @property
    def alive_entities(self):
        for entity in self.entities:
            if not entity.dead:
                yield entity

    @property
    def alive_teams(self):
        teams = []
        for entity in self.alive_entities:
            if entity.team not in teams:
                teams.append(entity.team)
        return teams

    def tick(self):
        for entity in self.entities:
            entity.tick_turn()
        self.turn += 1

    def update_actions(self):
        self.stage('pre-update')
        for entity in self.entities:
            entity.update_actions()
        self.stage('post-update')

    def pre_move(self):
        for entity in self.entities:
            entity.pre_move()

    def cancel_damages(self, source):
        for entity in self.entities:
            entity.inbound_dmg.cancel(source)

    def calculate_damages_new(self):
        for entity in self.entities:
            in_damage = 0
            for incoming in entity.inbound_dmg.damages:
                source, damage = incoming
                if source.outbound_dmg.sum() >= source.inbound_dmg.sum():
                    in_damage += damage
            self.lose_hp(entity, in_damage)

    def lose_hp(self, entity, damage):
        hp_loss = (damage // 6) + 1
        entity.cache.update({'hp_loss': hp_loss, 'hp_loss_damage': damage})

        self.stage('hp-loss')

        hp_loss = entity.cache.get('hp_loss')
        entity.hp -= hp_loss
        self.say(f"{entity.hearts}|{entity.name} теряет {hp_loss} ХП. Остается {entity.hp} ХП.")

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

    def stage(self, stage):
        """
        stages: post-death, pre-action, post-action, post-damages, pre-damages, post-tick, pre-move, attack, hp-loss
        """
        self.current_stage = stage
        for entity in self.entities:
            for skill in filter(lambda s: s.is_triggered(stage), entity.skills):
                skill()

    def death(self):
        for entity in self.alive_entities:
            if entity.hp <= 0:
                self.say(f'☠️|{entity.name} теряет сознание.')
                entity.dead = True
                for alive_entity in self.entities:
                    alive_entity.nearby_entities.remove(entity) if entity in alive_entity.nearby_entities else None

    def finish(self):
        if not len(self.alive_teams):  # If everyone is dead
            self.stop()
            return

        if len(self.alive_teams) > 1:  # If there is more than 1 team alive (no-team is also a team)
            return
        if self.alive_teams[0] is None:  # If there is only no-team entities
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
        self.stage('pre-action')  # 1. Pre-action stage
        self.call_actions()  # 2. Action stage
        self.stage('post-action')  # 3. Post-action stage
        self.say(f'\nЭффекты {self.turn}:')
        self.stage('pre-damages')
        self.say(f'\nРезультаты хода {self.turn}:')
        self.calculate_damages()  # 4. Damages stage
        self.stage('post-damages')  # 5. Post-damages stage
        self.tick()  # 6. Tick stage
        self.stage('post-tick')  # 7. Post-tick stage
        self.death()  # 8. Death stage
        self.stage('post-death')  # 9. Post-death stage
        self.finish()  # 10. Finish stage
