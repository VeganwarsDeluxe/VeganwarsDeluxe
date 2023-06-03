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
all_weapons = [Claws, Drobovik, Obrez, Kastet, Tesak, Chain, BaseballBat, Rifle,
               Revolver, Pistol, Flamethrower, Axe, Knife, Shest, Saw]
all_items = [Stimulator]