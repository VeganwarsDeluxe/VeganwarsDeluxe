import pytest

from VegansDeluxe.core import PreMoveGameEvent
from VegansDeluxe.rebuild import DoubleVein, Berserk, Junkie
from VegansDeluxe.rebuild.Weapons.Revolver import RevolverAttack, Revolver
from tests.utils import get_duel_setup


@pytest.mark.asyncio()
async def test_double_vein():
    engine, session = await get_duel_setup()
    player_a, player_b = session.entities

    await player_a.attach_state(DoubleVein(), engine.event_manager)

    # Update the list of actions, available for each player
    await engine.action_manager.update_actions(session)

    assert player_a.hp == 5


@pytest.mark.asyncio()
async def test_berserk():
    engine, session = await get_duel_setup()
    player_a, player_b = session.entities

    player_a.weapon = Revolver(session.id, player_a.id)

    await player_a.attach_state(Berserk(), engine.event_manager)

    await engine.action_manager.update_actions(session)

    player_a.hp = 1
    await engine.event_manager.publish(PreMoveGameEvent(session.id, session.turn))
    assert player_a.max_energy == 6

    player_a.energy = 999

    attack_a = engine.action_manager.get_action(session, player_a, RevolverAttack.id)
    attack_a.target = player_b
    engine.action_manager.queue_action_instance(attack_a)

    await session.move()


@pytest.mark.asyncio()
async def test_junkie():
    engine, session = await get_duel_setup()
    player_a, player_b = session.entities

    player_a.weapon = Revolver(session.id, player_a.id)

    await player_a.attach_state(Junkie(), engine.event_manager)

    await engine.action_manager.update_actions(session)
    await engine.event_manager.publish(PreMoveGameEvent(session.id, session.turn))

    assert player_a.items
    assert type(player_a.items[0]) in Junkie.item_pool

    await session.move()
