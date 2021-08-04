#!/usr/bin/env python

"""
CatalogItem
"""

import os
from lxml import etree

from .core import NEWSMLG2NSPREFIX, BaseObject
from .anyitem import AnyItem
from .catalog import Catalog
from .contentmeta import ContentMetadataCatType


class CatalogItemContentMeta(ContentMetadataCatType):
    """
    Content Metadata for a Planning Item
    """
    xml_element_name = 'contentMeta'


class CatalogContainer(BaseObject):
    """
    The container of a single catalog
    """
    elements = [
        ('catalog', {
            'type': 'single', 'xml_name': 'catalog',
            'element_class': Catalog
        })
    ]


class CatalogItem(AnyItem):
    """
    An Item containing a single managed NewsML-G2 catalog
    """
    elements = [
        ('contentmeta', {
            'type': 'single', 'xml_name': 'contentMeta',
            'element_class': CatalogItemContentMeta
        }),
        ('catalogcontainer', {
            'type': 'single', 'xml_name': 'catalogContainer',
            'element_class': CatalogContainer
        })
    ]
