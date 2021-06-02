#!/usr/bin/env python

"""
AnyItemType definitions
"""

from lxml import etree

from .core import GenericArray, QCodeURIMixin
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes
)
from .catalog import CatalogMixin
from .complextypes import Name, TruncatedDateTimePropType
from .conceptgroups import FlexPartyPropType, Flex2ExtPropType
from .conceptrelationships import QualRelPropType, Related
from .itemmanagement import ItemManagementGroup
from .link import Link
from .rights import RightsInfo

DEBUG = True


class Party(FlexPartyPropType):
    """
    A party involved this hop of  the Hop History
    """

class ActionElement(QualRelPropType):
    """
    An action which is executed at this hop in the hop history.
    """
    attributes = {
        # The target of the action in a content object - expressed by a QCode.
        # If the target attribute is omitted the target of the action is the
        # whole object.
        'target': 'target',  # type="QCodeType">
        # The target of the action in a content object - expressed by a URI.
        # If the target attribute is omitted the target of the action is the
        # whole object.
        'targeturi': 'targeturi',  # type="IRIType">
        # The date and optionally the time (with a time zone) when this action
        # was performed on the target.
        'timestamp': 'timestamp',  # type="DateOptTimeType">
    }


class Action(GenericArray):
    """
    An array of ActionElement objects.
    """
    element_class = ActionElement


class Hop(CommonPowerAttributes):
    """
    A single hop of the Hop History. The details of the hop entry should
    reflect the actions taken by a party.
    """
    elements = {
        'party': {
            'type': 'array', 'xml_name': 'party', 'element_class': Party
        },
        'action': {
            'type': 'array',
            'xml_name': 'action',
            'element_class': Action
        }
    }
    attributes = {
        # The sequential value of this Hop in a sequence of Hops of a Hop
        # History.
        # Values need not to be consecutive. The sequence starts with the lowest
        # value.
        'seq': 'seq', # type="xs:nonNegativeInteger">
        # The date and optionally the time (with a time zone) when this item's
        # content object was forwarded.
        'timestamp': 'timestamp', # type="DateOptTimeType">
    }


class HopHistory(CommonPowerAttributes, GenericArray):
    """
    A history of the creation and modifications of the content object of this
    item, expressed as a sequence of hops.
    """
    element_class = Hop


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
    elements = {
        'timestamp': {
            'type': 'single',
            'xml_name': 'timestamp',
            'element_class': Timestamp
        },
        'name': { 'type': 'array', 'xml_name': 'name', 'element_class': Name },
        'related': {
            'type': 'array', 'xml_name': 'related', 'element_class': Related
        },
        'publishedExtProperty': {
            'type': 'array',
            'xml_name': 'publishedExtProperty',
            'element_class': PublishedExtProperty
        },
    }
    attributes = {
        # A free-text value assigned as property value.
        'literal': 'literal'  # type="g2normalizedString">
    }


class PubHistory(GenericArray):
    """
    One to many datasets about publishing this item.
    """
    element_class = Published


class ItemMetaExtPropertyElement(Flex2ExtPropType):
    """
    Extension Property: the semantics are defined by the concept referenced by
    the rel attribute.
    The semantics of the Extension Property must have the same scope as the
    parent property.
    """


class ItemMetaExtProperty(GenericArray):
    """
    An array of ItemMetaExtPropertyElement objects.
    """
    element_class = ItemMetaExtPropertyElement


class ItemMetadataType(ItemManagementGroup, CommonPowerAttributes,
    I18NAttributes):
    """
    The type for a set of properties directly associated with the item
    (Type defined in this XML Schema only)
    """
    elements = {
        'link': { 'type': 'array', 'xml_name': 'link', 'element_class': Link },
        'itemmetaextproperty': {
            'type': 'array',
            'xml_name': 'itemMetaExtProperty',
            'element_class': ItemMetaExtProperty
        }
    }


class ItemMeta(ItemMetadataType):
    """
    A set of properties directly associated with the Item
    """


class AnyItem(CatalogMixin, I18NAttributes):
    """
    An abstract class. All G2 items are inherited from this class.
    """

    attributes = {
        # The IPTC standard with which the Item is conformant.
        'standard': 'standard',
        # The major-minor version of the IPTC standard with which the Item is conformant.
        'standardversion': 'standardversion',
        # The conformance level with which the Item is conformant.
        'conformance': 'conformance', # TODO default "core"
        # The persistent, universally unique identifier common for all versions of the Item.
        'guid': 'guid', # TODO enforce requiredness
        # The version of the Item.
        'version': 'version'  # TODO type positive integer, default "1"
    }

    elements = {
        'hophistory': { 'type': 'array', 'xml_name': 'hopHistory', 'element_class': HopHistory },
        'pubhistory': { 'type': 'array', 'xml_name': 'pubHistory', 'element_class': PubHistory },
        'rightsinfo': { 'type': 'array', 'xml_name': 'rightsInfo', 'element_class': RightsInfo },
        'itemmeta': { 'type': 'single', 'xml_name': 'itemMeta', 'element_class': ItemMeta }
    }

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            self.build_catalog(xmlelement)
            assert self.itemmeta is not None, "itemMeta is required in any NewsML-G2 Item"
