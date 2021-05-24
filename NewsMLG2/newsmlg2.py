#!/usr/bin/env python

from lxml import etree
import json

from .core import NEWSMLG2, BaseObject, GenericArray
from .complextypes import *
from .labeltypes import BlockType


class CatalogRefElement(BaseObject):
    """
    A reference to a remote catalog. A hyperlink to a set of scheme alias declarations.
    """
    attributes = {
        # A short natural language name for the catalog.
        'title': 'title',
        # A hyperlink to a remote Catalog.
        'href': 'href'
    }


class CatalogRef(GenericArray):
    """
    A reference to document(s) listing externally-supplied controlled vocabularies.
    The catalog file can be in NewsML 1.
    """
    element_class = CatalogRefElement


# TODO: probably should move this into its own file, rightsinformation.py ??
# with rightsinfo etc
class RightsBlockType(BlockType):
    """
    An expression of rights in natural language or as a reference to remote information
    """
    attributes = {
        # The locator of a remote expression of rights
        'href': 'href',  # type="IRIType"
    }

    def __init__(self, **kwargs):
        super(RightsBlockType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if xmlelement.text:
            self.text = xmlelement.text.strip()

    def __str__(self):
        return self.text
