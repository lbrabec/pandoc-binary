import os
import sys


def main():
    pandoc = os.path.join(os.path.dirname(__file__), "data", "bin", "pandoc")
    os.execl(pandoc, pandoc, *sys.argv[1:])
