#!/usr/bin/env python

"""
Implementation of the NewsML-G2 standard for representing news and media
content.
"""

from .core import VERSION
from .catalogstore import CatalogStore, AliasNotFoundInCatalogs
from .document import NewsMLG2Document

# from .catalogstore import *
# from .document import *
# from .newsitem import *

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

# ugly global/singleton - TODO do this a different way!
# CATALOG_STORE = CatalogStore()
