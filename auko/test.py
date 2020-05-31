from auko.components import StanfordClient, OLLIEClient
from auko.components import DependencyExtractor, OpenIEExtractor, KBPExtractor, OllieExtractor, POSExtractor
from auko.components import StanfordCoreferenceResolver, SpacyNeuralCoreferenceResolver
from auko.components import EARLJointLinker


def test_extractors(text: str):
    with StanfordClient() as client:
        extractor = DependencyExtractor(client)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        for triple in triples:
            print('|-', triple)
        ################################
        print('=' * 40)
        extractor = OpenIEExtractor(client)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        for triple in triples:
            print('|-', triple)
        ################################
        print('=' * 40)
        extractor = KBPExtractor(client)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        for triple in triples:
            print('|-', triple)
        ################################
        print('=' * 40)
        extractor = POSExtractor(client)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        for triple in triples:
           print('|-', triple)
        ################################
    with OLLIEClient() as client:
        print('=' * 40)
        extractor = OllieExtractor(client)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        for triple in triples:
            print('|-', triple)


def test_coref_resolvers(text):
    with StanfordClient() as client:
        resolver = StanfordCoreferenceResolver(client)
        chains = resolver.get_coreference_chains(text)
        print(resolver.name)
        print('^' * 30)
        print(chains)
    ################################
    print('=' * 40)
    resolver = SpacyNeuralCoreferenceResolver()
    chains = resolver.get_coreference_chains(text)
    print(resolver.name)
    print('^' * 30)
    print(chains)


if __name__ == '__main__':
    old_test = '''Despite improved digital access to scholarly knowledge in recent decades,
    scholarly communication remains exclusively document-based.
    In this form, scholarly knowledge is hard to process automatically.'''
    test = "Barack Obama was born in Hawaii. He was elected president in 2008."
    test_extractors(test)
    # test_coref_resolvers(test)
    linker = EARLJointLinker()
    x = linker.get_entities_and_relations("Who is the wife of Barack Obama ?")

