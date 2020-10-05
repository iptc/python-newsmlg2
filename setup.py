from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.1'

setup(
  name = 'newsmlg2',
  packages=find_packages(exclude=['contrib', 'docs', 'tests']),
  version = VERSION,
  description = 'Python implementation of the NewsML-G2 standard (https://iptc.org/standards/newsml-g2/)',
  long_description=long_description,
  author = 'Brendan Quinn',
  author_email = 'brendan@iptc.org',
  url = 'https://github.com/iptc/python-newsmlg2',
  download_url = 'https://github.com/iptc/python-newsmlg2/archive/'+VERSION+'.tar.gz',
  keywords = ['api', 'media', 'publishing', 'news', 'syndication'],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
  python_requires='>=3',
)
