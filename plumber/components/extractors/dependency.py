from typing import List
from plumber.components.extractors.base import StanfordBasedExtractor
from plumber.components.format import Triple
from xml.dom.minidom import parseString
import nltk


# Adapted from https://github.com/anutammewar/extract_triplets/blob/1de00fe5f15be81bf8d8d02a32a9b00c4ec84882/extract.py
class DependencyExtractor(StanfordBasedExtractor):

    def __init__(self, **kwargs):
        super().__init__(name='Dependency-based Extractor', **kwargs)
        self.id_map = {}  # key=id, value=word
        self.tree_up = {}  # key = child id, value = parent id
        self.tree_down = {}  # kay = parent id, value = list of children ids
        self.rels = {}  # list of relation labels found in the tree
        self.tuples = []  # list of relation tiples (rel label, head, child)
        self.triplets = []  # list of meaningful triplets
        self.root = ""

    def __combine_verb_words(self, comb_type):
        # to get a verb entity consisting of multiple words like
        # auxilary verb,adverb,etc combined to form a single meaningful entity
        # Ex: Michael was running towards home very fast.
        # verb entity: "running very fast"
        # currently works only if root word is a verb and combines two or more verbs in conjunction
        head = self.root
        entity2 = [int(head)]
        stack = [head]
        while len(stack) != 0:
            args = []
            if stack[0] in self.tree_down:
                args = self.tree_down[stack[0]]
            stack = stack[1:]
            for x in args:
                if int(x) in entity2:
                    continue
                tuples1 = self.tuples[:]
                for y in tuples1:
                    if y[2] == x and (("verb" in comb_type and y[0] in ["neg", "aux", "advmod", "cc", "conj",
                                                                        "compound", "case", "cop"]) or (
                                              "dobj" in comb_type and y[0] in ["neg", "aux", "advmod", "cc", "conj",
                                                                               "compound", "dobj", "det", "amod",
                                                                               "case", "cop"])):
                        self.tree_down[head] += [x]
                        self.tree_up[x] = head
                        new_tup = (y[0], head, x)
                        self.tuples.append(new_tup)
                        self.tuples.remove(y)
                        entity2.append(int(x))
                        stack.append(x)
        entity2 = sorted(list(set(entity2)))
        string2 = ""
        for x in entity2:
            string2 += self.id_map[str(x)] + " "
        entity2 = string2
        return entity2

    def __combine_subj_words(self):
        # to get a noun subject entity consisting of multiple words like
        # determiner,adjective, etc combined to form a single meaningful entity
        # Ex: The red box contained three balls.
        # subject entity: "The red box"
        # also combines two are more subjects in conjuction
        entity1 = []
        head = "-1"
        for tup in self.tuples:
            if "nsubj" in tup[0] and tup[1] == self.root:
                head = tup[2]
                break
        if head == "-1":
            return -1
        entity1 = [int(head)]
        stack = [head]
        while len(stack) != 0:
            args = []
            if stack[0] in self.tree_down:
                args = self.tree_down[stack[0]]
            stack = stack[1:]
            for x in args:
                if int(x) in entity1:
                    continue
                tuples1 = self.tuples[:]
                for y in tuples1:
                    if y[2] == x and y[0] in ["neg", "advmod", "cc", "conj", "det", "amod", "compound", "nmod", "case"]:
                        self.tree_down[head] += [x]
                        self.tree_up[x] = head
                        new_tup = (y[0], head, x)
                        self.tuples.append(new_tup)
                        self.tuples.remove(y)
                        entity1.append(int(x))
                        stack.append(x)

        entity1 = sorted(list(set(entity1)))
        string1 = ""
        for x in entity1:
            string1 += self.id_map[str(x)] + " "
        entity1 = string1
        return entity1

    def __get_object(self, head):
        entity3 = [int(head)]
        stack = [head]
        while len(stack) != 0:
            args = []
            if stack[0] in self.tree_down:
                args = self.tree_down[stack[0]]
            stack = stack[1:]
            for x in args:
                if int(x) in entity3:
                    continue
                tuples1 = self.tuples[:]

                for y in tuples1:
                    if y[2] == x and y[0] in ["neg", "advmod", "cc", "conj", "compound", "det", "amod", "case", "nmod"]:
                        self.tree_down[head] += [x]
                        self.tree_up[x] = head
                        new_tup = (y[0], head, x)
                        self.tuples.append(new_tup)
                        self.tuples.remove(y)
                        entity3.append(int(x))
                        stack.append(x)

        entity3 = sorted(list(set(entity3)))
        string3 = ""
        for x in entity3:
            string3 += self.id_map[str(x)] + " "
        entity3 = string3
        return entity3

    def __form_triplets(self, entity1: str, entity2: str, sentence: str, previous_length: int, text: str):
        head = "-1"
        for tup in self.tuples:
            if "dobj" in tup[0] and tup[1] == self.root:
                head = tup[2]
                break
        triple = Triple()
        start_idx = sentence.find(entity1) + previous_length
        end_idx = start_idx + len(entity1)
        triple.add_subject(entity1, start_idx, end_idx, text)
        ###########################
        start_idx = sentence.find(entity2) + previous_length
        end_idx = start_idx + len(entity2)
        triple.add_predicate(entity2, start_idx, end_idx, text)
        if head != "-1":  # direct object present
            entity3 = self.__get_object(head).strip()  # get direct object entity
            start_idx = sentence.find(entity3) + previous_length
            end_idx = start_idx + len(entity3)
            triple.add_object(entity3, start_idx, end_idx, text)
            self.triplets.append(triple)  # (entity1,entity2,direct-object)
            # if there is no other argument (other than direct-object) then go to next sentence
            if "nmod" not in self.rels:
                if all(["nmod" not in k for k in self.rels.keys()]):
                    return -1
            else:
                entity2 = self.__combine_verb_words("dobj")  # modified entity2

        head = "-1"
        tuples1 = self.tuples[:]
        for rel in tuples1:
            if "nmod" in rel[0] and rel[1] == self.root:
                head = rel[2]
                entity3 = self.__get_object(head).strip()
                start_idx = sentence.find(entity3) + previous_length
                end_idx = start_idx + len(entity3)
                triple.add_object(entity3, start_idx, end_idx, text)
                self.triplets.append(triple)
        if head == "-1":
            return -1
        return 1

    def __extract_triplets(self, sentences, text):
        text_sentences = nltk.sent_tokenize(text)
        for idx, sentence in enumerate(sentences):
            self.id_map = {}
            self.tree_up = {}
            self.tree_down = {}
            self.rels = {}
            basic_dep = sentence.getElementsByTagName('dependencies')
            if len(basic_dep) == 0:
                continue
            basic_dep = basic_dep[0]
            self.tuples = []
            # -------------------extract relations ----------------------
            for link in basic_dep.getElementsByTagName('dep'):
                rel = link.attributes['type'].value
                head = link.getElementsByTagName('governor')[0].attributes['idx'].value
                self.id_map[head] = link.getElementsByTagName('governor')[0].childNodes[0].nodeValue
                child = link.getElementsByTagName('dependent')[0].attributes['idx'].value
                self.id_map[child] = link.getElementsByTagName('dependent')[0].childNodes[0].nodeValue
                self.tree_up[child] = head
                if head not in self.tree_down:
                    self.tree_down[head] = []
                self.tree_down[head].append(child)
                self.tuples.append((rel, head, child))
                self.rels[rel] = 1
            if "nsubj" not in self.rels:  # if there is no subject, go to next sentence
                if all(["nsubj" not in k for k in self.rels.keys()]):
                    continue
            self.root = self.tuples[0][2]
            # MEANINGFUL TRIPLET = (subj, verb, object) = (entity1, entity2, entity3)
            entity2 = self.__combine_verb_words("verb")
            entity1 = self.__combine_subj_words()
            if entity1 == -1:  # if the root word has no subject associated, skip the sentence
                continue
            if self.__form_triplets(
                    entity1.strip(),
                    entity2.strip(),
                    text_sentences[idx],
                    sum([len(s) for s in text_sentences[:idx]]) + text[:text.find(text_sentences[idx]) + len(
                        text_sentences[idx])].count(' ') - sum([s.count(' ') for s in text_sentences[:idx + 1]])
                    , text) == -1:
                continue

    def get_triples(self, text) -> List[Triple]:
        output = self.client.parse(text, output_format='xml')
        xmldoc = parseString(output)  # parse the xml output
        sentences = xmldoc.getElementsByTagName('sentence')
        self.__extract_triplets(sentences, text)
        return self.triplets
