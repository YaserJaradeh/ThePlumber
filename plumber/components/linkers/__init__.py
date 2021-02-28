# ======= Base linkers =======
from .base import BaseLinker, BaseWebLinker, DummyLinker, BaseSpacyANNLinker
# ======= Entity linkers =======
from .entity import DBpediaSpotlightEntityLinker, OpenTapiocaEntityLinker, TagMeEntityLinker
from .entity import TextRazorEntityLinker, TextRazorDBpediaLinker, TextRazorWikidataLinker
from .entity import MeaningCloudEntityLinker
# ======= Relation linkers =======

# ======= Joint linkers =======
from .joint import FalconJointLinker, FalconWikidataJointLinker, FalconDBpediaJointLinker
from .joint import EARLJointLinker
from .joint import WikidataSpacyANNJointLinker, DBpediaSpacyANNJointLinker
from .joint import ESFalconWikidataJointLinker, ESFalconDBpediaJointLinker
from .joint import ESEarlDBpediaJointLinker, ESEarlWikidataJointLinker
from .joint import ESTagMeDBpediaJointLinker, ESTagMeWikidataJointLinker
from .joint import ORKGSpacyANNLinker
