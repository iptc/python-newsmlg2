#!/usr/bin/env python

"""
Implementation of the NewsML-G2 standard for representing news and media
content.
"""

VERSION = 0.1
from .catalogstore import CatalogStore, AliasNotFoundInCatalogs
from .document import NewsMLG2Document

__version__ = VERSION
__all__ = (
    # TODO 'CatalogItem',
    # TODO 'ConceptItem',
    # TODO 'KnowledgeItem',
    'NewsItem',
    # TODO 'PackageItem',
    # TODO 'PlanningItem',
    # TODO 'NewsMessage',
    '__version__'
)
__author__ = 'International Press Telecommuications Council'
__license__ = "MIT"
