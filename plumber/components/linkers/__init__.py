# ======= Base linkers =======
from .base import BaseLinker, BaseWebLinker, DummyLinker
# ======= Entity linkers =======
from .entity import DBpediaSpotlightEntityLinker, OpenTapiocaEntityLinker, TagMeEntityLinker
# ======= Relation linkers =======

# ======= Joint linkers =======
from .joint import FalconJointLinker, FalconWikidataJointLinker, FalconDBpediaJointLinker
from .joint import EARLJointLinker
