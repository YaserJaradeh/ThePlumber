from typing import List
from plumber.components.extractors.base import BaseExtractor
from plumber.components.format import Triple
import os
import inspect


class MinIEExtractor(BaseExtractor):

    def __init__(self, **kwargs):
        super().__init__(name='MinIE extractor', **kwargs)

    def get_triples(self, text) -> List[Triple]:
        # Generate the extractions (With SAFE mode (mode = 2))
        # NOTE: sentence must be wrapped into String, else it won't work.
        minie = MinIE(String(sentence), parser, 2)
        triples = []
        for ap in minie.getPropositions().elements():
            # Some elements might by null so we don't process them.
            if ap is not None:
                triple = Triple()
                # ========== Subject ==============
                if ap.subject.toString() not in text:
                    start_index = -1
                    end_index = -1
                else:
                    start_index = text.index(ap.subject.toString())
                    end_index = start_index + len(ap.subject.toString())
                triple.add_subject(ap.subject.toString(), start_index, end_index, text)
                # ========== Predicate ==============
                if ap.relation.toString() not in text:
                    start_index = -1
                    end_index = -1
                else:
                    start_index = text.index(ap.relation.toString())
                    end_index = start_index + len(ap.relation.toString())
                triple.add_predicate(ap.relation.toString(), start_index, end_index, text)
                # ========== Object ==============
                if ap.object.toString() not in text:
                    start_index = -1
                    end_index = -1
                else:
                    start_index = text.index(ap.object.toString())
                    end_index = start_index + len(ap.object.toString())
                triple.add_object(ap.object.toString(), start_index, end_index, text)
                # ========== Add triple to final output
                triples.append(triple)
        return triples


# Change CLASSPATH to point to the minie jar archive
os.environ['CLASSPATH'] = f"{os.path.dirname(inspect.getfile(MinIEExtractor))}/resources/minie-0.0.1-SNAPSHOT.jar"

# Set JAVA_HOME for this session
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'

from jnius import autoclass

CoreNLPUtils = autoclass('de.uni_mannheim.utils.coreNLP.CoreNLPUtils')
AnnotatedProposition = autoclass('de.uni_mannheim.minie.annotation.AnnotatedProposition')
MinIE = autoclass('de.uni_mannheim.minie.MinIE')
StanfordCoreNLP = autoclass('edu.stanford.nlp.pipeline.StanfordCoreNLP')
String = autoclass('java.lang.String')

# Dependency parsing pipeline initialization
parser = CoreNLPUtils.StanfordDepNNParser()


if __name__ == "__main__":
    sentence = 'The Joker believes that the hero Batman was not actually born in foggy Gotham City.'
    extractor = MinIEExtractor()
    x = extractor.get_triples(sentence)
