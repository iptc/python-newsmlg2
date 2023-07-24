#!/usr/bin/env python

"""
Concept relationship classes - move merge with concepts.py
"""

from .core import BaseObject, QCodeURIMixin
from .attributegroups import (
    ArbitraryValueAttributes, CommonPowerAttributes, FlexAttributes,
    I18NAttributes, QuantifyAttributes, TimeValidityAttributes
)
from .complextypes import Name


class HierarchyInfo(CommonPowerAttributes):
    """
    Represents the position of a concept in a hierarchical taxonomy tree by a
    sequence of QCode tokens representing the ancestor concepts and this concept
    """

class FlexPropType(CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible generic type for both controlled and uncontrolled values
    """

    elements = [
        ('name', { 'type': 'array', 'xml_name': 'name', 'element_class': Name }),
        ('hierarchyinfo', {
            'type': 'array', 'xml_name': 'hierarchyInfo',
            'element_class': HierarchyInfo
        })
    ]


class SameAsType(FlexPropType, TimeValidityAttributes):
    """
    The type for an identifier of an equivalent concept
    (Type defined in this XML Schema only)
    """


class SameAs(SameAsType):
    """
    An identifier of a concept with equivalent semantics
    """


class QCodePropType(QCodeURIMixin, CommonPowerAttributes):
    """
    The type for a property with a QCode value in a qcode attribute
    """


class Bag(QCodePropType, QuantifyAttributes):
    """
    A group of existing concepts which express a new concept.
    """

    attributes = {
        # The type of the concept assigned as controlled property value -
        # expressed by a QCode
        'type': {
            'xml_name': 'type',
            'xml_type': 'QCodeType'
        },
        # The type of the concept assigned as controlled property value -
        # expressed by a URI
        'typeuri': {
            'xml_name': 'typeuri',
            'xml_type': 'IRIType'
        },
        # Indicates how significant the event expressed by a bit of event
        # concept type is to the concept expressed by this bit The scope of this
        # relationship is limited to the bits of a single bag. See also the note
        # below the table.
        'significance': {
            'xml_name': 'significance',
            'xml_type': 'Int100Type'
        }
    }


class Facet(FlexPropType, TimeValidityAttributes):
    """
    In NAR 1.8 and later, facet is deprecated and SHOULD NOT (see RFC 2119) be
    used, the "related" property should be used instead.
    (was: An intrinsic property of the concept.)
    """
    attributes = {
        # The identifier of the relationship between the current concept
        # (containing the facet) and the concept identified by the facet value
        # - expressed by a QCode
        'rel': {
            'xml_name': 'rel',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The identifier of the relationship between the current concept
        # (containing the facet) and the concept identified by the facet value
        # - expressed by a URI
        'reluri': {
            'xml_name': 'reluri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # DO NOT USE this attribute, for G2 internal maintenance purposes only.
        'g2flag': {
            'xml_name': 'g2flag',
            'xml_type': 'xs:string',
            'use': 'optional" fixed="DEPR'
        }
    }


class RelatedConceptRelated(FlexPropType, TimeValidityAttributes,
    ArbitraryValueAttributes):
    """
    A related concept, where the relationship is different from 'sameAs',
    'broader' or 'narrower'.
    (for some reason RelatedConceptType defines this separately rather than
    re-using the Related class)
    """
    xml_element_name = 'related'
    attributes = {
        # The identifier of the relationship between the current concept and the
        # target concept - expressed by a QCode
        'rel': {
            'xml_name': 'rel',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The identifier of the relationship between the current concept and the
        # target concept - expressed by a URI
        'reluri': {
            'xml_name': 'reluri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The rank of the current concept among concepts having a relationship
        # to the target concept.
        'rank': {
            'xml_name': 'rank',
            'xml_type': 'xs:nonNegativeInteger'
        }
    }


class RelatedConceptType(FlexPropType, TimeValidityAttributes):
    """
    The type for an identifier of a related concept
    """

    elements = [
        ('facet', {
            'type': 'array', 'xml_name': 'facet', 'element_class': Facet
        }),
        ('related', {
            'type': 'array', 'xml_name': 'related',
            'element_class': RelatedConceptRelated
        }),
        ('sameas', {
            'type': 'array', 'xml_name': 'sameAs', 'element_class': SameAs
        })
    ]
    attributes = {
        # The identifier of the relationship between the current concept and the
        # target concept - expressed by a QCode
        'rel': {
            'xml_name': 'rel',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The identifier of the relationship between the current concept and the
        # target concept - expressed by a URI
        'reluri': {
            'xml_name': 'reluri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The rank of the current concept among concepts having a relationship
        # to the target concept.
        'rank': {
            'xml_name': 'rank',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        }
    }


class MainConcept(RelatedConceptType):
    """
    The concept which is faceted by other concept(s) asserted by facetConcept
    """


class FacetConcept(RelatedConceptType):
    """
    The concept which is faceting another concept asserted by mainConcept
    """


class Broader(RelatedConceptType):
    """
    An identifier of a more generic concept.
    """


class Narrower(RelatedConceptType):
    """
    An identifier of a more specific concept.
    """


class FlexRelatedConceptType(RelatedConceptType, ArbitraryValueAttributes):
    """
    The type for identifying a related concept
    """
    elements = [
        ('bag', { 'type': 'single', 'xml_name': 'bag', 'element_class': Bag })
    ]


class Related(FlexRelatedConceptType):
    """
    A related concept, where the relationship is different from 'sameAs',
    'broader' or 'narrower'.
    """


class QualRelPropType(QCodePropType, I18NAttributes):
    """
    Type for a property with a  QCode value in a qcode attribute, a URI in
    a uri attribute and optional names and related concepts
    """

    elements = [
        ('name', { 'type': 'array', 'xml_name': 'name', 'element_class': Name }),
        ('hierarchyinfo', {
            'type': 'array', 'xml_name': 'hierarchyInfo',
            'element_class': HierarchyInfo
        }),
        ('related', {
            'type': 'array', 'xml_name': 'related', 'element_class': Related
        })
    ]


class FlexProp2Type(CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible type for related concepts for both controlled and uncontrolled
    values
    """

    elements = [
        ('name', { 'type': 'array', 'xml_name': 'name', 'element_class': Name }),
        ('hierarchyinfo', {
            'type': 'array', 'xml_name': 'hierarchyInfo',
            'element_class': HierarchyInfo
        }),
        ('sameas', {
            'type': 'array', 'xml_name': 'sameAs', 'element_class': SameAs
        })
    ]


class FlexRelatedPropType(FlexProp2Type):
    """
    Flexible generic type for both controlled and uncontrolled values of a
    related concept
    """
    attributes = {
        # The identifier of the relationship between the concept containing the
        # related property and the concept identified by the related value -
        # expressed by a QCode
        'rel': {
            'xml_name': 'rel',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The identifier of the relationship between the concept containing the
        # related property and the concept identified by the related value -
        # expressed by a URI
        'reluri': {
            'xml_name': 'reluri',
            'xml_type': 'IRIType',
            'use': 'optional'
        }
    }


ConceptRelationshipsGroup = [
    ('sameas', {
        'type': 'array', 'xml_name': 'sameAs', 'element_class': SameAs
    }),
    ('broader', {
        'type': 'array', 'xml_name': 'broader', 'element_class': Broader
    }),
    ('narrower', {
        'type': 'array', 'xml_name': 'narrower', 'element_class': Narrower
    }),
    ('related', {
        'type': 'array', 'xml_name': 'related', 'element_class': Related
    })
]
