#!/usr/bin/env python

"""
Implementation of the NewsML-G2 standard for representing news and media
content.
"""

from .catalogstore import CatalogStore, AliasNotFoundInCatalogs
from .document import NewsMLG2Document

VERSION = 0.1
DEBUG = True

__version__ = VERSION
__all__ = (
    # TODO 'CatalogItem',
    'ConceptItem',
    'KnowledgeItem',
    'NewsItem',
    # TODO 'PackageItem',
    # TODO 'PlanningItem',
    # TODO 'NewsMessage',
    '__version__'
)
__author__ = 'International Press Telecommuications Council'
__license__ = "MIT"
