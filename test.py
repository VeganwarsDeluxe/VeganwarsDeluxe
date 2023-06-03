from core.Entities.Dummy import Dummy
from core.Sessions.Session import Session
import random

from modern.Weapons.Claws import Claws
from modern.Weapons.Drobovik import Drobovik
from modern.Weapons.Obrez import Obrez
from modern.Weapons.Fist import Fist
from modern.Weapons.Kastet import Kastet
from modern.Weapons.Tesak import Tesak
from modern.Weapons.Revolver import Revolver
from modern.Weapons.Pistol import Pistol
from modern.Weapons.Flamethrower import Flamethrower
from modern.Weapons.Axe import Axe
from modern.Weapons.Knife import Knife
from modern.Weapons.Shest import Shest
from modern.Weapons.Chain import Chain
from modern.Weapons.Saw import Saw
from modern.Weapons.BaseballBat import BaseballBat
from modern.Weapons.Rifle import Rifle

from modern.Skills.Biceps import Biceps
from modern.Skills.Dvuzhil import Dvuzhil
from modern.Skills.Armor import Armor
from modern.Skills.Cherep import Cherep
from modern.Skills.Thief import Thief

from modern.States.Aflame import Aflame
from modern.States.DamageThreshold import DamageThreshold
from modern.States.Bleeding import Bleeding
from modern.States.KnockDown import Knockdown
from modern.States.KnockedWeapon import KnockedWeapon
from modern.States.Injury import Injury
from modern.States.Stun import Stun

from modern.Items.Stimulator import Stimulator

all_states = [Aflame, DamageThreshold, Bleeding, Knockdown, KnockedWeapon, Injury, Stun]
all_skills = [Dvuzhil, Armor, Biceps, Cherep, Thief]
all_weapons = [Claws, Drobovik, Obrez, Fist, Kastet, Tesak, Chain, BaseballBat, Rifle,
               Revolver, Pistol, Flamethrower, Axe, Knife, Shest, Saw]
all_items = [Stimulator]


def simulate():
    s = Session()

    PlayerA = Dummy(s, 'Алекс')
    PlayerB = Dummy(s, 'Скелет')

    PlayerA.weapon = Rifle(PlayerA) # random.choice(all_weapons)()
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
        s.say(f'Turn {s.turn} begins!')
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
