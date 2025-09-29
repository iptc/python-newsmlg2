#!/usr/bin/env python

"""
Implementation of the NewsML-G2 standard for representing news and media
content.
"""

from .anyitem import *
from .attributegroups import *
from .catalog import *
from .catalogitem import *
from .catalogstore import *
from .complextypes import *
from .conceptitem import *
from .concepts import *
from .conceptrelationships import *
from .contentmeta import *
from .core import *
from .document import NewsMLG2Document
from .entities import *
from .extensionproperties import *
from .events import *
from .ids import *
from .itemmanagement import *
from .knowledgeitem import *
from .labeltypes import *
from .link import *
from .newsitem import *
from .newsmessage import *
from .packageitem import *
from .partmeta import *
from .planningitem import *
from .rights import *
from .simpletypes import *
from .utils import *

VERSION = 1.0
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
