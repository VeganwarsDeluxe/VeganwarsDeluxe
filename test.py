from core.Entities.Dummy import Dummy
from core.Sessions.Session import Session
import random
from modern import all_states, all_weapons, all_skills, all_items
from modern import Flamethrower as TestWeapon


def simulate():
    s = Session()

    PlayerA = Dummy(s, 'Алекс')
    PlayerB = Dummy(s, 'Скелет')

    PlayerA.weapon = TestWeapon(PlayerA) # random.choice(all_weapons)()
    PlayerB.weapon = random.choice(all_weapons)(PlayerB)

    PlayerA.skills += [random.choice(all_skills)()] + list(map(lambda s: s(), all_states))
    PlayerB.skills += [random.choice(all_skills)()] + list(map(lambda s: s(), all_states))

    PlayerA.items += [random.choice(all_items)()]
    PlayerB.items += [random.choice(all_items)()]

    s.entities = [PlayerA, PlayerB]

    for i in range(33):
        if not s.active:
            return
        s.pre_move(), s.trigger('pre-move')
        s.say(f'Ход {s.turn}:')
        for player in s.alive_entities:
            if player.items and random.choice([True, False]):
                item = random.choice(player.items)
                item.source = player
                item.target = player.target
                player.items.remove(item)
                player.using_items.append(item)
            while True:
                player.action = random.choice(player.actions)
                targets = player.get_targets(player.action.type)
                if not targets:
                    continue
                player.target = random.choice(targets)
                break
            player.action.source = player
            player.action.target = player.target

        s.move()
        s.say('')


simulate()
