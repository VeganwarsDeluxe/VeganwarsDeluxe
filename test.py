from core.Entities.Dummy import Dummy
from core.Sessions.Session import Session
import random

from core.Weapons.Claws import Claws
from core.Weapons.Drobovik import Drobovik
from core.Weapons.Obrez import Obrez
from core.Weapons.Fist import Fist
from core.Weapons.Kastet import Kastet
from core.Weapons.Tesak import Tesak
from core.Weapons.Revolver import Revolver
from core.Weapons.Pistol import Pistol
from core.Weapons.Flamethrower import Flamethrower
from core.Weapons.Axe import Axe
from core.Weapons.Knife import Knife
from core.Weapons.Shest import Shest
from core.Weapons.Chain import Chain
from core.Weapons.Saw import Saw
from core.Weapons.BaseballBat import BaseballBat
from core.Weapons.Rifle import Rifle

from core.Skills.Biceps import Biceps
from core.Skills.Dvuzhil import Dvuzhil
from core.Skills.Armor import Armor
from core.Skills.Cherep import Cherep
from core.Skills.Thief import Thief

from core.States.Aflame import Aflame
from core.States.DamageThreshold import DamageThreshold
from core.States.Bleeding import Bleeding
from core.States.KnockDown import Knockdown
from core.States.KnockedWeapon import KnockedWeapon
from core.States.Injury import Injury
from core.States.Stun import Stun

from core.Items.Stimulator import Stimulator

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
        print(f'Turn {s.turn} begins!')
        for player in s.alive_entities:
            player.say(f'Я могу: {[a.id for a in player.actions]} и {[i.id for i in player.items]}')
            if player.items and random.choice([True, False]):
                item = random.choice(player.items)
                item.source = player
                item.target = player.target
                player.items.remove(item)
                player.using_items.append(item)
            while True:
                player.action = random.choice(player.actions)
                player.target = player
                if player.action.type == 'enemy':
                    if not player.targets:
                        continue
                    player.target = random.choice(player.targets)
                break
            player.action.source = player
            player.action.target = player.target
        s.move()
        print()


simulate()
