from typing import List
import spacy
from plumber.components import BaseExtractor, Triple
from nltk.stem.snowball import SnowballStemmer
import re
import itertools
from dateparser.search import search_dates


class R0Extractor(BaseExtractor):
    rules = [
        (r"mean incub period", "mean incubation period", 1),
        (r"(basic reproduct|r0 estim)", "R0 estimates (average)", 1),
        (r"mean serial|mean generat", "mean serial interval", 1),
        (r"mean incub period", "incubation period", r"\(\s*(\d+\.?\d*)\s*[,-]?\s*(\d+\.?\d*)\s*\)"),
        (r"(basic reproduct|r0 estim)", "95% Confidence interval", r"\((\s*|\s*\d*\s*\%\s*ci\s*[:,]\s*)(\d+\.?\d*)\s*[,-]?\s*(\d+\.?\d*)\s*\)"),
        (r"serial interv|generat interv", "serial interval", r"\((\s*|\s*\d*\s*\%\s*ci\s*[:,]\s*)(\d+\.?\d*)\s*[,-]?\s*(\d+\.?\d*)\s*\)"),

    ]

    def __init__(self, **kwargs):
        super().__init__(name='Covid-19 R0-Extractor', **kwargs)
        self.nlp = spacy.load('en')
        self.stemmer = SnowballStemmer(language='english')
        self.regex = r"\d+\.?\d*"

    def get_triples(self, text: str) -> List[Triple]:
        result = []
        # load text and stem it
        doc = self.nlp(text)
        new_text = ' '.join([self.stemmer.stem(token.text) for token in doc])
        # remove stop words
        doc = self.nlp(new_text)
        new_text = ' '.join([token.text for token in doc if not token.is_stop])
        # replace words with lemmas
        doc = self.nlp(new_text)
        # for sent in doc.sents:
        #     triple = self.check_for_dates(sent.text)
        #     if triple is not None:
        #         result.append([triple])
        new_text = ' '.join([token.lemma_ for token in doc])
        new_text = self.pre_process_text(new_text)
        # get sentences
        doc = self.nlp(new_text)
        for sent in doc.sents:
            # find sentences with a number in them
            matches = re.finditer(self.regex, sent.text, re.MULTILINE)
            # for matchNum, match in enumerate(matches, start=1):
            #    print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum,
            #                                                                        start=match.start(),
            #                                                                        end=match.end(),
            #                                                                        match=match.group()))
            if bool(next(matches, False)):
                result.append(self.check_against_rules(sent.text))
        return list(itertools.chain(*result))

    @staticmethod
    def pre_process_text(text: str) -> str:
        return text.replace('covid-19', 'covid')

    def check_against_rules(self, sent: str) -> List[Triple]:
        result = []
        for pattern, predicate, guide in self.rules:
            matches = [m for m in re.finditer(pattern, sent, re.MULTILINE | re.IGNORECASE)]
            if len(matches) > 0:
                numbers = [match for match in re.finditer(self.regex, sent, re.MULTILINE)]
                new_triple = Triple()
                new_triple.add_subject('Contribution 1', -1, -1, sent)
                new_triple.add_predicate(predicate, -1, -1, sent)
                if isinstance(guide, int):
                    number = self.get_number_after_mention(matches[0], numbers, guide)
                    if number is None:
                        continue
                    new_triple.add_object(number.group(), -1, -1, sent)
                else:
                    numbers = [match for match in re.finditer(guide, sent, re.MULTILINE)]
                    if len(numbers) == 0:
                        continue
                    number = self.get_number_after_mention(matches[0], numbers)
                    if number is None:
                        continue
                    new_triple.add_object(number.group(), -1, -1, sent)
                result.append(new_triple)
        return result

    @staticmethod
    def get_number_after_mention(match, matches, number_order=1):
        start_idx = match.end()
        suitable = list(filter(lambda m: m.start() > start_idx, matches))
        if len(suitable) == 0:
            return None
        return suitable[number_order - 1]

    @staticmethod
    def check_for_dates(sent: str) -> Triple:
        dates = search_dates(sent)
        if dates is not None and len(dates) == 2:
            new_triple = Triple()
            new_triple.add_subject('Contribution 1', -1, -1, sent)
            new_triple.add_predicate('Study date', -1, -1, sent)
            obj = f'{dates[0][1].date()} - {dates[1][1].date()}'
            new_triple.add_object(obj, -1, -1, sent)
            return new_triple


