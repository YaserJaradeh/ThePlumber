# ======= Base linkers =======
from .base import BaseRelationLinker, BaseJointLinker, BaseEntityLinker, BaseWebLinker
# ======= Entity linkers =======
from .entity import FalconEntityLinkerWikidata, FalconEntityLinkerDBpedia
from .entity import DBpediaSpotlightEntityLinker, OpenTapiocaEntityLinker
# ======= Relation linkers =======

# ======= Joint linkers =======
from .joint import FalconJointLinker, FalconJoinLinkerWikidata, FalconJoinLinkerDBpedia
from .joint import EARLJointLinker
