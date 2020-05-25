from typing import List


class Span:
    """
    Span class to represent the location of a token in the text
    """
    start: int = None
    end: int = None
    surface_form: str = None
    text: str = None

    def __init__(self, start: int, end: int, surface_form: str, text: str):
        self.start = start
        self.end = end
        self.surface_form = surface_form
        self.text = text

    def __str__(self) -> str:
        return self.surface_form

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return self.__str__()


class Chain:
    """
    Corefernce chain class representation, contains the main token with it's aliases
    """
    main: str = None
    aliases: List[Span] = None

    def __init__(self, main: str):
        self.main = main
        self.aliases = []

    def add_alias(self, mention: str, start: int, end: int, text: str):
        """
        Adds an alias to the main token of this chain
        :param mention: the alias surface form
        :param start: the start index of the alias in the text
        :param end: the end index of the alias in the text
        :param text: the original text where the alias exists
        """
        self.aliases.append(Span(start, end, mention, text))

    def __str__(self) -> str:
        return f"{self.main} a.k.a. [{', '.join([m.surface_form for m in self.aliases])}]"

    def __repr__(self) -> str:
        return self.__str__()
