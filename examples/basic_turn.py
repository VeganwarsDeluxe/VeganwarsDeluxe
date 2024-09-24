import asyncio
import random

from VegansDeluxe import rebuild
from VegansDeluxe.core import Session, Entity, content_manager
from VegansDeluxe.rebuild import Pistol, Shotgun
from VegansDeluxe.core import Engine


async def run():
    # Create the engine instance
    print("-"*13)
    engine = Engine()
    print(engine.stats())

    # Create the game session and attach it to the engine
    session = Session(engine.event_manager)
    await engine.attach_session(session)

    # Create two players
    player_a = Entity(session.id, "Player A", 4, 4, 5, 5)
    player_b = Entity(session.id, "Player B", 4, 4, 5, 5)

    # Attach players to the session
    session.attach_entity(player_a)
    session.attach_entity(player_b)

    for entity in session.entities:
        for state in rebuild.all_states:
            # Attach all default states to all players
            await entity.attach_state(state(), engine.event_manager)

        # Attach one random skill to all players
        await entity.attach_state(random.choice(rebuild.all_skills), engine.event_manager)

    # Set a weapon for each player
    player_a.weapon = Shotgun(session.id, player_a.id)
    player_b.weapon = Pistol(session.id, player_b.id)

    # Update the list of actions, available for each player
    await engine.action_manager.update_actions(session)

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
    await session.move()

    # Display game logs
    for text in session.texts:
        print(text, end='')
        pass
    return engine


asyncio.run(run())
asyncio.run(run())
asyncio.run(run())

