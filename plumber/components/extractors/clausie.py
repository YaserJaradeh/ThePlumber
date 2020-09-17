import abc
import urllib.request
import os.path
import zipfile
import os
import subprocess
import tempfile
from collections import namedtuple
from plumber.components.extractors import BaseExtractor
from plumber.components.format import Triple as PTriple
from typing import List
import nltk


DEFAULT_CLAUSIE_VERSION = '0-0-1'

INSTALL_DIR = '~/.pyclausie_resources/'


class ClausIE:
    """ This is an abstract base class for extracting triples from a
        sentence using ClausIE. To use this, you'll need to instantiate
        one of the backends. You can do this via the get_instance()
        helper method.
        If you don't have the needed clausie jar file the flag
        download_if_missing will fetch it for you.
        Subclasses need to override the extract_triples method.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, jar_filename=None, download_if_missing=False,
                 version=None):
        """ jar_filename should point to calusie.jar. If you don't
            have this jar file the download_if_missing parameter can
            be set which will retrieve the file for you.
        """
        if not (jar_filename is not None or download_if_missing):
            raise ValueError("Must set either jar_filename or "
                             " download_if_missing to True.")

        self.jar_filename = jar_filename
        if self.jar_filename is None:
            if version is None:
                version = DEFAULT_CLAUSIE_VERSION
            filename = 'clausie/clausie.jar'
            self.jar_filename = self.setup_and_get_default_path(filename)
            if download_if_missing:
                self.download_if_missing(version)

    @abc.abstractmethod
    def extract_triples(self, sentences, ids=None, **kwargs):
        """ extract triples from list of sentences."""

    def setup_and_get_default_path(self, jar_base_filename):
        install_dir = os.path.expanduser(INSTALL_DIR)
        try:
            os.makedirs(install_dir)
        except OSError:
            pass
        jar_filename = os.path.join(install_dir, jar_base_filename)
        return jar_filename

    def download_if_missing(self, version=None, verbose=True):
        """ This method will download and extract the clausie zip
            file if it does not already exist.
        """
        if os.path.exists(self.jar_filename):
            return

        jar_url = self.get_jar_url(version)
        filename = 'clausie-%s.zip' % version
        install_dir = os.path.expanduser(INSTALL_DIR)
        zip_filename = os.path.join(install_dir, filename)
        if verbose:
            print("Downloading %r -> %r" % (jar_url, zip_filename))
        opener = ErrorAwareURLOpener()
        opener.retrieve(jar_url, filename=zip_filename)
        with zipfile.ZipFile(zip_filename, 'r') as zip_file:
            zip_file.extractall(install_dir)

    @staticmethod
    def get_jar_url(version=None):
        if version is None:
            version = DEFAULT_CLAUSIE_VERSION
        if not isinstance(version, str):
            raise TypeError("Version must be a string or None (got %r)." %
                            version)
        filename = 'clausie-%s.zip' % version
        return 'http://resources.mpi-inf.mpg.de/d5/clausie/' \
                '%s' % filename

    @staticmethod
    def get_instance(jar_filename=None, version=None,
                     download_if_missing=True, backend='subprocess',
                     **extra_args):
        extra_args.update(jar_filename=jar_filename,
                          download_if_missing=download_if_missing,
                          version=version)

        if backend == 'subprocess':
            return SubprocessBackend(**extra_args)

        raise ValueError("Unknown backend: %r (known backends: "
                         "'subprocess')" % backend)


class ErrorAwareURLOpener(urllib.request.FancyURLopener):
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        raise ValueError("Error downloading %r: %s %s" %
                         (url, errcode, errmsg))


class SubprocessBackend(ClausIE):
    """ Interface to ClausIE using subprocess. This creates a java call
        to clausie.jar.
    """

    def __init__(self, jar_filename=None, download_if_missing=False,
                 version=None, java_command='java'):
        """ java_command is the path the the java binary.
        """
        ClausIE.__init__(self, jar_filename, download_if_missing,
                         version)
        self.java_command = java_command

    def extract_triples(self, sentences, ids=None, java='java',
                        print_sent_confidence=False):
        """ This method takes a list of sentences and ids (optional)
            then returns a list of triples extracted by ClausIE.
            currently supported options:
                -l - Used if ids is a list and not None.
                -p - Returns the confidence score of the extracted
                     triple.

            Note: sentences and ids must be a list even if you only
                  extract triples for one sentence.
        """
        input_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            if ids is not None:
                for identifier, sentence in zip(ids, sentences):
                    input_file.write('{0!r}\t{1!r}\n'.format(identifier, sentence).encode('utf8'))
            else:
                for sentence in sentences:
                    input_file.write('{0!r}\n'.format(sentence).encode('utf8'))
            input_file.flush()

            command = [self.java_command,
                       '-jar', self.jar_filename,
                       '-f', input_file.name]
            if ids is not None:
                command.append('-l')
            if print_sent_confidence:
                command.append('-p')
            sd_process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
            return_code = sd_process.wait()
            stderr = sd_process.stderr.read()
            stdout = sd_process.stdout.read()
            self._raise_on_bad_exitcode(return_code, stderr)
        finally:
            os.remove(input_file.name)

        triples = Corpus.from_tsv(stdout.splitlines(), print_sent_confidence)
        return triples

    @staticmethod
    def _raise_on_bad_exitcode(return_code, stderr):
        if return_code:
            print('stderr:', stderr)
            raise ValueError("Bad exit code from ClausIE.")


FIELD_NAMES = ('index', 'subject', 'predicate', 'object', 'confidence')


class Triple(namedtuple('Triple', FIELD_NAMES)):
    """ Inherits from namedtuple. This tuple contains the fields index,
        subject, predicate, object, and confidence.
    """
    def __repr__(self):
        items = [(field, getattr(self, field, None)) for field in FIELD_NAMES]
        fields = ['%s=%r' % (k, v) for k, v in items if v is not None]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(fields))


class Corpus(list):
    """ Inherits from list. Corpus parses the ClausIE output and stores
        a list of Triple.
    """
    @classmethod
    def from_tsv(cls, stream, print_sent_confidence):
        stream = iter(stream)
        corpus = cls()
        for line in stream:
            if not print_sent_confidence:
                if len(line.decode().split('\t')) != 4:
                    continue
                (ident, subj, pred, obj) = line.decode().split('\t')
                triple = Triple(ident, subj.strip('"'), pred.strip('"'),
                                obj.strip('"'), None)
                corpus.append(triple)
            else:
                if len(line.decode().split('\t')) != 5:
                    continue
                (ident, subj, pred, obj, conf) = line.decode().split('\t')
                triple = Triple(ident, subj.strip('"'), pred.strip('"'),
                                obj.strip('"'), conf.strip('"'))
                corpus.append(triple)
        return corpus


class ClausIEExtractor(BaseExtractor):

    def __init__(self, **kwargs):
        super().__init__(name='ClausIE extractor', **kwargs)
        self.cl = ClausIE.get_instance()

    def get_triples(self, text) -> List[PTriple]:
        sentences = nltk.sent_tokenize(text)
        triples = self.cl.extract_triples(sentences)
        plumber_triples = []
        for triple in triples:
            trp = PTriple()
            # ========== Subject ==============
            if triple.subject not in text:
                continue
            start_index = text.index(triple.subject)
            end_index = start_index + len(triple.subject)
            trp.add_subject(triple.subject, start_index, end_index, text)
            # ========== Predicate ==============
            if triple.predicate not in text:
                continue
            start_index = text.index(triple.predicate)
            end_index = start_index + len(triple.predicate)
            trp.add_predicate(triple.predicate, start_index, end_index, text)
            # ========== Object ==============
            if triple.object not in text:
                continue
            start_index = text.index(triple.object)
            end_index = start_index + len(triple.object)
            trp.add_object(triple.object, start_index, end_index, text)
            # ========== Add triple to final output
            plumber_triples.append(trp)
        return plumber_triples


if __name__ == '__main__':
    extractor = ClausIEExtractor()
    x = extractor.get_triples(text="Barack Obama is the president of the United States of America")
