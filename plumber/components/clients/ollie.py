import os
from tempfile import NamedTemporaryFile
from pathlib import Path
from subprocess import Popen, PIPE
from wget import download
import pandas
from io import StringIO
from json import loads


class OLLIEClient:

    def __init__(self):
        self.remote_url = 'http://knowitall.cs.washington.edu/ollie/ollie-app-latest.jar'
        self.install_dir = Path('~/.ollie_resources/').expanduser()
        self.install_dir.mkdir(exist_ok=True)
        if not (self.install_dir / Path('ollie-app-latest.jar')).exists():
            print('Downloading from %s.' % self.remote_url)
            download(self.remote_url, out=str(self.install_dir))
            self.parser_remote_url = 'http://www.maltparser.org/mco/english_parser/engmalt.linear-1.7.mco'
            print('Downloading from %s.' % self.parser_remote_url)
            download(self.parser_remote_url, out=str(self.install_dir))
        os.environ['OLLIE_HOME'] = str(self.install_dir)

    def get_extraction(self, input_text):
        """
        Will take an input and use ollie to perform verb extraction.
        Returns a json containing all the extraction information.
        input_text - The file name, or text to perform extraction on.
        """

        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(input_text)
            f.seek(0)
            to_extract = f.name

            # Save current working directory and change it to OLLIE home
            wd = os.getcwd()
            os.chdir(os.environ['OLLIE_HOME'])

            sp = Popen(['java',
                        '-Xmx2g',
                        '-jar',
                        str(self.install_dir / 'ollie-app-latest.jar'),
                        '--parallel',
                        '--output-format',
                        'tabbed',
                        to_extract],
                       stdout=PIPE)
            out = sp.stdout.read()

        # delete temp file
        os.unlink(f.name)

        # return working directory to old one
        os.chdir(wd)

        data_frame = pandas.read_csv(StringIO(out.decode('utf-8')), sep='\t')

        # Orient the data frame by records
        output = loads(data_frame.to_json(orient='records'))

        return output

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        if 'OLLIE_HOME' in os.environ:
            del os.environ['OLLIE_HOME']
