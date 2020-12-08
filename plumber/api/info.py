from typing import Dict, List


class ComponentDescription:
    name: str
    key: str
    task: str
    kg: str = None
    url: str = None
    icon: str = None
    desc: str = None

    def __init__(self, name: str, task: str, key: str = None, kg: str = None, url: str = None, icon: str = None,
                 desc: str = None):
        self.name = name
        self.task = task
        self.key = name if key is None else key
        self.kg = kg
        self.url = url
        self.icon = icon
        self.desc = desc

    def as_dict(self) -> Dict:
        return vars(self)

    @staticmethod
    def create_te(name: str, key: str = None, kg: str = None, url: str = None, icon: str = None, desc: str = None):
        return ComponentDescription(name, "TE", key, kg, url, icon, desc)

    @staticmethod
    def create_cr(name: str, key: str = None, kg: str = None, url: str = None, icon: str = None, desc: str = None):
        return ComponentDescription(name, "CR", key, kg, url, icon, desc)

    @staticmethod
    def create_el(name: str, key: str = None, kg: str = None, url: str = None, icon: str = None, desc: str = None):
        return ComponentDescription(name, "EL", key, kg, url, icon, desc)

    @staticmethod
    def create_rl(name: str, key: str = None, kg: str = None, url: str = None, icon: str = None, desc: str = None):
        return ComponentDescription(name, "RL", key, kg, url, icon, desc)

    @staticmethod
    def create_el_rl(name: str, key: str = None, kg: str = None, url: str = None, icon: str = None, desc: str = None):
        return ComponentDescription(name, "EL/RL", key, kg, url, icon, desc)


