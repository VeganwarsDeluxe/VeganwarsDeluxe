"""
Module for Rebuild game content.
"""

import pathlib

from VegansDeluxe.core.Translator.Translator import translator
from VegansDeluxe.rebuild.Items.Adrenaline import Adrenaline
from VegansDeluxe.rebuild.Items.Chitin import Chitin
from VegansDeluxe.rebuild.Items.FlashGrenade import FlashGrenade
from VegansDeluxe.rebuild.Items.Grenade import Grenade
from VegansDeluxe.rebuild.Items.Jet import Jet
from VegansDeluxe.rebuild.Items.Molotov import Molotov
from VegansDeluxe.rebuild.Items.RageSerum import RageSerum
from VegansDeluxe.rebuild.Items.Shield import Shield
from VegansDeluxe.rebuild.Items.Stimulator import Stimulator
from VegansDeluxe.rebuild.Items.ThrowingKnife import ThrowingKnife
from VegansDeluxe.rebuild.Skills.Alchemist import Alchemist
from VegansDeluxe.rebuild.Skills.Berserk import Berserk
from VegansDeluxe.rebuild.Skills.Biceps import Biceps
from VegansDeluxe.rebuild.Skills.DoubleVein import DoubleVein
from VegansDeluxe.rebuild.Skills.GasMask import GasMask
from VegansDeluxe.rebuild.Skills.Inquisitor import Inquisitor
from VegansDeluxe.rebuild.Skills.Junkie import Junkie
from VegansDeluxe.rebuild.Skills.Medic import Medic
from VegansDeluxe.rebuild.Skills.Mimic import Mimic
from VegansDeluxe.rebuild.Skills.Necromancer import Necromancer
from VegansDeluxe.rebuild.Skills.Ninja import Ninja
from VegansDeluxe.rebuild.Skills.Pyromaniac import Pyromaniac
from VegansDeluxe.rebuild.Skills.Sadist import Sadist
from VegansDeluxe.rebuild.Skills.Scope import Scope
from VegansDeluxe.rebuild.Skills.ShieldGen import ShieldGen
from VegansDeluxe.rebuild.Skills.Stockpile import Stockpile
from VegansDeluxe.rebuild.Skills.Thief import Thief
from VegansDeluxe.rebuild.Skills.ToughSkull import ToughSkull
from VegansDeluxe.rebuild.Skills.Visor import Visor
from VegansDeluxe.rebuild.Skills.Zombie import Zombie
from VegansDeluxe.rebuild.States.Aflame import Aflame
from VegansDeluxe.rebuild.States.Armor import Armor
from VegansDeluxe.rebuild.States.Bleeding import Bleeding
from VegansDeluxe.rebuild.States.DamageThreshold import DamageThreshold
from VegansDeluxe.rebuild.States.Dodge import Dodge
from VegansDeluxe.rebuild.States.DroppedWeapon import DroppedWeapon
from VegansDeluxe.rebuild.States.Injury import Injury
from VegansDeluxe.rebuild.States.KnockDown import Knockdown
from VegansDeluxe.rebuild.States.Stun import Stun
from VegansDeluxe.rebuild.States.Zombie import ZombieState
from VegansDeluxe.rebuild.Weapons.Axe import Axe
from VegansDeluxe.rebuild.Weapons.BaseballBat import BaseballBat
from VegansDeluxe.rebuild.Weapons.Bow import Bow
from VegansDeluxe.rebuild.Weapons.Chain import Chain
from VegansDeluxe.rebuild.Weapons.Claws import Claws
from VegansDeluxe.rebuild.Weapons.Fist import Fist
from VegansDeluxe.rebuild.Weapons.Flamethrower import Flamethrower
from VegansDeluxe.rebuild.Weapons.Hatchet import Hatchet
from VegansDeluxe.rebuild.Weapons.Knife import Knife
from VegansDeluxe.rebuild.Weapons.Knuckles import Knuckles
from VegansDeluxe.rebuild.Weapons.Mace import Mace
from VegansDeluxe.rebuild.Weapons.Molot import Molot
from VegansDeluxe.rebuild.Weapons.Pistol import Pistol
from VegansDeluxe.rebuild.Weapons.Police import Police
from VegansDeluxe.rebuild.Weapons.Revolver import Revolver
from VegansDeluxe.rebuild.Weapons.Rifle import Rifle
from VegansDeluxe.rebuild.Weapons.Saber import Saber
from VegansDeluxe.rebuild.Weapons.Saw import Saw
from VegansDeluxe.rebuild.Weapons.SawedOffShotgun import SawedOffShotgun
from VegansDeluxe.rebuild.Weapons.Shaft import Shaft
from VegansDeluxe.rebuild.Weapons.Shotgun import Shotgun
from VegansDeluxe.rebuild.Weapons.Spear import Spear
from VegansDeluxe.rebuild.Weapons.Torch import Torch

all_states = [Aflame, DamageThreshold, Bleeding, Knockdown, DroppedWeapon, Injury, Stun, Dodge, Armor, ZombieState]
all_skills = [DoubleVein, Biceps, ToughSkull, Thief, Medic, Stockpile, ShieldGen, Alchemist, Mimic,
              Berserk, Junkie, Ninja, Necromancer, Sadist, Scope, Inquisitor, Visor, Zombie, Pyromaniac, GasMask]
all_weapons = [Claws, Shotgun, SawedOffShotgun, Fist, Knuckles, Hatchet, Chain, BaseballBat, Rifle, Torch,
               Revolver, Pistol, Flamethrower, Axe, Knife, Shaft, Saw, Mace, Molot,
               Police, Saber, Bow, Spear]
all_items = [Stimulator, Grenade, Molotov, FlashGrenade, ThrowingKnife, Adrenaline, Chitin, Jet, Shield, RageSerum]

game_items_pool = [Shield, Grenade, Molotov, FlashGrenade, ThrowingKnife, Adrenaline, Jet, Chitin]

localizations = str(pathlib.Path(__file__).parent.resolve().joinpath("localizations"))
translator.load_folder(localizations)
