# ======= Base linkers =======
from .base import BaseLinker, BaseWebLinker, DummyLinker
# ======= Entity linkers =======
from .entity import FalconWikidataEntityLinker, FalconDBpediaEntityLinker
from .entity import DBpediaSpotlightEntityLinker, OpenTapiocaEntityLinker
# ======= Relation linkers =======

# ======= Joint linkers =======
from .joint import FalconJointLinker, FalconWikidataJointLinker, FalconDBpediaJointLinker
from .joint import EARLJointLinker
