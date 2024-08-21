Usage
=====

.. _installation:

Installation
------------

To use Deluxe engine, first install it using pip:

.. code-block:: console

   (.venv) $ pip3 install git+https://onedev.gts.org.ua/vezono/vegans-deluxe#egg=VegansDeluxe

Currently, we do not distribute our library on pypi.org. Yet.

If for some reason you need to install a version from different branch (ex. dev):

.. code-block:: console

   (.venv) $ pip3 install git+https://onedev.gts.org.ua/vezono/vegans-deluxe@dev#egg=VegansDeluxe

Basic usage
----------------

Below is an example of basic Session process. More examples can be found
in `examples folder <https://github.com/VeganwarsDeluxe/VeganwarsDeluxe/tree/master/src>`_.

.. code-block:: python3

    import random

    from VegansDeluxe import rebuild
    from VegansDeluxe.core import Session, Entity
    from VegansDeluxe.rebuild import Pistol, Shotgun
    from VegansDeluxe.core import Engine

    # Create the engine instance
    engine = Engine()

    # Create the game session and attach it to the engine
    session = Session(engine.event_manager)
    engine.attach_session(session)

    # Create two players
    player_a = Entity(session.id, "Player A", 4, 4, 5, 5)
    player_b = Entity(session.id, "Player B", 4, 4, 5, 5)

    # Attach players to the session
    session.attach_entity(player_a)
    session.attach_entity(player_b)

    for entity in session.entities:
        for state in rebuild.all_states:
            # Attach all default states to all players
            entity.attach_state(state(), engine.event_manager)

        # Attach one random skill to all players
        entity.attach_state(random.choice(rebuild.all_skills), engine.event_manager)

    # Set a weapon for each player
    player_a.weapon = Shotgun(session.id, player_a.id)
    player_b.weapon = Pistol(session.id, player_b.id)

    # Update the list of actions, available for each player
    engine.action_manager.update_actions(session)

    # Get "Attack" Action instance
    attack_a = engine.action_manager.get_action(session, player_a, 'attack')
    attack_b = engine.action_manager.get_action(session, player_b, 'attack')

    # Set player's attack target to each other
    attack_a.target = player_b
    attack_b.target = player_a

    # Add attack actions to the action queue
    engine.action_manager.queue_action_instance(attack_a)
    engine.action_manager.queue_action_instance(attack_b)

    # Execute the move
    session.move()

    # Display game logs
    for text in session.texts:
        print(text, end='')


