#!/usr/bin/env python

import argparse
import os
import sys

# because we want to reference a module that hasn't been installed yet
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..'))

from NewsMLG2 import NewsMLG2Document

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load NewsML-G2 instance file')
    parser.add_argument('filename', help='file to be loaded')
    args = parser.parse_args()

    document = NewsMLG2Document(args.filename)

    print(document.to_xml())
