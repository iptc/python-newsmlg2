#!/usr/bin/env python

"""
AnyItemType definitions
"""

from lxml import etree

from .core import XML, NEWSMLG2, BaseObject, GenericArray
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, TimeValidityAttributes
)
from .catalog import CatalogMixin
from .complextypes import DateTimeOrNullPropType, DateTimePropType
from .rights import RightsBlockType, RightsInfo
from .propertytypes import QualPropType, QualRelPropType
from .conceptgroups import FlexPartyPropType, Flex2ExtPropType

DEBUG = True


class Party(FlexPartyPropType):
    """
    A party involved this hop of  the Hop History
    """

class Hop(CommonPowerAttributes):
    """
    A single hop of the Hop History. The details of the hop entry should
    reflect the actions taken by a party.
    """
    elements = {
        'party': { 'type': 'array', 'element_class': Party }
        # TODO more: see XML below...
    }
    """
<xs:element name="action" minOccurs="0" maxOccurs="unbounded">
<xs:annotation>
   <xs:documentation>An action which is executed at this hop in the hop history.</xs:documentation>
</xs:annotation>
<xs:complexType>
   <xs:complexContent>
      <xs:extension base="QualRelPropType">
         <xs:attribute name="target" type="QCodeType">
            <xs:annotation>
               <xs:documentation>The target of the action in a content object - expressed by a QCode. If the target attribute is omitted the target of the action is the whole object.</xs:documentation>
            </xs:annotation>
         </xs:attribute>
         <xs:attribute name="targeturi" type="IRIType">
            <xs:annotation>
               <xs:documentation>The target of the action in a content object - expressed by a URI. If the target attribute is omitted the target of the action is the whole object.</xs:documentation>
            </xs:annotation>
         </xs:attribute>
         <xs:attribute name="timestamp" type="DateOptTimeType">
            <xs:annotation>
               <xs:documentation>The date and optionally the time (with a time zone) when this action was performed on the target.</xs:documentation>
            </xs:annotation>
         </xs:attribute>
      </xs:extension>
   </xs:complexContent>
</xs:complexType>
    """
    attributes = {
        # The sequential value of this Hop in a sequence of Hops of a Hop History.
        # Values need not to be consecutive. The sequence starts with the lowest value.
        'seq': 'seq', # type="xs:nonNegativeInteger">
        # The date and optionally the time (with a time zone) when this item's
        # content object was forwarded.
        'timestamp': 'timestamp', # type="DateOptTimeType">
    }


class HopHistory(CommonPowerAttributes, GenericArray):
    """
    A history of the creation and modifications of the content object of this item, expressed as a sequence of hops.
    """
    element_class = Hop


class Published(BaseObject):
    pass


class PubHistory(GenericArray):
    element_class = Published



class ItemClass(QualRelPropType):
    """
    The nature of the item, set in accordance with the structure of its content.
    """


class Provider(FlexPartyPropType):
    """
    The party (person or organisation) responsible for the management of the Item.
    """


class VersionCreated(DateTimePropType):
    """
    The date and time on which the current version of the Item was created.
    """


class FirstCreated(DateTimePropType):
    """
    The date and time on which the first version of the Item was created.
    """


class Embargoed(DateTimeOrNullPropType):
    """
    The date and time on which the first version of the Item was created.
    """


class PubStatus(QualPropType):
    """
    The publishing status of the Item, its value is "usable" by default.
    """

class Role(QualPropType):
    """
    The role of the Item in the editorial workflow.
    """

class ServiceElement(QualPropType):
    """
    An editorial service to which an item is assigned by its provider.
    """

class Service(GenericArray):
    element_class = ServiceElement


