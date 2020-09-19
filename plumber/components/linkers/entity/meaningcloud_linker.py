from plumber.components.linkers.base import BaseLinker
from plumber.components.format import Pair
from typing import List
import meaningcloud
from random import randint


MEANING_CLOUD_KEYS = ['dba7075ffe53d945f44e92fd13dd420e',
                      '66a32925ab31d259206f53b84bc12643',
                      '5386417778500e3fd2e4e3f7b0db2835',
                      '4e1a435d7c08f2b9106a6173bbb40497']


class MeaningCloudEntityLinker(BaseLinker):
    # Name of the model to use. Example: "IAB_en" by default = "IPTC_en"
    model = 'IAB_en'

    def __init__(self, **kwargs):
        BaseLinker.__init__(self, name="Meaning Cloud entity linker", **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        topics_response = meaningcloud.TopicsResponse(
            meaningcloud.TopicsRequest(
                MEANING_CLOUD_KEYS[randint(0, len(MEANING_CLOUD_KEYS) - 1)],
                txt=text,
                lang='en',
                topicType='e').sendReq())
        if topics_response.isSuccessful():
            entities = topics_response.getEntities()
            links = []
            for entity in entities:
                if 'semld_list' not in entity:
                    continue
                found = list(filter(lambda x: x[:23] == 'http://en.wikipedia.org', entity['semld_list']))
                if len(found) > 0:
                    links.append(
                        Pair(f"http://dbpedia.org/resource/{found[0][found[0].rfind('/') + 1:]}",
                             entity['form'], 'entity')
                    )
            return links
        else:
            if topics_response.getResponse() is None:
                print("\nOh no! The request sent did not return a Json\n")
            else:
                print("\nOh no! There was the following error: " + topics_response.getStatusMsg() + "\n")
            return []


if __name__ == '__main__':
    linker = MeaningCloudEntityLinker()
    x = linker.get_links("London is a very nice city but I also love Madrid.")
