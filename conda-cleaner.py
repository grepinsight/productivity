from os import environ, remove, rmdir
from shutil import rmtree
from sys import version_info

import importlib_metadata as metadata

MODULES_PATH = [
    f"{environ['CONDA_PREFIX']}/lib/python{version_info.major}.{version_info.minor}/site-packages"
]

if __name__ == "__main__":
    for pkg in filter(
        lambda a: a.metadata["name"] is None, metadata.distributions(path=MODULES_PATH)
    ):
        print("Erasing", pkg._path)
        if pkg._path.is_dir():
            print("rmtree %s" % pkg._path)
            rmtree(pkg._path)
        else:
            print("remove %s" % pkg._path)
            remove(pkg._path)
