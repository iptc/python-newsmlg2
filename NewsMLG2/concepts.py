#!/usr/bin/env python

"""
Handle concepts, including concept names.
"""

from .core import GenericArray
from .attributegroups import (
    CommonPowerAttributes, TimeValidityAttributes
)
from .complextypes import ConceptNameType
from .labeltypes import BlockType


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
