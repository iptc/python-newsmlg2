#!/usr/bin/env python

"""
AnyItemType definitions
"""

from lxml import etree

from .core import BaseObject, NEWSMLG2_VERSION, QCodeURIMixin
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, QuantifyAttributes
)
from .catalog import build_catalog, get_catalogs, CatalogRef, Catalog
from .complextypes import Name, TruncatedDateTimePropType
from .concepts import Flex1PropType
from .extensionproperties import Flex2ExtPropType
from .conceptrelationships import QualRelPropType, Related
from .itemmanagement import ItemManagementGroup
from .link import Link
from .rights import RightsInfo


class Action(QualRelPropType):
    """
    An action which is executed at this hop in the hop history.
    """
    attributes = {
        # The target of the action in a content object - expressed by a QCode.
        # If the target attribute is omitted the target of the action is the
        # whole object.
        'target': {
            'xml_name': 'target',
            'xml_type': 'QCodeType'
        },
        # The target of the action in a content object - expressed by a URI.
        # If the target attribute is omitted the target of the action is the
        # whole object.
        'targeturi': {
            'xml_name': 'targeturi',
            'xml_type': 'IRIType'
        },
        # The date and optionally the time (with a time zone) when this action
        # was performed on the target.
        'timestamp': {
            'xml_name': 'timestamp',
            'xml_type': 'DateOptTimeType'
        }
    }


class Hop(CommonPowerAttributes):
    """
    A single hop of the Hop History. The details of the hop entry should
    reflect the actions taken by a party.
    """
    elements = [
        ('party', {
            'type': 'array', 'xml_name': 'party', 'element_class': 'concepts.Party'
        }),
        ('action', {
            'type': 'array',
            'xml_name': 'action',
            'element_class': Action
        })
    ]
    attributes = {
        # The sequential value of this Hop in a sequence of Hops of a Hop
        # History.
        # Values need not to be consecutive. The sequence starts with the lowest
        # value.
        'seq': {
            'xml_name': 'seq',
            'xml_type': 'xs:nonNegativeInteger'
		},
        # The date and optionally the time (with a time zone) when this item's
        # content object was forwarded.
        'timestamp': {
            'xml_name': 'timestamp',
            'xml_type': 'DateOptTimeType'
		}
    }


class HopHistory(BaseObject):
    """
    A history of the creation and modifications of the content object of this
    item, expressed as a sequence of hops.
    """
    elements = [
        ('hop', { 'type': 'array', 'xml_name': 'hop', 'element_class': Hop })
    ]


class Timestamp(TruncatedDateTimePropType):
    """
    Time stamp representing an optionally truncated date and time
    """


class PublishedExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """


class Published(CommonPowerAttributes, QCodeURIMixin):
    """
    A step in the "pubHistory".
    """
    elements = [
        ('timestamp', {
            'type': 'single',
            'xml_name': 'timestamp',
            'element_class': Timestamp
        }),
        ('name', { 'type': 'array', 'xml_name': 'name', 'element_class': Name }),
        ('related', {
            'type': 'array', 'xml_name': 'related', 'element_class': Related
        }),
        ('publishedExtProperty', {
            'type': 'array',
            'xml_name': 'publishedExtProperty',
            'element_class': PublishedExtProperty
        })
    ]
    attributes = {
        # A free-text value assigned as property value.
        'literal': {
            'xml_name': 'literal',
            'xml_type': 'g2normalizedString'
		}
    }


class PubHistory(BaseObject):
    """
    One to many datasets about publishing this item.
    """
    elements = [
        ('published', {
            'type': 'array',
            'xml_name': 'published',
            'element_class': Published
        })
    ]


class ItemMetaExtProperty(Flex2ExtPropType):
    """
    Extension Property: the semantics are defined by the concept referenced by
    the rel attribute.
    The semantics of the Extension Property must have the same scope as the
    parent property.
    """


class ItemMetadataType(CommonPowerAttributes, I18NAttributes):
    """
    The type for a set of properties directly associated with the item
    (Type defined in this XML Schema only)
    """
    elements = ItemManagementGroup + [
        ('link', { 'type': 'array', 'xml_name': 'link', 'element_class': Link }),
        ('itemmetaextproperty', {
            'type': 'array',
            'xml_name': 'itemMetaExtProperty',
            'element_class': ItemMetaExtProperty
        })
    ]


class ItemMeta(ItemMetadataType):
    """
    A set of properties directly associated with the Item
    """
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        assert self.itemclass is not None, "itemClass is required in any NewsML-G2 Item"
        assert self.provider is not None, "provider is required in any NewsML-G2 Item"
        assert self.versioncreated is not None, "versionCreated is required in any NewsML-G2 Item"


class AnyItem(I18NAttributes):
    """
    An abstract class. All G2 items are inherited from this class.
    """

    attributes = {
        # The IPTC standard with which the Item is conformant.
        'standard': {
            'xml_name': 'standard',
            # NOTE: the XML Schema doesn't define a default but
            # we do, for ease of use reasons
            'default': 'NewsML-G2'
        },
        # The major-minor version of the IPTC standard with which the Item is conformant.
        'standardversion': {
            'xml_name': 'standardversion',
            # NOTE: the XML Schema doesn't define a default but
            # we default to the most recent version, for ease of use
            'default': NEWSMLG2_VERSION
        },
        # The conformance level with which the Item is conformant.
        'conformance': {
            'xml_name': 'conformance',
            # NOTE: the XML Schema defines default "core" but from 2.27+ the
            # Specification recommends only using "power"
            'default': 'power'
        },
        # The persistent, universally unique identifier common for all versions of the Item.
        'guid': {
            'xml_name': 'guid',
            'use': 'required'
        },
        # The version of the Item.
        'version': {
            'xml_name': 'version',
            'xml_type': 'positive integer',
            'default': '1'
        }
    }

    elements = [
        ('catalogref', { 'type': 'array', 'xml_name': 'catalogRef', 'element_class': CatalogRef }),
        ('catalog', { 'type': 'array', 'xml_name': 'catalog', 'element_class': Catalog }),
        ('hophistory', { 'type': 'single', 'xml_name': 'hopHistory', 'element_class': HopHistory }),
        ('pubhistory', { 'type': 'single', 'xml_name': 'pubHistory', 'element_class': PubHistory }),
        ('rightsinfo', { 'type': 'array', 'xml_name': 'rightsInfo', 'element_class': RightsInfo }),
        ('itemmeta', { 'type': 'single', 'xml_name': 'itemMeta', 'element_class': ItemMeta })
    ]

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            build_catalog(xmlelement)
            assert self.itemmeta is not None, "itemMeta is required in any NewsML-G2 Item"

    def get_catalogs(self):
        """
        Wrapper for global get_catalogs() function.
        """
        return get_catalogs()


class AssertType(CommonPowerAttributes, I18NAttributes):
    """
    The type of an assertion about a concept
    (Type defined in this XML Schema only)
    """
    attributes = {
        # A concept identifier.
        'qcode': {
            'xml_name': 'qcode',
            'xml_type': 'QCodeType',
            'use': 'optional'
		},
        # A URI which identifies a concept.
        'uri': {
            'xml_name': 'uri',
            'xml_type': 'IRIType',
            'use': 'optional'
		},
        # A free-text text string assigned as property value
        'literal': {
            'xml_name': 'literal',
            'xml_type': 'g2normalizedString',
            'use': 'optional'
		}
    }


class Assert(AssertType):
    """
    An assertion about a concept
    """


class InlineRef(Flex1PropType, QuantifyAttributes):
    """
    Inline reference
    The concept represented by the content identified by the local identifier(s)
    """
    attributes = {
        # A set of local identifiers of inline content
        'idrefs': {
            'xml_name': 'idrefs',
            'xml_type': 'xs:IDREFS',
			'use': 'required'
		}
    }


class DerivedFrom(Flex1PropType):
    """
    Refers to the ids of elements whose values have been derived from the
    concept represented by this property.
    """
    attributes = {
        # Refers to the ids of elements which values have been derived from the
        # concept represented by this property
        'idrefs': {
            'xml_name': 'idrefs',
            'xml_type': 'xs:IDREFS'
		}
    }


class DerivedFromValue(CommonPowerAttributes):
    """
    Represents the non-Concept value that was used for deriving the value of one
    or more properties in this NewsML-G2 item.
    """
    attributes = {
        # Refers to the id of the element that provides the value used for the
        # derivation.
        'sourceidref': {
            'xml_name': 'sourceidref',
            'xml_type': 'xs:IDREF',
			'use': 'required'
		},
        # Refers to the ids of elements whose values have been derived from the
        # value represented by this property.
        'idrefs': {
            'xml_name': 'idrefs',
            'xml_type': 'xs:IDREFS',
			'use': 'required'
		}
    }