if __name__ == '__main__':
    ext = R0Extractor()
    text = "Background: As the COVID-19 epidemic is spreading, incoming data allows us to quantify values of key variables that determine the transmission and the effort required to control the epidemic. We determine the incubation period and serial interval distribution for transmission clusters in Singapore and in Tianjin. We infer the basic reproduction number and identify the extent of pre-symptomatic transmission. Methods: We collected outbreak information from Singapore and Tianjin, China, reported from Jan.19-Feb.26 and Jan.21-Feb.27, respectively. We estimated incubation periods and serial intervals in both populations. Results: The mean incubation period was 7.1 (6.13, 8.25) days for Singapore and 9 (7.92, 10.2)days for Tianjin. Both datasets had shorter incubation periods for earlier-occurring cases. The mean serial interval was 4.56 (2.69, 6.42) days for Singapore and 4.22 (3.43, 5.01) for Tianjin. We inferred that early in the outbreaks, infection was transmitted on average 2.55 and 2.89days before symptom onset (Singapore, Tianjin). The estimated basic reproduction number for Singapore was 1.97 (1.45, 2.48) secondary cases per infective; for Tianjin it was 1.87 (1.65,2.09) secondary cases per infective. Conclusions: Estimated serial intervals are shorter than incubation periods in both Singapore and Tianjin, suggesting that pre-symptomatic transmission is occurring. Shorter serial intervals lead to lower estimates of R0, which suggest that half of all secondary infections should be prevented to control spread."
    #text = "Background The 2019 novel Coronavirus (COVID-19) emerged in Wuhan, China in December 2019 and has been spreading rapidly in China. Decisions about its pandemic threat and the appropriate level of public health response depend heavily on estimates of its basic reproduction number and assessments of interventions conducted in the early stages of the epidemic. Methods We conducted a mathematical modeling study using five independent methods to assess the basic reproduction number (R0) of COVID-19, using data on confirmed cases obtained from the China National Health Commission for the period 10th January to 8th February. We analyzed the data for the period before the closure of Wuhan city (10th January to 23rd January) and the post-closure period (23rd January to 8th February) and for the whole period, to assess both the epidemic risk of the virus and the effectiveness of the closure of Wuhan city on spread of COVID-19. Findings Before the closure of Wuhan city the basic reproduction number of COVID-19 was 4.38 (95% CI: 3.63-5.13), dropping to 3.41 (95% CI: 3.16-3.65) after the closure of Wuhan city. Over the entire epidemic period COVID-19 had a basic reproduction number of 3.39 (95% CI: 3.09-3.70), indicating it has a very high transmissibility. Interpretation COVID-19 is a highly transmissible virus with a very high risk of epidemic outbreak once it emerges in metropolitan areas. The closure of Wuhan city was effective in reducing the severity of the epidemic, but even after closure of the city and the subsequent expansion of that closure to other parts of Hubei the virus remained extremely infectious. Emergency planners in other cities should consider this high infectiousness when considering responses to this virus."
    #text = "We estimated the reproduction number of 2020 Iranian COVID-19 epidemic using two different methods: R0 was estimated at 4.4 (95% CI, 3.9, 4.9) (generalized growth model) and 3.50 (1.28, 8.14) (epidemic doubling time) (February 19 - March 1) while the effective R was estimated at 1.55 (1.06, 2.57) (March 6-19)."
    x = ext.get_triples(text)
