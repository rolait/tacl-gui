import hashlib
from pathlib import Path

from app.validatable.CorpusPath import CorpusPath


class Witness:

    def __init__(self, corpusPath: CorpusPath, work: str, name: str):
        if work is None or work.strip() == '':
            raise ValueError('The work name must not be None or empty.')
        if name is None or name.strip() == '':
            raise ValueError('The witness name must not be None or empty.')

        self._work = work
        self._name = name

        # witnesses always have the suffix ".txt" (lower case).
        self._path = Path(corpusPath.asPath(), work, name + ".txt")

    def exists(self) -> bool:
        return self._path.exists()

    def calculateChecksum(self) -> str:
        if not self.exists():
            raise RuntimeError("Can not calculate md5sum. File {} does not exist.".format(self._path))

        with open(self._path, mode='r', encoding='utf-8') as file:
            return hashlib.md5(file.read().encode('utf-8')).hexdigest()

    def __str__(self):
        return '{}/{}'.format(self._work, self._name)
