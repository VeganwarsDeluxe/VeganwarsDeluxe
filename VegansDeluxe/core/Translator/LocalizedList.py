from VegansDeluxe.core.Translator.LocalizedString import LocalizedString


class LocalizedList:
    def __init__(self, elements, separator=", "):
        self.elements = elements
        self.separator = separator
