#!/usr/bin/env python

"""
Implementation of the NewsML-G2 standard for representing news and media
content.
"""

from .anyitem import ItemMeta
from .catalog import Catalog, Scheme
from .catalogitem import CatalogItem, CatalogItemContentMeta
from .catalogstore import CatalogStore, AliasNotFoundInCatalogs, URINotFoundInCatalogs
from .conceptitem import ConceptItem, ConceptItemContentMeta
from .core import GenericArray
from .document import NewsMLG2Document
from .events import Event, Events, EventDetails
from .knowledgeitem import KnowledgeItem, KnowledgeItemContentMeta
from .newsitem import NewsItem, NewsItemContentMeta
from .newsmessage import NewsMessage
from .packageitem import PackageItem, PackageItemContentMeta
from .planningitem import PlanningItem, PlanningItemContentMeta
from .utils import qcode_to_uri, uri_to_qcode

VERSION = 0.6
NEWSMLG2_VERSION = 2.33
DEBUG = True

__version__ = VERSION
__all__ = (
    'CatalogItem',
    'ConceptItem',
    'KnowledgeItem',
    'NewsItem',
    'PackageItem',
    'PlanningItem',
    'NewsMessage',
    '__version__'
)
__author__ = 'International Press Telecommuications Council'
__license__ = "MIT"
