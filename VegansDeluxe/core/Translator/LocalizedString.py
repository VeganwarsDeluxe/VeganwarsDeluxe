import copy
from typing import Self, Tuple, Dict

from VegansDeluxe.core.Translator.LocalizedList import LocalizedList
from VegansDeluxe.core.Translator.Translator import translator


class LocalizedString:
    def __init__(self, key: str, format_queue=None):
        if format_queue is None:
            format_queue = []

        self.key = key
        self.__format_queue: list[callable] = format_queue

    def __str__(self):
        return self.localize()

    def localize(self, code: str = ""):
        if code and code not in translator.locales:
            print(f"Warning: no [{code}] locale in translator. Defaulting to [{translator.default_locale}].")
            code = translator.default_locale
        string = translator.get_string(self.key, code)
        if string is None and code != translator.default_locale:
            print(f"Warning: string [{self.key}] not found in [{code}]. Defaulting to [{translator.default_locale}].")
            string = self.localize(translator.default_locale)
        if string is None:
            print(f"Warning: string [{self.key}] not found in default locale [{translator.default_locale}]. "
                  f"Defaulting to raw key.")
            string = self.key

        for format_func in self.__format_queue:
            string = format_func(string, code)

        return string

    def localize_args(self, args: tuple, kwargs: dict, code: str) -> tuple[list[str], dict[str, str]]:
        localized_args: list[str] = []
        localized_kwargs: dict[str, str] = {}

        for arg in args:
            arg = ensure_str(arg, code)
            localized_args.append(arg)

        for k, v in kwargs.items():
            v = ensure_str(v, code)
            localized_kwargs.update({k: v})

        return localized_args, localized_kwargs

    def format(self, *args, **kwargs) -> Self:
        def format_func(string: str, code=''):
            l_args, l_kwargs = self.localize_args(args, kwargs, code)
            return string.format(*l_args, **l_kwargs)

        self_copy = self.copy()
        self_copy.__format_queue.append(format_func)
        return self_copy

    def insert(self, line):
        def format_func(string: str, code=''):
            l_line = line
            if isinstance(line, LocalizedString):
                l_line = line.localize(code)
            return l_line.format(string)
        self_copy = self.copy()
        self_copy.__format_queue.append(format_func)
        return self_copy

    def __add__(self, other):
        return self.insert("{0}"+other)

    def copy(self) -> Self:
        return LocalizedString(self.key, self.__format_queue)


def ensure_str(data: str | LocalizedList | LocalizedString, code: str) -> str:
    if isinstance(data, LocalizedString):
        return data.localize(code)
    elif isinstance(data, LocalizedList):
        return data.separator.join([ensure_str(element, code) for element in data.elements])
    else:
        return data


ls = LocalizedString
