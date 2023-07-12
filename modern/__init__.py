from modern.Items.Adrenaline import Adrenaline
from modern.Items.FlashGrenade import FlashGrenade
from modern.Items.Grenade import Grenade
from modern.Items.Hitin import Hitin
from modern.Items.Jet import Jet
from modern.Items.Molotov import Molotov
from modern.Items.RageSerum import RageSerum
from modern.Items.Shield import Shield
from modern.Items.Stimulator import Stimulator
from modern.Items.ThrowingKnife import ThrowingKnife
from modern.Skills.Alchemist import Alchemist
from modern.Skills.Berserk import Berserk
from modern.Skills.Biceps import Biceps
from modern.Skills.Cherep import Cherep
from modern.Skills.Dvuzhil import Dvuzhil
from modern.Skills.Inquisitor import Inquisitor
from modern.Skills.Junkie import Junkie
from modern.Skills.Medic import Medic
from modern.Skills.Mimic import Mimic
from modern.Skills.Ninja import Ninja
from modern.Skills.Sadist import Sadist
from modern.Skills.Scope import Scope
from modern.Skills.ShieldGen import ShieldGen
from modern.Skills.Stockpile import Stockpile
from modern.Skills.Thief import Thief
from modern.Skills.Zombie import Zombie
from modern.States.Aflame import Aflame
from modern.States.Armor import Armor
from modern.States.Bleeding import Bleeding
from modern.States.DamageThreshold import DamageThreshold
from modern.States.Dodge import Dodge
from modern.States.Injury import Injury
from modern.States.KnockDown import Knockdown
from modern.States.KnockedWeapon import KnockedWeapon
from modern.States.Stun import Stun
from modern.States.Zombie import ZombieState
from modern.Weapons.Axe import Axe
from modern.Weapons.BaseballBat import BaseballBat
from modern.Weapons.Bow import Bow
from modern.Weapons.Bulava import Bulava
from modern.Weapons.Chain import Chain
from modern.Weapons.Claws import Claws
from modern.Weapons.Fist import Fist
from modern.Weapons.Flamethrower import Flamethrower
from modern.Weapons.Kastet import Kastet
from modern.Weapons.Knife import Knife
from modern.Weapons.Molot import Molot
from modern.Weapons.Obrez import Obrez
from modern.Weapons.Pistol import Pistol
from modern.Weapons.Police import Police
from modern.Weapons.Revolver import Revolver
from modern.Weapons.Rifle import Rifle
from modern.Weapons.Saber import Saber
from modern.Weapons.Saw import Saw
from modern.Weapons.Shest import Shest
from modern.Weapons.Shotgun import Shotgun
from modern.Weapons.Sword import Sword
from modern.Weapons.Tesak import Tesak
from modern.Weapons.Torch import Torch

all_states = [Aflame, DamageThreshold, Bleeding, Knockdown, KnockedWeapon, Injury, Stun, Dodge, Armor, ZombieState]
all_skills = [Dvuzhil, Biceps, Cherep, Thief, Medic, Stockpile, ShieldGen, Alchemist, Mimic,
              Berserk, Junkie, Ninja, Sadist, Scope, Inquisitor, Zombie]
all_weapons = [Claws, Shotgun, Obrez, Fist, Kastet, Tesak, Chain, BaseballBat, Rifle, Torch,
               Revolver, Pistol, Flamethrower, Axe, Knife, Shest, Saw, Bulava, Molot,
               Police, Saber, Sword, Bow]
all_items = [Stimulator, Grenade, Molotov, FlashGrenade, ThrowingKnife, Adrenaline, Hitin, Jet, Shield, RageSerum]

game_items_pool = [Shield, Grenade, Molotov, FlashGrenade, ThrowingKnife, Adrenaline, Jet, Hitin]
