from typing import List
from plumber.components.clients.stanford import StanfordClient
from plumber.components.extractors.base import StanfordBasedExtractor
from plumber.components.format import Triple
import operator
import nltk


# Adapted from https://github.com/tdpetrou/RDF-Triple-API/blob/master/rdf_triple.py
class RdfSpo:

    def __init__(self, name, pos=''):
        self.name = name
        self.word = ''
        self.parent = ''
        self.grandparent = ''
        self.depth = ''
        self.predicate_list = []
        self.predicate_siblings = []
        self.pos = pos
        self.attr = []
        self.attr_trees = []


class RdfTriple:

    def __init__(self, sentence):
        self.sentence = sentence
        self.first_NP = ''
        self.first_VP = ''
        self.parse_tree = None
        self.subject = RdfSpo('subject')
        self.predicate = RdfSpo('predicate', 'VB')
        self.Object = RdfSpo('object')

    def find_np(self, t):
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            if t.label() == 'NP':
                if self.first_NP == '':
                    self.first_NP = t
            elif t.label() == 'VP':
                if self.first_VP == '':
                    self.first_VP = t
            for child in t:
                self.find_np(child)

    def find_subject(self, t, parent=None, grandparent=None):
        if self.subject.word != '':
            return
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            if t.label()[:2] == 'NN':
                if self.subject.word == '':
                    self.subject.word = t.leaves()[0]
                    self.subject.pos = t.label()
                    self.subject.parent = parent
                    self.subject.grandparent = grandparent
            else:
                for child in t:
                    self.find_subject(child, parent=t, grandparent=parent)

    def find_predicate(self, t, parent=None, grandparent=None, depth=0):
        try:
            t.label()
        except AttributeError:
            pass
        else:
            if t.label()[:2] == 'VB':
                self.predicate.predicate_list.append((t.leaves()[0], depth, parent, grandparent))

            for child in t:
                self.find_predicate(child, parent=t, grandparent=parent, depth=depth + 1)

    def find_deepest_predicate(self):
        if not self.predicate.predicate_list:
            return '', '', '', ''
        return max(self.predicate.predicate_list, key=operator.itemgetter(1))

    def extract_word_and_pos(self, t, depth=0, words=None):
        if words is None:
            words = []
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            if t.height() == 2:
                words.append((t.leaves()[0], t.label()))
            for child in t:
                self.extract_word_and_pos(child, depth + 1, words)
        return words

    def print_tree(self, t, depth=0):
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            for child in t:
                self.print_tree(child, depth + 1)

    def find_object(self):
        for t in self.predicate.parent:
            if self.Object.word == '':
                self.find_object_np_pp(t, t.label(), self.predicate.parent, self.predicate.grandparent)

    def find_object_np_pp(self, t, phrase_type, parent=None, grandparent=None):
        """
        finds the object given its a NP or PP or ADJP
        """
        if self.Object.word != '':
            return
        try:
            t.label()
        except AttributeError:
            pass
        else:
            # Now we know that t.node is defined
            if t.label()[:2] == 'NN' and phrase_type in ['NP', 'PP']:
                if self.Object.word == '':
                    self.Object.word = t.leaves()[0]
                    self.Object.pos = t.label()
                    self.Object.parent = parent
                    self.Object.grandparent = grandparent
            elif t.label()[:2] == 'JJ' and phrase_type == 'ADJP':
                if self.Object.word == '':
                    self.Object.word = t.leaves()[0]
                    self.Object.pos = t.label()
                    self.Object.parent = parent
                    self.Object.grandparent = grandparent
            else:
                for child in t:
                    self.find_object_np_pp(child, phrase_type, parent=t, grandparent=parent)

    def get_attributes(self, pos, sibling_tree, grandparent):
        rdf_type_attr = []
        if pos[:2] == 'JJ':
            for item in sibling_tree:
                if item.label()[:2] == 'RB':
                    rdf_type_attr.append((item.leaves()[0], item.label()))
        else:
            if pos[:2] == 'NN':
                for item in sibling_tree:
                    if item.label()[:2] in ['DT', 'PR', 'PO', 'JJ', 'CD']:
                        rdf_type_attr.append((item.leaves()[0], item.label()))
                    if item.label() in ['QP', 'NP']:
                        # append a tree
                        rdf_type_attr.append(item, item.label())
            elif pos[:2] == 'VB':
                for item in sibling_tree:
                    if item.label()[:2] == 'AD':
                        rdf_type_attr.append((item, item.label()))

        if grandparent:
            if pos[:2] in ['NN', 'JJ']:
                for uncle in grandparent:
                    if uncle.label() == 'PP':
                        rdf_type_attr.append((uncle, uncle.label()))
            elif pos[:2] == 'VB':
                for uncle in grandparent:
                    if uncle.label()[:2] == 'VB':
                        rdf_type_attr.append((uncle, uncle.label()))

        return self.attr_to_words(rdf_type_attr)

    @staticmethod
    def attr_to_words(attr):
        new_attr_words = []
        new_attr_trees = []
        for tup in attr:
            if not isinstance(tup[0], str):
                # if type(tup[0]) != unicode:
                if tup[0].height() == 2:
                    new_attr_words.append((tup[0].leaves()[0], tup[0].label()))
                else:
                    new_attr_trees.append(str(tup[0]))
            else:
                new_attr_words.append(tup)
        return new_attr_words, new_attr_trees

    def jsonify_rdf(self):
        return {'sentence': self.sentence,
                'parse_tree': self.parse_tree.__repr__(),
                'predicate': {'word': self.predicate.word, 'POS': self.predicate.pos,
                              'Word Attributes': self.predicate.attr, 'Tree Attributes': self.predicate.attr_trees},
                'subject': {'word': self.subject.word, 'POS': self.subject.pos,
                            'Word Attributes': self.subject.attr, 'Tree Attributes': self.subject.attr_trees},
                'object': {'word': self.Object.word, 'POS': self.Object.pos,
                           'Word Attributes': self.Object.attr, 'Tree Attributes': self.Object.attr_trees},
                'rdf': [self.subject.word, self.predicate.word, self.Object.word]
                }

    def get_triples(self, parsed_text):
        self.parse_tree = parsed_text
        self.find_np(self.parse_tree)
        self.find_subject(self.first_NP)
        self.find_predicate(self.first_VP)
        if self.subject.word == '' and self.first_NP != '':
            self.subject.word = self.first_NP.leaves()[0]
        self.predicate.word, self.predicate.depth, self.predicate.parent, self.predicate.grandparent = \
            self.find_deepest_predicate()
        self.find_object()
        self.subject.attr, self.subject.attr_trees = self.get_attributes(self.subject.pos, self.subject.parent,
                                                                         self.subject.grandparent)
        self.predicate.attr, self.predicate.attr_trees = self.get_attributes(self.predicate.pos, self.predicate.parent,
                                                                             self.predicate.grandparent)
        self.Object.attr, self.Object.attr_trees = self.get_attributes(self.Object.pos, self.Object.parent,
                                                                       self.Object.grandparent)
        return self.jsonify_rdf()