components = [
    ComponentDescription.create_te(name="ClausIE", url="https://dl.acm.org/doi/10.1145/2488388.2488420",
                                   desc="""ClausIE is a clause-based approach to open information extraction, which extracts relations and their arguments from natural language text. ClausIE fundamentally differs from previous approaches in that it separates the detection of ``useful'' pieces of information expressed in a sentence from their representation in terms of extractions. In more detail, ClausIE exploits linguistic knowledge about the grammar of the English language to first detect clauses in an input sentence and to subsequently identify the type of each clause according to the grammatical function of its constituents. Based on this information, ClausIE is able to generate high-precision extractions; the representation of these extractions can be flexibly customized to the underlying application"""),
    ComponentDescription.create_te(name="Dependency-based Extractor", key="dependency",
                                   url="https://github.com/anutammewar/extract_triplets",
                                   desc="""The dependency extractor makes use of stanford parser to extract meaningful entity triplets from sentences based on the dependecy tree of said sentence"""),
    ComponentDescription.create_te(name="Graphene",
                                   url="http://aclweb.org/anthology/C18-1195",
                                   icon="https://github.com/Lambda-3/Graphene/raw/master/wiki/images/graphene_logo.png",
                                   desc="""Graphene is an Open Information Extraction (IE) approach that uses a two-layered transformation stage consisting of a clausal disembedding layer and a phrasal disembedding layer, together with rhetorical relation identification. In that way, graphene convert sentences that present a complex linguistic structure into simplified, syntactically sound sentences, from which then it can extract propositions that are represented in a two-layered hierarchy in the form of core relational tuples and accompanying contextual information which are semantically linked via rhetorical relations"""),
    ComponentDescription.create_te(name="KBP", url="https://nlp.stanford.edu/projects/kbp/",
                                   desc="""KBP is a stanford approach used for the task of knowledge base population."""),
    ComponentDescription.create_te(name="MinIE", url="https://www.aclweb.org/anthology/D17-1278/",
                                   icon="https://camo.githubusercontent.com/554a2bfffeb3b98831586187b637335c787e4d6422f5d454075b9a34f34f2d48/68747470733a2f2f756d612d7069312e6769746875622e696f2f6d696e69652f696d616765732f6d696e69655f6c6f676f2e706e67",
                                   desc="""MinIE is an open information extraction system that aims to provide useful, compact extractions with high precision and recall. MinIE approaches these goals by (1) representing information about polarity, modality, attribution, and quantities with semantic annotations instead of in the actual extraction, and (2) identifying and removing parts that are considered overly specific"""),
    ComponentDescription.create_te(name="OLLIE", url="https://www.aclweb.org/anthology/D12-1048/",
                                   desc="""OLLIE is a open information extraction system that addresses known issuess in state of the art systems, which are (1) they extract only relations that are mediated by verbs, and (2) they ignore context thus extraction tuples that are not asseted as factual."""),
    ComponentDescription.create_te(name="OpenIE",
                                   url="https://github.com/dair-iitd/OpenIE-standalone",
                                   icon="https://openie.allenai.org/assets/images/textrunner.jpg",
                                   desc="""OpenIE is an open information extraction that is a successor of OLLIE, OpenIE imporves extractions from noun relations, numerical senteces and conjunctive sentences."""),
    ComponentDescription.create_te(name="POS",
                                   url="https://github.com/tdpetrou/RDF-Triple-API",
                                   desc="""A simple approach for extracting RDF triple-like triples (subject, predicate, object) of any sentence based on the part-of-speech tags."""),
    ComponentDescription.create_te(name="ReVerb",
                                   url="https://www.aclweb.org/anthology/D11-1142/",
                                   icon="http://reverb.cs.washington.edu/knowitall.jpg",
                                   desc="""ReVerb is a program that automatically identifies and extracts binary relationships from English sentences. ReVerb is designed for Web-scale information extraction, where the target relations cannot be specified in advance and speed is important"""),
    ComponentDescription.create_te(name="R0-Extractor", key="r0",
                                   desc="""Inspired by the Covid-19 pandemic, a custom extractor that tries to extract R0 related figures from the published articles about the COV-19 virus"""),
    ##################################################################################
    ComponentDescription.create_cr(name="Stanford", key="stanford_coreference",
                                   url="https://www.aclweb.org/anthology/D10-1048/",
                                   desc="""a simple coreference architecture based on a sieve that applies tiers of deterministic coreference models one at a time from highest to lowest precision. Each tier builds on the previous tier’s entity cluster output. Further, Stanford Coreference resolver propagates global information by sharing attributes (e.g., gender and number) across mentions in the same cluster. This cautious sieve guarantees that stronger features are given precedence over weaker ones and that each decision is made using all of the information available at the time."""),
    ComponentDescription.create_cr(name="NeuralCoref", key="spacy_neural_coreference",
                                   url="https://www.aclweb.org/anthology/D16-1245/",
                                   desc="""NeuralCoref applies reinforcement learning to directly optimize a neural mention-ranking model for coreference evaluation metrics. NeuralCoref employes two approaches: the REINFORCE policy gradient algorithm and a rewardrescaled max-margin objective"""),
    ComponentDescription.create_cr(name="HMTL", key="hmtl",
                                   url="https://arxiv.org/abs/1811.06031",
                                   icon="https://huggingface.co/hmtl/assets/icon.svg",
                                   desc="""HMTL is not a typo of HTML rather it refers to Hierarchical Multi-Task Learning, this model is able to learn various Natural Language Processing (NLP) tasks, including the Coreference Resultion."""),
    ##################################################################################
    ComponentDescription.create_el(name="Meaning Cloud", key="MeaningCloudEntity", kg="DBpedia",
                                   url="https://www.meaningcloud.com/",
                                   icon="https://www.meaningcloud.com/wp-content/themes/textalytics/img_compressed/logo.png",
                                   desc="""MeaningCloud is a proprietary tool that is advertised as the easiest, most powerful and most affordable way to extract the meaning of all kinds of unstructured content: social conversation, articles, documents"""),
    ComponentDescription.create_el(name="OpenTapioca", key="OpenTapiocaEntity", kg="Wikidata",
                                   url="https://opentapioca.org/",
                                   desc="""One of the first openly available systems for entity linking on Wikidata, OpenTapioca annotates text with locations, organizations and people from Wikidata KG."""),
    ComponentDescription.create_el(name="DBpedia Spotlight", key="DBpediaSpotlightEntity", kg="DBpedia",
                                   url="https://www.dbpedia-spotlight.org/",
                                   icon="https://www.dbpedia-spotlight.org/images/logo2.png",
                                   desc="""It is a tool for automatically annotating mentions of DBpedia resources in text, providing a solution for linking unstructured information sources to the Linked Open Data cloud through DBpedia."""),
    ComponentDescription.create_el(name="TagMe", key="TagMeEntity", kg="DBpedia",
                                   url="https://tagme.d4science.org/tagme/",
                                   icon="https://tagme.d4science.org/tagme/img/tagme-logo.png",
                                   desc="""TAGME is a powerful tool that is able to identify on-the-fly meaningful short-phrases (called "spots") in an unstructured text and link them to a pertinent Wikipedia page in a fast and effective way. This annotation process has implications which go far beyond the enrichment of the text with explanatory links because it concerns with the contextualization and, in some way, the understanding of the text."""),
    ComponentDescription.create_el(name="Text Razor DBP", key="TextRazorDBpedia", kg="DBpedia",
                                   url="https://www.textrazor.com/",
                                   icon="https://www.textrazor.com/img/logo.png",
                                   desc="""The DBpedia entity linker variant of the proprietary tool, TextRazor extracts meaning from your text. The TextRazor API helps you extract and understand the Who, What, Why and How from your (survey verbatims, emails, research, tweets, news stories, and legal documents) with unprecedented accuracy and speed."""),
    ComponentDescription.create_el(name="Text Razor WD", key="TextRazorWikidata", kg="Wikidata",
                                   url="https://www.textrazor.com/",
                                   icon="https://www.textrazor.com/img/logo.png",
                                   desc="""The Wikidata entity linker variant of the proprietary tool, TextRazor extracts meaning from your text. The TextRazor API helps you extract and understand the Who, What, Why and How from your (survey verbatims, emails, research, tweets, news stories, and legal documents) with unprecedented accuracy and speed."""),
    ComponentDescription.create_el_rl(name="EARL", key="EARLJoint", kg="DBpedia",
                                      url="https://sda.tech/projects/earl/",
                                      desc="""EARL (Entity And Relation Linker), a system for jointly linking entities and relations in a question to a knowledge graph. EARL treats entity linking and relation linking as a single task and thus aims to reduce the error caused by the dependent steps. To realise this, EARL uses the knowledge graph to jointly disambiguate entity and relations. EARL obtains the context for entity disambiguation by observing the relations surrounding the entity. Similarly, it obtains the context for relation disambiguation by looking at the surrounding entities."""),
    ComponentDescription.create_el_rl(name="Falcon", key="FalconDBpediaJoint", kg="DBpedia",
                                      url="https://labs.tib.eu/falcon/",
                                      icon="https://labs.tib.eu/falcon/static/img/logo.jpg",
                                      desc="""FALCON is used to extract real word entities and the relations between them specifically all the facts mentioned in DBpedia Knowledge Graph. FALCON is not designed for questions or facts which don't exist or are without a meaning like (I want to eat icecream), becaue there isn't a fact in DBpedia about it !"""),
    ComponentDescription.create_el_rl(name="Falcon 2.0", key="FalconWikidataJoint", kg="Wikidata",
                                      url="https://labs.tib.eu/falcon/falcon2/",
                                      icon="https://labs.tib.eu/falcon/static/img/logo2.jpg",
                                      desc="""The second iteration of the joint entity and relation linking tool, this iteration is much faster, and works on Wikidata knowledge graph."""),
    ComponentDescription.create_el_rl(name="ORKG ANN Linker", key="ORKGSpacyANN", kg="ORKG",
                                      desc="""An Entity and Relation linking tool, that is built by the awesome team of the ORKG to link mentions to the ORKG graph"""),
]


class PipelineDescription:
    name: str
    extractors: List[str]
    linkers: List[str]
    resolvers: List[str]

    def __init__(
            self,
            name='pipeline',
            extractors: List[str] = None,
            linkers: List[str] = None,
            resolvers: List[str] = None
    ):
        self.extractors = extractors
        self.linkers = linkers
        self.resolvers = resolvers
        self.name = name

    def as_dict(self) -> Dict:
        return vars(self)


pipelines = [
    PipelineDescription(name='Wikidata Test Pipeline', extractors=['MinIE'],
                        linkers=['FalconWikidataJoint'], resolvers=['hmtl']),
    PipelineDescription(name='R0 Extraction Pipeline', extractors=['r0']),
]
