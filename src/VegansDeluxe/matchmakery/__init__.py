import pathlib

from VegansDeluxe.core import translator

localizations = str(pathlib.Path(__file__).parent.resolve().joinpath("localizations"))
translator.load_folder(localizations)

from .Tags import EntityTag
