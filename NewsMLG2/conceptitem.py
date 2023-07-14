"""
Concept Item
"""

from .anyitem import (
    AnyItem, Assert, DerivedFrom, DerivedFromValue, InlineRef
)
from .contentmeta import ContentMetadataAcDType
from .concepts import Concept


class ConceptItemContentMeta(ContentMetadataAcDType):
    """
    Content Metadata for a Concept Item
    User Note: For multiple concepts use a Knowledge Item
    """
    xml_element_name = 'contentMeta'


class ConceptItem(AnyItem):
    """
    An Item containing information about a concept.
    """
    elements = [
        ('contentmeta', {
            'type': 'single', 'xml_name': 'contentMeta',
            'element_class': ConceptItemContentMeta
        }),
        ('assert', {
            'type': 'array', 'xml_name': 'assert', 'element_class': Assert
        }),
        ('inlineref', {
            'type': 'array', 'xml_name': 'inlineRef',
            'element_class': InlineRef
        }),
        ('derivedfrom', {
            'type': 'array', 'xml_name': 'derivedFrom',
            'element_class': DerivedFrom
        }),
        ('derivedfromvalue', {
            'type': 'array', 'xml_name': 'derivedFromValue',
            'element_class': DerivedFromValue
        }),
        ('concept', {
            'type': 'single', 'xml_name': 'concept',
            'element_class': Concept
        })
    ]
