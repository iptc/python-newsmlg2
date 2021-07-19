#!/usr/bin/env python

"""
Implementation of the NewsML-G2 standard for representing news and media
content.
"""

from .anyitem import ItemMeta
from .catalogstore import CatalogStore, AliasNotFoundInCatalogs
from .document import NewsMLG2Document
from .newsitem import NewsItem
from .packageitem import PackageItem

VERSION = 0.2
DEBUG = True

__version__ = VERSION
__all__ = (
    # TODO 'CatalogItem',
    'ConceptItem',
    'KnowledgeItem',
    'NewsItem',
    'PackageItem',
    # TODO 'PlanningItem',
    # TODO 'NewsMessage',
    '__version__'
)
__author__ = 'International Press Telecommuications Council'
__license__ = "MIT"
