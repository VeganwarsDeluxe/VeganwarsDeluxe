"""
Core module of the library. Contains all core mechanics of the engine.
"""

import pathlib

from .Actions import *
from .Actions.WeaponAction import *
from .Entities import *
from .Events import *
from .Items import *
from .Sessions import *
from .Skills import *
from .States import *
from .Translator.Translator import translator
from .Weapons import *
from .Context import Context, StateContext, EventContext, ActionExecutionContext
from .SessionManager import SessionManager
from .ContentManager import ContentManager, AttachedAction, RegisterState, RegisterEvent, At, Next, Every, After, \
    RegisterItem, RegisterWeapon
from .TargetType import *
from .Engine import *
from .utils import *
__version__ = "1.4.5"

localizations = str(pathlib.Path(__file__).parent.resolve().joinpath("localizations"))

translator.load_folder(localizations)
