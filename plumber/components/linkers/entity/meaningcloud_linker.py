from plumber.components.linkers.base import BaseLinker
from plumber.components.format import Pair
from typing import List
import meaningcloud


class MeaningCloudEntityLinker(BaseLinker):
    # Name of the model to use. Example: "IAB_en" by default = "IPTC_en"
    model = 'IAB_en'
    license_key = '66a32925ab31d259206f53b84bc12643'

    def __init__(self, **kwargs):
        BaseLinker.__init__(self, name="Meaning Cloud entity linker", **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        topics_response = meaningcloud.TopicsResponse(
            meaningcloud.TopicsRequest(self.license_key, txt=text, lang='en', topicType='e').sendReq())
        if topics_response.isSuccessful():
            entities = topics_response.getEntities()
            links = []
            for entity in entities:
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
