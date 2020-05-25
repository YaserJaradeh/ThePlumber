from auko.components import StanfordClient, OLLIEClient
from auko.components import DependencyExtractor, OpenIEExtractor, KBPExtractor, OllieExtractor, POSExtractor
from auko.components import StanfordCoreferenceResolver, SpacyNeuralCoreferenceResolver


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


if __name__ == '__main__':
    text = '''Despite improved digital access to scholarly knowledge in recent decades,
    scholarly communication remains exclusively document-based.
    In this form, scholarly knowledge is hard to process automatically.'''
    text = "Barack Obama was born in Hawaii. He was elected president in 2008. He is the first black president of the USA. The United states of america is one of the biggest countries of the world, it is also one of the richest."
    # test_extractors(text)
    # with StanfordClient() as client:
    #     resolver = StanfordCoreferenceResolver(client)
    #     chains = resolver.get_coreference_chains(text)
    #     print(chains)
    resolver = SpacyNeuralCoreferenceResolver()
    chains = resolver.get_coreference_chains(text)
    print(chains)