############################################################


class POSExtractor(StanfordBasedExtractor):

    def __init__(self, **kwargs):
        super().__init__(name='POS-based extractor', **kwargs)

    def get_triples(self, text) -> List[Triple]:
        sentences = nltk.sent_tokenize(text)
        triples = []
        for sentence_idx, sentence in enumerate(sentences):
            parsed_text = self.client.nltk_parse(sentence)
            text_triple = RdfTriple(text)
            result = text_triple.get_triples(parsed_text)
            subj = result['rdf'][0]
            pred = result['rdf'][1]
            obj = result['rdf'][2]
            triple = Triple()
            start_idx = sentence.find(subj) + sum([len(s) for s in sentences[:sentence_idx]]) + (
                    text[:text.find(sentence) + len(sentence)].count(' ')
                    - sum([s.count(' ') for s in sentences[:sentence_idx+1]]))
            end_idx = start_idx + len(subj)
            triple.add_subject(subj, start_idx, end_idx, text)
            ##########################
            start_idx = sentence.find(pred) + sum([len(s) for s in sentences[:sentence_idx]]) + (
                    text[:text.find(sentence) + len(sentence)].count(' ')
                    - sum([s.count(' ') for s in sentences[:sentence_idx+1]]))
            end_idx = start_idx + len(pred)
            triple.add_predicate(pred, start_idx, end_idx, text)
            ##########################
            start_idx = sentence.find(obj) + sum([len(s) for s in sentences[:sentence_idx]]) + (
                    text[:text.find(sentence) + len(sentence)].count(' ')
                    - sum([s.count(' ') for s in sentences[:sentence_idx+1]]))
            end_idx = start_idx + len(obj)
            triple.add_object(obj, start_idx, end_idx, text)
            # triples.append({
            #     'subject': result['rdf'][0],
            #     'relation': result['rdf'][1],
            #     'object': result['rdf'][2]
            # })
            triples.append(triple)
        return triples
