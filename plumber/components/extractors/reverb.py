from typing import List
from plumber.components.extractors.base import BaseExtractor
from plumber.components.format import Triple
import os
from tempfile import NamedTemporaryFile
from pathlib import Path
from subprocess import Popen, PIPE
import gdown


class ReVerbExtractor(BaseExtractor):

    def __init__(self, **kwargs):
        super().__init__(name='ReVerb extractor', **kwargs)
        self.remote_url = 'https://drive.google.com/uc?id=1JuEZn7-ZWgR0WVtO2tpf8_I-RjMgvkiF'
        self.install_dir = Path('~/.reverb_resources/').expanduser()
        self.install_dir.mkdir(exist_ok=True)
        if not self.check_for_reverb_binaries():
            print('Downloading from %s.' % self.remote_url)
            gdown.download(self.remote_url,
                           str(self.install_dir / Path('reverb-core-1.4.3-SNAPSHOT-jar-with-dependencies.jar')),
                           quiet=False)
        os.environ['REVERB_HOME'] = str(self.install_dir)

    def check_for_reverb_binaries(self) -> bool:
        return (self.install_dir / Path('reverb-core-1.4.3-SNAPSHOT-jar-with-dependencies.jar')).exists()

    def run_reverb_jar(self, input_text) -> List:
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(input_text)
            f.seek(0)
            to_extract = f.name

            # Save current working directory and change it to REVERB home
            wd = os.getcwd()
            os.chdir(os.environ['REVERB_HOME'])

            sp = Popen(['java',
                        '-Xmx2g',
                        '-jar',
                        str(self.install_dir / 'reverb-core-1.4.3-SNAPSHOT-jar-with-dependencies.jar'),
                        to_extract],
                       stdout=PIPE)
            out = sp.stdout.read()

        # delete temp file
        os.unlink(f.name)

        # return working directory to old one
        os.chdir(wd)

        reverb_output = out.decode('utf-8')
        triples = []
        for row in reverb_output.split('\n'):
            columns = row.split('\t')
            if len(columns) < 18:
                # ignore empty or invalid lines
                continue
            triples.append((columns[2], columns[3], columns[4]))
        return triples

    def get_triples(self, text) -> List[Triple]:
        if not self.check_for_reverb_binaries():
            raise RuntimeError("ReVerb binaries seems to be missing!")
        extracted_triples = self.run_reverb_jar(text)
        triples = []
        for triple in extracted_triples:
            trp = Triple()
            # ========== Subject ==============
            start_index = text.index(triple[0])
            end_index = start_index + len(triple[0])
            trp.add_subject(triple[0], start_index, end_index, text)
            # ========== Predicate ==============
            start_index = text.index(triple[1])
            end_index = start_index + len(triple[1])
            trp.add_predicate(triple[1], start_index, end_index, text)
            # ========== Object ==============
            start_index = text.index(triple[2])
            end_index = start_index + len(triple[2])
            trp.add_object(triple[2], start_index, end_index, text)
            # ========== Add triple to final output
            triples.append(trp)
        return triples


if __name__ == "__main__":
    sentence = 'Bananas are an excellent source of potassium.'
    extractor = ReVerbExtractor()
    x = extractor.get_triples(sentence)
