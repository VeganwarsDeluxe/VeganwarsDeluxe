"""
Core module of the library. Contains all core mechanics of the engine.
"""

import pathlib

from .Actions import *
from .Actions.WeaponAction import *
from .ContentManager import ContentManager, AttachedAction, RegisterState, RegisterEvent, At, Next, Every, After, \
    RegisterItem, RegisterWeapon
from .Context import Context, StateContext, EventContext, ActionExecutionContext
from .Engine import *
from .Entities import *
from .Events import *
from .Items import *
from .Session import *
from .SessionManager import SessionManager
from .Skills import *
from .States import *
from .TargetType import *
from .Translator.Translator import translator
from .Weapons import *
from .utils import *

__version__ = "1.5.0"

localizations = str(pathlib.Path(__file__).parent.resolve().joinpath("localizations"))

translator.load_folder(localizations)
