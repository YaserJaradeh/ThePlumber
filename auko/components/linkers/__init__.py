# ======= Base linkers =======
from .base import BaseRelationLinker, BaseJointLinker, BaseEntityLinker, BaseWebLinker, DummyLinker
# ======= Entity linkers =======
from .entity import FalconWikidataEntityLinker, FalconDBpediaEntityLinker
from .entity import DBpediaSpotlightEntityLinker, OpenTapiocaEntityLinker
# ======= Relation linkers =======

# ======= Joint linkers =======
from .joint import FalconJointLinker, FalconWikidataJoinLinker, FalconDBpediaJoinLinker
from .joint import EARLJointLinker
