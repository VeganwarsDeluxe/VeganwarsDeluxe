from core.Actions.ActionManager import action_manager
from core.Actions.EntityActions import *

from modern.Weapons.Claws import Claws
from modern.Weapons.Shotgun import Shotgun
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
from modern.Weapons.Bulava import Bulava
from modern.Weapons.Molot import Molot
from modern.Weapons.Torch import Torch
from modern.Weapons.Police import Police
from modern.Weapons.Saber import Saber
from modern.Weapons.Sword import Sword
from modern.Weapons.Bow import Bow

from modern.Skills.Biceps import Biceps
from modern.Skills.Dvuzhil import Dvuzhil
from modern.Skills.Cherep import Cherep
from modern.Skills.Thief import Thief
from modern.Skills.Medic import Medic
from modern.Skills.Stockpile import Stockpile
from modern.Skills.ShieldGen import ShieldGen
from modern.Skills.Alchemist import Alchemist
from modern.Skills.Mimic import Mimic

from modern.States.Aflame import Aflame
from modern.States.DamageThreshold import DamageThreshold
from modern.States.Bleeding import Bleeding
from modern.States.KnockDown import Knockdown
from modern.States.KnockedWeapon import KnockedWeapon
from modern.States.Injury import Injury
from modern.States.Stun import Stun
from modern.States.Dodge import Dodge
from modern.States.Armor import Armor

from modern.Items.Stimulator import Stimulator
from modern.Items.Grenade import Grenade
from modern.Items.Molotov import Molotov
from modern.Items.ThrowingKnife import ThrowingKnife
from modern.Items.FlashGrenade import FlashGrenade
from modern.Items.Adrenaline import Adrenaline
from modern.Items.Hitin import Hitin
from modern.Items.Jet import Jet
from modern.Items.Shield import Shield
from modern.Items.RageSerum import RageSerum

all_states = [Aflame, DamageThreshold, Bleeding, Knockdown, KnockedWeapon, Injury, Stun, Dodge, Armor]
all_skills = [Dvuzhil, Biceps, Cherep, Thief, Medic, Stockpile, ShieldGen, Alchemist, Mimic]
all_weapons = [Claws, Shotgun, Obrez, Fist, Kastet, Tesak, Chain, BaseballBat, Rifle, Torch,
               Revolver, Pistol, Flamethrower, Axe, Knife, Shest, Saw, Bulava, Molot,
               Police, Saber, Sword, Bow]
all_items = [Stimulator, Grenade, Molotov, FlashGrenade, ThrowingKnife, Adrenaline, Hitin, Jet, Shield, RageSerum]

game_items_pool = [Shield, Grenade, Molotov, FlashGrenade, ThrowingKnife, Adrenaline, Jet, Hitin]