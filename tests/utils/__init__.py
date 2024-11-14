from VegansDeluxe import rebuild
from VegansDeluxe.core import Engine, Session, Entity


async def get_duel_setup():
    # Create the engine instance
    engine = Engine()

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

    return engine, session
