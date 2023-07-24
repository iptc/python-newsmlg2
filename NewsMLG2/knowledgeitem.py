#!/usr/bin/env python

"""
KnowledgeItem - one of the main Item classes in NewsML-G2
"""

from .anyitem import (
    AnyItem, Assert, DerivedFrom, DerivedFromValue, InlineRef
)
from .attributegroups import (
    AuthorityAttributes, CommonPowerAttributes
)
from .catalog import SameAsScheme
from .complextypes import Name
from .concepts import Concept, Definition, Note
from .extensionproperties import Flex2ExtPropType
from .conceptrelationships import Related
from .contentmeta import ContentMetadataAcDType
from .partmeta import PartMeta


class ConceptSet(CommonPowerAttributes):
    """
    An unordered set of concepts
    """

    elements = [
        ('concept', {
            'type': 'array', 'xml_name': 'concept',
            'element_class': Concept
        })
    ]


class SchemeMetaExtPropertyElement(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """


class SchemeMetaExtProperty(Flex2ExtPropType):
    """
    Array of SchemeMetaExtProperty objects.
    """
    element_class = SchemeMetaExtPropertyElement


class SchemeMeta(AuthorityAttributes, CommonPowerAttributes):
    """
    Metadata about a scheme conveyed by a Knowledge Item
    """

    elements = [
        ('sameasscheme', {
            'type': 'array', 'xml_name': 'sameAsScheme',
            'element_class': SameAsScheme
        }),
        ('name', {
            'type': 'array', 'xml_name': 'name',
            'element_class': Name
        }),
        ('definition', {
            'type': 'array', 'xml_name': 'definition',
            'element_class': Definition
        }),
        ('note', {
            'type': 'array', 'xml_name': 'note',
            'element_class': Note
        }),
        ('related', {
            'type': 'array', 'xml_name': 'related',
            'element_class': Related
        }),
        ('schememetaextproperty', {
            'type': 'array', 'xml_name': 'schemeMetaExtProperty',
            'element_class': SchemeMetaExtProperty
        })
    ]
    attributes = {
        # The URI which identifies the scheme
        'uri': {
            'xml_name': 'uri',
            'xml_type': 'IRIType',
            'use': 'required'
        },
        # The alias preferred by the schema authority
        'preferredalias': {
            'xml_name': 'preferredalias'
        },
        # List of all concept types used within this Knowledge Item
        'concepttype': {
            'xml_name': 'concepttype',
            'xml_type': 'QCodeListType'
        },
        # The date (and, optionally, the time) when the scheme was created.
        # This must not be later than the creation timestamp of any concepts in
        # the scheme (identified by the schemeMeta @uri).
        'schemecreated': {
            'xml_name': 'schemecreated',
            'xml_type': 'DateOptTimeType',
            'use': 'optional'
        },
        # The date (and, optionally, the time) when the scheme was last
        # modified. The initial value is the date (and, optionally, the time)
        # of creation of the scheme (identified by the schemeMeta @uri).
        'schememodified': {
            'xml_name': 'schememodified',
            'xml_type': 'DateOptTimeType',
            'use': 'optional'
        },
        # The date (and, optionally, the time) after which the scheme should not
        # be used anymore. If a scheme is marked as retired, then all concepts
        # in that scheme (identified by the schemeMeta @uri) must also be
        # retired.
        'schemeretired': {
            'xml_name': 'schemeretired',
            'xml_type': 'DateOptTimeType',
            'use': 'optional'
        }
    }


class KnowledgeItemContentMeta(ContentMetadataAcDType):
    """
    Content Metadata for a Knowledge Item
    """
    xml_element_name = 'contentMeta'


class KnowledgeItem(AnyItem):
    """
    An Item used for collating a set of concept definitions to form the physical
    representation of a controlled vocabulary
    """

    elements = [
        ('contentmeta', {
            'type': 'single', 'xml_name': 'contentMeta',
            'element_class': KnowledgeItemContentMeta
        }),
        ('partmeta', {
            'type': 'array', 'xml_name': 'partMeta',
            'element_class': PartMeta
        }),
        ('assert', {
            'type': 'array', 'xml_name': 'assert',
            'element_class': Assert
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
        ('conceptset', {
            'type': 'single', 'xml_name': 'conceptSet',
            'element_class': ConceptSet
        }),
        ('schememeta', {
            'type': 'single', 'xml_name': 'schemeMeta',
            'element_class': SchemeMeta
        })
    ]
