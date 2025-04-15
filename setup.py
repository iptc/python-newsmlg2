from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.7'

setup(
  name = 'newsmlg2',
  packages = find_packages(exclude=['contrib', 'docs']),
  version = VERSION,
  description = 'Python implementation of the NewsML-G2 standard (https://iptc.org/standards/newsml-g2/)',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  author = 'Brendan Quinn',
  author_email = 'office@iptc.org',
  url = 'https://github.com/iptc/python-newsmlg2',
  download_url = 'https://github.com/iptc/python-newsmlg2/archive/v'+VERSION+'.tar.gz',
  keywords = ['api', 'media', 'publishing', 'news', 'syndication'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
  install_requires=[
    'lxml',
  ],
  include_package_data=True,
  package_data={'': ['catalogs/*']},
  python_requires='>=3',
  tests_require=['pytest'],
)