class ItemMeta(BaseObject):
    """
    A set of properties directly associated with the Item
    """

    single_elements = {
        'itemClass': ItemClass,
        'provider': Provider,
        'versionCreated': VersionCreated,
        'firstCreated': FirstCreated,
        'embargoed': Embargoed,
        'pubStatus': PubStatus,
    }
    array_elements = {
        'service': Service
    }
    def __init__(self,  **kwargs):
        super(ItemMeta, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            # assert self.itemclass is not None, "itemClass is required in any NewsML-G2 Item"
            # assert self.provider is not None, "provider is required in any NewsML-G2 Item"
            # assert self.versioncreated is not None, "versionCreated is required in any NewsML-G2 Item"
            pass

    def get_itemclass(self):
        return self.get_single_element_value('itemClass').get_qcode()

    def get_itemclass_uri(self):
        return self.get_single_element_value('itemClass').get_uri()

    def get_provider(self):
        return self.get_single_element_value('provider').get_qcode()

    def get_provider_uri(self):
        return self.get_single_element_value('provider').get_uri()

    def get_versioncreated(self):
        return str(self.get_single_element_value('versionCreated'))

    def get_firstcreated(self):
        return str(self.get_single_element_value('firstCreated'))

    def get_embargoed(self):
        return str(self.get_single_element_value('embargoed'))

    def get_pubstatus(self):
        return self.get_single_element_value('pubStatus').get_qcode()

    def get_pubstatus_uri(self):
        return self.get_single_element_value('pubStatus').get_uri()

    def get_services(self):
        return self.get_array_element_value('service')

    def get_service(self):
        return self.get_array_element_value('service')[0].get_qcode()

    def get_service_uri(self):
        return self.get_array_element_value('service')[0].get_uri()

    """
         <xs:element ref="role" minOccurs="0"/>
         <xs:element ref="fileName" minOccurs="0"/>
         <xs:element ref="generator" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="profile" minOccurs="0"/>
         <xs:element ref="service" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="title" minOccurs="0" maxOccurs="unbounded">
            <xs:annotation>
               <xs:documentation>A short natural language name for the Item.</xs:documentation>
            </xs:annotation>
         </xs:element>
         <xs:element ref="edNote" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="memberOf" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="instanceOf" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="signal" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="altRep" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="deliverableOf" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="hash" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="expires" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="origRep" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="incomingFeedId" minOccurs="0" maxOccurs="unbounded"/>
         <xs:element ref="metadataCreator" minOccurs="0"/>
    """


class ItemMetaExtProperty(Flex2ExtPropType):
    """
    Extension Property: the semantics are defined by the concept referenced by
    the rel attribute.
    The semantics of the Extension Property must have the same scope as the
    parent property.
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
        'version': 'version', # TODO type positive integer, default "1"
        # TODO: should be in a separate class "i18nattributes"
        # Specifies the language of this property and potentially all descendant
        # properties. xml:lang values of descendant properties override this
        # value. Values are determined by Internet BCP 47.
        XML+'lang': 'xml:lang',
        # The directionality of textual content (enumeration: ltr, rtl)
        'dir': 'dir'
    }

    single_elements = {
        'itemMeta': ItemMeta
    }
    array_elements = {
        'hopHistory': HopHistory,
        'pubHistory': PubHistory,
        'rightsInfo': RightsInfo
    }
    def __init__(self,  **kwargs):
        super(AnyItem, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            self.build_catalog(xmlelement)
            #self.hopHistory = HopHistory(
            #    xmlarray = xmlelement.findall(NEWSMLG2+'hopHistory')
            #)
            #self.pubHistory = PubHistory(
            #    xmlarray = xmlelement.findall(NEWSMLG2+'pubHistory')
            #)
            #self.rightsInfoArray = RightsInfo(
            #    xmlarray = xmlelement.findall(NEWSMLG2+'rightsInfo')
            #)
            #self.itemMeta = ItemMeta(
            #    xmlelement = xmlelement.find(NEWSMLG2+'itemMeta')
            #)
            # assert self.itemMeta is not None, "itemMeta is required in any NewsML-G2 Item"

    def get_itemmeta(self):
        return self.get_single_element_value('itemMeta')

    def get_rightsinfo(self):
        return self.get_array_element_value('rightsInfo')


