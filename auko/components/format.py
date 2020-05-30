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
    Coreference chain class representation, contains the main token with it's aliases
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


class Triple:
    """
    A triple representation of the shape <S, P, O>, each component is a Span object
    """
    subject: Span = None
    predicate: Span = None
    object: Span = None

    def add_subject(self, surface_form: str, start: int, end: int, text: str):
        """
        Add the subject part to the triple object
        :param surface_form: the string surface form of the subject
        :param start: the start index of the subject in the text
        :param end: the end index of the subject in the text
        :param text: the text where the triple is extracted from
        """
        self.subject = Span(start, end, surface_form, text)

    def add_predicate(self, surface_form: str, start: int, end: int, text: str):
        """
        Add the predicate part to the triple object
        :param surface_form: the string surface form of the predicate
        :param start: the start index of the predicate in the text
        :param end: the end index of the predicate in the text
        :param text: the text where the triple is extracted from
        """
        self.predicate = Span(start, end, surface_form, text)

    def add_object(self, surface_form: str, start: int, end: int, text: str):
        """
        Add the object part to the triple object
        :param surface_form: the string surface form of the object
        :param start: the start index of the object in the text
        :param end: the end index of the object in the text
        :param text: the text where the triple is extracted from
        """
        self.object = Span(start, end, surface_form, text)

    @property
    def as_text(self):
        return f"{self.subject} {self.predicate} {self.object}"

    def __str__(self) -> str:
        return f"<{self.subject}, {self.predicate}, {self.object}>"

    def __repr__(self) -> str:
        return self.__str__()


class Pair:
    """
    A class representing a pair of values, used for linking, pairs the span and the mapping from a KG
    """
    span: Span = None
    mapping: str = None

    def __init__(self, span: Span, mapping: str):
        self.span = span
        self.mapping = mapping

    @property
    def left(self) -> Span:
        """
        Left side of the pair
        :return: a Span
        """""
        return self.span

    def right(self) -> str:
        """
        right side of the pair
        :return: a string of the mapping
        """
        return self.mapping

    def __str__(self) -> str:
        return f"({self.left}, {self.right})"

    def __repr__(self) -> str:
        return self.__str__()
