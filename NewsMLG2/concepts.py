#!/usr/bin/env python

"""
Handle concepts, including concept names.
"""

from lxml import etree

from .core import GenericArray
from .attributegroups import (
    CommonPowerAttributes, TimeValidityAttributes
)
from .complextypes import IntlStringType, Name, ConceptNameType
from .labeltypes import BlockType

#class ConceptNameType(TimeValidityAttributes, IntlStringType):
#    """
#    The type of a natural language name for the concept (Type defined in this
#    XML Schema only)
#    """
#    name = None
#    attributes = {
#        # A refinement of the semantics of the name - expressed by a QCode
#        'role': 'role',
#        # A refinement of the semantics of the name - expressed by a URI
#        'roleuri': 'roleuri',
#        # Specifies which part of a full name this property provides - expressed
#        # by a QCode
#        'part': 'part',
#        # Specifies which part of a full name this property provides - expressed
#        # by a URI
#        'parturi': 'parturi'
#    }
#
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        xmlelement = kwargs.get('xmlelement')
#        if isinstance(xmlelement, etree._Element):
#            self.name = xmlelement.text.strip()
#
#    name_role_mappings = {
#        # http://cv.iptc.org/newscodes/namerole/
#        # http://cv.iptc.org/newscodes/namerole/adjectival
#        'nrol:adjectival': 'adjectival',
#        'nrol:alternate': 'alternate',    # http://cv.iptc.org/newscodes/namerole/alternate
#        'nrol:display': 'display',        # http://cv.iptc.org/newscodes/namerole/display
#        'nrol:full': 'full',              # http://cv.iptc.org/newscodes/namerole/full
#        'nrol:mnemonic': 'mnemonic',      # http://cv.iptc.org/newscodes/namerole/mnemonic
#        'nrol:short': 'short',            # http://cv.iptc.org/newscodes/namerole/short
#        'nrol:sort': 'sort',              # http://cv.iptc.org/newscodes/namerole/sort
#        'nrol:synonym': 'synonym',        # http://cv.iptc.org/newscodes/namerole/synonym
#        # http://cv.iptc.org/newscodes/namepart/
#        'nprt:acadTitle': 'acadTitle',    # http://cv.iptc.org/newscodes/namepart/acadTitle
#        'nprt:family': 'family',          # http://cv.iptc.org/newscodes/namepart/family
#        'nprt:given': 'given',            # http://cv.iptc.org/newscodes/namepart/given
#        'nprt:middle': 'middle',          # http://cv.iptc.org/newscodes/namepart/middle
#        # http://cv.iptc.org/newscodes/namepart/salutation
#        'nprt:salutation': 'salutation',
#        # temporary hacks while we decide what to fix
#        'nprt:first': 'given',
#        'nrol:first': 'given',
#        'nprt:last': 'family',
#        'nrol:last': 'family',
#    }
#
#    def as_dict(self):
#        super().as_dict()
#        # the only place where we diverge from a direct match with the SportsML
#        role = self.attr_values.get('role', None)
#        part = self.attr_values.get('part', None)
#        if role and role in self.name_role_mappings.keys():
#            self.dict.update({
#                self.name_role_mappings[role]: self.name or ""
#            })
#            del self.dict['role']
#        elif part and part in self.name_role_mappings.keys():
#            self.dict.update({
#                self.name_role_mappings[part]: self.name or ""
#            })
#            del self.dict['part']
#        # elif self.name:
#        else:
#            self.dict.update({'name': self.name or ""})
#        return self.dict
#
#    def __str__(self):
#        return self.name


#class Name(GenericArray):
#    """
#    Array of ConceptNameType objects.
#    """
#    element_class = ConceptNameType


class DefinitionElement(BlockType, TimeValidityAttributes):
    """
    A natural language definition of the semantics of the concept. This
    definition is normative only for the scope of the use of this concept.
    """


class Definition(GenericArray):
    """
    Array of DefinitionElement objects.
    """
    element_class = ConceptNameType


class HierarchyInfoElement(CommonPowerAttributes):
    """
    Represents the position of a concept in a hierarchical taxonomy tree by a
    sequence of QCode tokens representing the ancestor concepts and this concept
    """

class HierarchyInfo(GenericArray):
    """
    Array of HierarchyInfoElement objects.
    """
    element_class = HierarchyInfoElement


class NoteElement(BlockType, TimeValidityAttributes):
    """
    Additional natural language information about the concept.
    """


class Note(GenericArray):
    """
    Array of NoteElement objects.
    """
    element_class = ConceptNameType
