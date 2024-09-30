import random

import pytest

from VegansDeluxe import rebuild
from VegansDeluxe.rebuild import Pistol, Shotgun
from VegansDeluxe.rebuild.Weapons.Pistol import PistolAttack
from VegansDeluxe.rebuild.Weapons.Shotgun import ShotgunAttack
from tests.utils import get_duel_setup


@pytest.mark.asyncio()
async def test_basic_turn():
    engine, session = await get_duel_setup()
    player_a, player_b = session.entities

    for entity in session.entities:
        # Attach one random skill to all players
        await entity.attach_state(random.choice(rebuild.all_skills), engine.event_manager)

    # Set energy level so player A will always hit
    player_a.energy = 10
    player_b.energy = 0

    # Set a weapon for each player
    player_a.weapon = Shotgun(session.id, player_a.id)
    player_b.weapon = Pistol(session.id, player_b.id)

    # Update the list of actions, available for each player
    await engine.action_manager.update_actions(session)

    # Get "Attack" Action instance
    attack_a = engine.action_manager.get_action(session, player_a, ShotgunAttack.id)
    attack_b = engine.action_manager.get_action(session, player_b, PistolAttack.id)

    # Set player's attack target to each other
    attack_a.target = player_b
    attack_b.target = player_a

    # Add attack actions to the action queue
    engine.action_manager.queue_action_instance(attack_a)
    engine.action_manager.queue_action_instance(attack_b)

    assert session.turn == 1
    # Execute the move
    await session.move()

    assert player_b.hp < 4
    assert session.turn == 2
