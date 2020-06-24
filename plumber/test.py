from plumber.components import StanfordClient, OLLIEClient
from plumber.components import DependencyExtractor, OpenIEExtractor, KBPExtractor, OllieExtractor, POSExtractor
from plumber.components import StanfordCoreferenceResolver, SpacyNeuralCoreferenceResolver
from plumber.components import EARLJointLinker, FalconWikidataJointLinker


def test_extractors(text: str):
    with StanfordClient() as client:
        kwargs = {'stanford_client': client}
        extractor = DependencyExtractor(**kwargs)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        for triple in triples:
            print('|-', triple)
        ################################
        print('=' * 40)
        extractor = OpenIEExtractor(**kwargs)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        for triple in triples:
            print('|-', triple)
        ################################
        print('=' * 40)
        extractor = KBPExtractor(**kwargs)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        for triple in triples:
            print('|-', triple)
        ################################
        print('=' * 40)
        extractor = POSExtractor(**kwargs)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        for triple in triples:
           print('|-', triple)
        ################################
    with OLLIEClient() as client:
        kwargs = {'ollie_client': client}
        print('=' * 40)
        extractor = OllieExtractor(**kwargs)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        for triple in triples:
            print('|-', triple)


def test_coref_resolvers(text):
    with StanfordClient() as client:
        kwargs = {'stanford_client': client}
        resolver = StanfordCoreferenceResolver(**kwargs)
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
    #test_extractors(test)
    # test_coref_resolvers(test)
    linker = FalconWikidataJointLinker()
    x = linker.get_links("Who is the wife of Barack Obama ?")

