from auko.components import StanfordClient, OLLIEClient
from auko.components import DependencyExtractor, OpenIEExtractor, KBPExtractor, OllieExtractor

if __name__ == '__main__':
    text = 'Barack Obama was born in Hawaii.  He was elected president in 2008.'
    # with StanfordClient() as client:
    #     extractor = DependencyExtractor(client)
    #     print(extractor.name)
    #     print('^' * 30)
    #     triples = extractor.get_triples(text)
    #     for triple in triples:
    #         print('|-', triple)
    #     ################################
    #     print('='*40)
    #     extractor = OpenIEExtractor(client)
    #     print(extractor.name)
    #     print('^' * 30)
    #     triples = extractor.get_triples(text)
    #     for triple in triples:
    #         print('|-', triple)
    #     ################################
    #     print('=' * 40)
    #     extractor = KBPExtractor(client)
    #     print(extractor.name)
    #     print('^' * 30)
    #     triples = extractor.get_triples(text)
    #     for triple in triples:
    #         print('|-', triple)
    with OLLIEClient() as client:
        print('=' * 40)
        extractor = OllieExtractor(client)
        print(extractor.name)
        print('^' * 30)
        triples = extractor.get_triples(text)
        # for triple in triples:
        #     print('|-', triple)
