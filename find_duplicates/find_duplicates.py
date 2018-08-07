import os, sys
import hashlib
import collections

HEAD = 4096
BLOCK = 4096

class Digest:
    NONE = -1
    SIZE = 0
    HEAD = 1
    MD5 = 2

    def __init__(self):
        self.kind = Digest.NONE
        self.value = [None] * 3

    def get(self):
        return (self.kind, self.value[self.kind] if self.kind >= 0 else None)

    @staticmethod
    def _getSize(path):
        statinfo = os.stat(path)

        return statinfo.st_size
 
    @staticmethod
    def _getMD5(path, size):
        m = hashlib.md5()

        with open(path, 'rb') as f:
            while True:
                to_read = min(size, BLOCK) if size > 0 else BLOCK

                chunk = f.read(to_read)

                if (size > 0) and (len(chunk) < to_read):
                    raise Exception("Filed to read {}".format(path))

                m.update(chunk)

                if size > 0: size -= to_read

                if len(chunk) < BLOCK: 
                    break

        return m.digest()

    def update(self, kind, path):
        if kind == Digest.SIZE:   value = self._getSize(path)
        elif kind == Digest.HEAD: value = self._getMD5(path, HEAD)
        elif kind == Digest.MD5:  value = self._getMD5(path, 0)
        else:
            raise Exception("Unknown digest {}.".format(kind))

        self.kind = kind
        self.value[self.kind] = value

    def improve(self, path):
        if self.kind < Digest.MD5:
            self.update(self.kind + 1, path)

class FileEntry:
    def __init__(self, path):
        self.path = path
        self.digest = Digest()

    def improve(self):
        self.digest.improve(self.path)
        return self.digest.get()

    def digest(self):
        return digest.get()


def find_duplicates(dir):
    """ Find duplicates in all files of dir directory. 
    """

    FILES = []

    # Get the list of files to process
    for dirName, subdirList, fileList in os.walk(dir):
        for fn in fileList:
            fname = os.path.join(dirName, fn)

            FILES.append(FileEntry(fname))

    BY_DIGEST = collections.defaultdict({ (Digest.NONE, None) : FILES })

    kind = Digest.NONE

    # Increasing Digest strength, filtering out non-duplicates.
    while (len(BY_DIGEST) > 0) and (kind <= Digest.MD5):
        BY_DIGEST_NEW = collections.defaultdict()

        for (d,fes) in BY_DIGEST.items():
            if len(fes) > 1:
                for f in fes:
                    BY_DIGEST_NEW[f.improve()].append(f)

        BY_DIGEST = BY_DIGEST_NEW
        kind += 1

    for (d, fes) in BY_DIGEST.items():
        print ("[" + ", ".join(map(lambda f: f.path, fes)) + "]")


def main():
    if len(sys.argv) != 2:
        print("{}: <direcotry>".format(sys.argv[0]))
        return 1

    find_duplicates(sys.argv[1])

    return 0

if __name__=="__main__":
    sys.exit(main())
