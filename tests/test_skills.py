import pytest

from VegansDeluxe.core import PreMoveGameEvent
from VegansDeluxe.core.Question.QuestionEvents import QuestionGameEvent
from VegansDeluxe.rebuild import DoubleVein, Berserk, Junkie, Visor
from VegansDeluxe.rebuild.Items.Stimulator import Stimulator
from VegansDeluxe.rebuild.Skills.Visor import VisorAction
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
async def test_berserk_hp_loss_does_not_increase_max_energy_twice():
    engine, session = await get_duel_setup()
    player_a, player_b = session.entities

    await player_a.attach_state(Berserk(), engine.event_manager)
    await engine.action_manager.update_actions(session)
    await engine.event_manager.publish(PreMoveGameEvent(session.id, session.turn))

    assert player_a.max_energy == 3

    await session.lose_hp(player_a, 6)
    assert player_a.hp == 2
    assert player_a.max_energy == 5

    session.turn += 1
    await engine.event_manager.publish(PreMoveGameEvent(session.id, session.turn))
    assert player_a.max_energy == 5

    await session.lose_hp(player_a, 6)
    assert player_a.hp == 0
    assert player_a.max_energy == 7

    session.turn += 1
    await engine.event_manager.publish(PreMoveGameEvent(session.id, session.turn))
    assert player_a.max_energy == 7


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


@pytest.mark.asyncio()
async def test_visor_shows_target_skills_and_items():
    engine, session = await get_duel_setup()
    source, target = session.entities
    await source.attach_state(Visor(), engine.event_manager)
    await target.attach_state(DoubleVein(), engine.event_manager)
    target.items.append(Stimulator())
    target.items.append(Stimulator())

    questions = []

    async def capture_question(event: QuestionGameEvent):
        questions.append(event.question)

    engine.event_manager.at_event(capture_question, session.id, event=QuestionGameEvent)

    action = VisorAction(session, source, source.get_state(Visor))
    await action.func(source, target)

    assert len(questions) == 1
    message = str(questions[0].text)
    assert "Double Vein" in message
    assert "x2 Stimulator" in message
