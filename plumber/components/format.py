from typing import List, AnyStr, Tuple, Dict


class Span:
    """
    Span class to represent the location of a token in the text
    """
    start: int = None
    end: int = None
    surface_form: AnyStr = None
    text: AnyStr = None
    mapping: AnyStr = None

    def __init__(self, start: int, end: int, surface_form: AnyStr, text: AnyStr):
        self.start = start
        self.end = end
        self.surface_form = surface_form
        self.text = text

    def __str__(self) -> AnyStr:
        return self.surface_form

    def __hash__(self) -> int:
        return self.surface_form.__hash__() ^ self.start.__hash__() ^ self.end.__hash__()

    def __eq__(self, other):
        return isinstance(other,
                          self.__class__) and self.surface_form == other.surface_form and self.start == other.start and self.end == other.end

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self) -> AnyStr:
        return self.__str__()


class Chain:
    """
    Coreference chain class representation, contains the main token with it's aliases
    """
    main: AnyStr = None
    aliases: List[Span] = None

    def __init__(self, main: AnyStr):
        self.main = main
        self.aliases = []

    def add_alias(self, mention: AnyStr, start: int, end: int, text: AnyStr):
        """
        Adds an alias to the main token of this chain
        :param mention: the alias surface form
        :param start: the start index of the alias in the text
        :param end: the end index of the alias in the text
        :param text: the original text where the alias exists
        """
        self.aliases.append(Span(start, end, mention, text))

    def __str__(self) -> AnyStr:
        return f"{self.main} a.k.a. [{', '.join([m.surface_form for m in self.aliases])}]"

    def __repr__(self) -> AnyStr:
        return self.__str__()


class Triple:
    """
    A triple representation of the shape <S, P, O>, each component is a Span object
    """
    subject: Span = None
    predicate: Span = None
    object: Span = None

    def add_subject(self, surface_form: AnyStr, start: int, end: int, text: AnyStr):
        """
        Add the subject part to the triple object
        :param surface_form: the string surface form of the subject
        :param start: the start index of the subject in the text
        :param end: the end index of the subject in the text
        :param text: the text where the triple is extracted from
        """
        self.subject = Span(start, end, surface_form, text)

    def add_predicate(self, surface_form: AnyStr, start: int, end: int, text: AnyStr):
        """
        Add the predicate part to the triple object
        :param surface_form: the string surface form of the predicate
        :param start: the start index of the predicate in the text
        :param end: the end index of the predicate in the text
        :param text: the text where the triple is extracted from
        """
        self.predicate = Span(start, end, surface_form, text)

    def add_object(self, surface_form: AnyStr, start: int, end: int, text: AnyStr):
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

    def __str__(self) -> AnyStr:
        return f"<{self.subject}, {self.predicate}, {self.object}>"

    def __repr__(self) -> AnyStr:
        return self.__str__()


class SPOTriple:
    """
    Class representing the final form of the triple after being processed by many components
    This class is used in the output only, and does not contain any information other than the surface form of the SPO
    """

    def __init__(self, subject: str, predicate: str, object: str, subject_label: str = None, predicate_label: str = None, object_label: str = None):
        self.subject = subject
        self.predicate = predicate
        self.object = object
        self.subject_label = subject_label
        self.predicate_label = predicate_label
        self.object_label = object_label

    def __str__(self) -> str:
        return f"<{self.subject}> <{self.predicate}> <{self.object}>"

    def __repr__(self) -> str:
        return self.__str__()

    def __get_ids(self) -> Tuple[str, str, str]:
        if '/' in self.subject:
            sub = self.subject[self.subject.rfind('/') + 1:]
            if sub[0] == '<':
                sub = sub[1:]
            if sub[-1] == '>':
                sub = sub[:-1]
        else:
            sub = self.subject
        ######################
        if '/' in self.predicate:
            pred = self.predicate[self.predicate.rfind('/') + 1:]
            if pred[0] == '<':
                pred = pred[1:]
            if pred[-1] == '>':
                pred = pred[:-1]
        else:
            pred = self.predicate
        ######################
        if '/' in self.object:
            obj = self.object[self.object.rfind('/') + 1:]
            pred = self.predicate[self.predicate.rfind('/') + 1:]
            if obj[0] == '<':
                obj = obj[1:]
            if obj[-1] == '>':
                obj = obj[:-1]
        else:
            obj = self.object
        ######################
        return sub, pred, obj

    def short_form(self) -> str:
        try:
            ids = self.__get_ids()
            return f"{ids[0]}, {ids[1]}, {ids[2]}"
        except Exception as ex:
            return ""

    def to_json(self) -> Dict:
        return {
            "subject": {
                "uri": self.subject,
                "label": self.subject_label
            },
            "predicate": {
                "uri": self.predicate,
                "label": self.predicate_label
            },
            "object": {
                "uri": self.object,
                "label": self.object_label
            }
        }

    @staticmethod
    def extract_labels(triple: Triple) -> Tuple[str, str, str]:
        subject_label = triple.subject.surface_form
        if not (triple.subject.start == -1 or triple.subject.end == -1):
            subject_label = triple.subject.text[triple.subject.start: triple.subject.end]
        #############################
        predicate_label = triple.predicate.surface_form
        if not (triple.predicate.start == -1 or triple.predicate.end == -1):
            predicate_label = triple.predicate.text[triple.predicate.start: triple.predicate.end]
        #############################
        object_label = triple.object.surface_form
        if not (triple.object.start == -1 or triple.object.end == -1):
            object_label = triple.object.text[triple.object.start: triple.object.end]
        return subject_label, predicate_label, object_label

    @staticmethod
    def from_triple(triple: Triple):
        # subject_label, predicate_label, object_label = SPOTriple.extract_labels(triple)
        return SPOTriple(
            triple.subject.mapping, triple.predicate.mapping, triple.object.mapping,
            triple.subject.surface_form, triple.predicate.surface_form, triple.object.surface_form
        )


class Pair:
    """
    A class representing a pair of values, used for linking, pairs the span and the mapping from a KG
    """
    span: str = None
    mapping: str = None
    link_type: str = None

    def __init__(self, mapping: str, span: str, link_type: str):
        self.span = span
        self.mapping = mapping
        if len(self.mapping) > 0 and self.mapping[0] == '<' and self.mapping[-1] == '>':
            self.mapping = self.mapping[1:-1]
        self.link_type = link_type

    @property
    def left(self) -> str:
        """
        Left side of the pair
        :return: a str
        """""
        return self.span

    def right(self) -> str:
        """
        right side of the pair
        :return: a string of the mapping
        """
        return self.mapping

    def __str__(self) -> AnyStr:
        return f"({self.left}, {self.right})"

    # def __repr__(self) -> AnyStr:
    #    return self.__str__()
