Creating NPCs
=====

.. note::

   Currently the library itself does not manage NPCs at all -
   for now this is meant to be supported in the end product. This article will cover NPC handling in
   vegans-deluxe-bot.

Basic NPC object
------------

.. code-block:: python3

    # Dummy in vegans-deluxe-bot is the base class for NPCs.
    class Slime(Dummy):
        def __init__(self, session_id: str, name=ls("slime.name")):
            super().__init__(session_id, name)

            self.weapon = SlimeWeapon(session_id, self.id)

            self.hp = 3
            self.max_hp = 3
            self.max_energy = 5

            self.team = 'slimes'

        def choose_act(self, session: Session[TelegramEntity]):
            super().choose_act(session)

            # Edit state-based attributes on the start of the game
            if session.turn == 1:
                self.get_state(DamageThreshold.id).threshold = 5

            # Approaching if able with 75% chance
            if self.nearby_entities != list(filter(lambda t: t != self, session.entities)) and percentage_chance(75):
                engine.action_manager.queue_action(session, self, SlimeApproach.id)
                return

            # Reloading when energy is 0
            if self.energy == 0:
                engine.action_manager.queue_action(session, self, SlimeReload.id)
                return

            # Randomly doing one of 2 actions
            if percentage_chance(50):
                engine.action_manager.queue_action(session, self, SlimeEvade.id)
                return
            else:
                attack = engine.action_manager.get_action(session, self, SlimeAttack.id)
                attack.target = random.choice(attack.targets)
                engine.action_manager.queue_action_instance(attack)
                return

            # Skipping turn if nothing above is triggered
            engine.action_manager.queue_action(session, self, SlimeSkip.id)


Creating custom actions
------------
You may have noticed different Action objects, like SlimeAttack and SlimeReload. For NPCs to have actions,
you need to create and attach them to the NPC.

.. code-block:: python3

    @AttachedAction(Slime)
    class SlimeReload(DecisiveAction):
        id = 'slime_reload'
        name = ls('slime.reload.name')
        target_type = OwnOnly()

        def func(self, source, target):
            self.session.say(ls("slime.reload.text").format(source.name, source.max_energy))
            source.energy = source.max_energy

Actions with cooldowns
------------
For now, best way to set up cooldowns is using variables in NPCs __init__.

.. code-block:: python3

    class Slime(Dummy):
        def __init__(self, session_id: str, name=ls("slime.name")):
            ...
            # On which turn Evade becomes available for NPCs to use
            self.evade_cooldown_turn = 0
            ...

         def choose_act(self, session: Session[TelegramEntity]):
            ...
            if session.turn >= self.evade_cooldown_turn:
                if some_other_checks:
                    engine.action_manager.queue_action(session, self, SlimeEvade.id)
                    self.evade_cooldown_turn = self.session.turn + 5
                    return
            ...

Using items
------------


Creating custom NPC weapons
------------
If you want custom attacks for your NPC, you create NPC weapons. It is done the same way as creating
usual weapons, really.

.. code-block:: python3

    class Slime(Dummy):
        def __init__(self, session_id: str, name=ls("slime.name")):
            ...
            self.weapon = SlimeWeapon(session_id, self.id)
            ...

    @RegisterWeapon
    class SlimeWeapon(MeleeWeapon):
        id = 'slime_weapon'
        name = ls('slime.weapon.name')

        cubes = 3
        damage_bonus = 0
        energy_cost = 2
        accuracy_bonus = 0


    @AttachedAction(SlimeWeapon)
    class SlimeAttack(MeleeAttack):
        id = 'slime_attack'
        name = ls("slime.attack.name")
        target_type = Enemies()

        def __init__(self, *args):
            super().__init__(*args)
            self.ATTACK_MESSAGE = ls("slime.weapon.attack")
            self.MISS_MESSAGE = ls("slime.weapon.miss")

        def func(self, source: Slime, target: Entity):
            damage = super().func(source, target)
            if not damage:
                return

            target.energy = max(0, target.energy - 1)
            if target.energy == 0:
                source.max_energy += 1
                source.energy = source.max_energy
                self.session.say(ls("slime.growth.text").format(source.name, source.max_energy))

Full NPC example
------------

.. code-block:: python3

    class Slime(Dummy):
        def __init__(self, session_id: str, name=ls("slime.name")):
            super().__init__(session_id, name)

            self.weapon = SlimeWeapon(session_id, self.id)

            self.hp = 3
            self.max_hp = 3
            self.max_energy = 5

            self.team = 'slimes'

            self.evade_cooldown_turn = 0

        def choose_act(self, session: Session[TelegramEntity]):
            super().choose_act(session)

            # Edit state-based attributes on the start of the game
            if session.turn == 1:
                self.get_state(DamageThreshold.id).threshold = 5

            # Approaching if able with 75% chance
            if self.nearby_entities != list(filter(lambda t: t != self, session.entities)) and percentage_chance(75):
                engine.action_manager.queue_action(session, self, SlimeApproach.id)
                return

            # Reloading when energy is 0
            if self.energy == 0:
                engine.action_manager.queue_action(session, self, SlimeReload.id)
                return

            # Randomly doing one of 2 actions
            if session.turn >= self.evade_cooldown_turn and percentage_chance(50):
                engine.action_manager.queue_action(session, self, SlimeEvade.id)
                self.evade_cooldown_turn = self.session.turn + 5
                return
            else:
                attack = engine.action_manager.get_action(session, self, SlimeAttack.id)
                attack.target = er.qrandom.choice(attack.targets)
                engine.action_manager.queue_action_instance(attack)
                return

            # Skipping turn if nothing above is triggered
            engine.action_manager.queue_action(session, self, SlimeSkip.id)

    @RegisterWeapon
    class SlimeWeapon(MeleeWeapon):
        id = 'slime_weapon'
        name = ls('slime.weapon.name')

        cubes = 3
        damage_bonus = 0
        energy_cost = 2
        accuracy_bonus = 0


    @AttachedAction(SlimeWeapon)
    class SlimeAttack(MeleeAttack):
        id = 'slime_attack'
        name = ls("slime.attack.name")
        target_type = Enemies()

        def __init__(self, *args):
            super().__init__(*args)
            self.ATTACK_MESSAGE = ls("slime.weapon.attack")
            self.MISS_MESSAGE = ls("slime.weapon.miss")

        def func(self, source: Slime, target: Entity):
            damage = super().func(source, target)
            if not damage:
                return

            target.energy = max(0, target.energy - 1)
            if target.energy == 0:
                source.max_energy += 1
                source.energy = source.max_energy
                self.session.say(ls("slime.growth.text").format(source.name, source.max_energy))