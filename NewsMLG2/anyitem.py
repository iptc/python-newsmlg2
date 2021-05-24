#!/usr/bin/env python

"""
AnyItemType definitions
"""

import json
import os
from lxml import etree

from .core import XML, NEWSMLG2, BaseObject, GenericArray
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, TimeValidityAttributes
)
from .catalog import CatalogMixin
from .complextypes import *
# from .complextypes import DateTimeOrNullPropType, DateTimePropType
from .newsmlg2 import RightsBlockType
from .propertytypes import QualPropType, QualRelPropType
from .conceptgroups import FlexPartyPropType

DEBUG = True

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

    def __init__(self,  **kwargs):
        super(AnyItem, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.buildCatalog(xmlelement)
            self.hopHistory = HopHistory(
                xmlarray = xmlelement.findall(NEWSMLG2+'hopHistory')
            )
            self.pubHistory = PubHistory(
                xmlarray = xmlelement.findall(NEWSMLG2+'pubHistory')
            )
            self.rightsInfoArray = RightsInfoArray(
                xmlarray = xmlelement.findall(NEWSMLG2+'rightsInfo')
            )
            self.itemMeta = ItemMeta(
                xmlelement = xmlelement.find(NEWSMLG2+'itemMeta')
            )
            assert self.itemMeta is not None, "itemMeta is required in any NewsML-G2 Item"


class Party(FlexPartyPropType):
    """
    A party involved this hop of  the Hop History
    """
    pass

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
    pass


class HopHistory(CommonPowerAttributes, GenericArray):
    """
    A history of the creation and modifications of the content object of this item, expressed as a sequence of hops.
    """
    element_class = Hop


class Published(BaseObject):
    pass


class PubHistory(GenericArray):
    element_class = Published

class Accountable(BaseObject):
    # TODO
    pass

class CopyrightHolder(FlexPartyPropType):
    """
    The person or organisation claiming the intellectual property for the content.
    """
    pass

class CopyrightNotice(RightsBlockType):
    """
    Any necessary copyright notice for claiming the intellectual property for the content.
    """
    pass

class CopyrightNoticeArray(GenericArray):
    element_class = CopyrightNotice

class UsageTerms(RightsBlockType):
    """
    A natural-language statement about the usage terms pertaining to the content.
    """
    pass

class UsageTermsArray(GenericArray):
    element_class = UsageTerms

class Link(BaseObject):
    # TODO
    pass

class LinkArray(GenericArray):
    element_class = Link

class RightsInfoExtProperty(BaseObject):
    # TODO
    pass

class RightsInfoExtPropertyArray(GenericArray):
    element_class = RightsInfoExtProperty

class RightsExpressionXML(BaseObject):
    # TODO
    pass

class RightsExpressionXMLArray(GenericArray):
    element_class = RightsExpressionXML
     
class RightsExpressionData(BaseObject):
    # TODO
    pass

class RightsExpressionDataArray(GenericArray):
    element_class = RightsExpressionData


class RightsInfo(CommonPowerAttributes, I18NAttributes, TimeValidityAttributes):
    """
    A set of properties representing the rights associated with the Item
    """
    attributes = {
        # Reference(s) to the part(s) of an Item to which the rightsInfo element applies. When referencing part(s) of the content of an Item, idrefs must include the partid value of a partMeta element which in turn references the part of the content.
        'idrefs': 'idrefs', # type="xs:IDREFS"
        # Indicates to which part(s) of an Item the rightsInfo element applies - expressed by a QCode. If the attribute does not exist then rightsInfo applies to all parts of the Item. Mandatory NewsCodes scheme for the values: http://cv.iptc.org/newscodes/riscope/
        'scope': 'scope', # type="QCodeListType" use="optional">
        # Indicates to which part(s) of an Item the rightsInfo element applies - expressed by a URI. If the attribute does not exist then rightsInfo applies to all parts of the Item. Mandatory NewsCodes scheme for the values: http://cv.iptc.org/newscodes/riscope/</xs:documentation>
        'scopeuri': 'scopeuri', # type="IRIListType" use="optional">
        # Indicates to which rights-related aspect(s) of an Item or part(s) of an Item the rightsInfo element applies - expressed by a QCode. If the attribute does not exist then rightsInfo applies to all aspects. Mandatory NewsCodes scheme for the values: http://cv.iptc.org/newscodes/riaspect</xs:documentation>
        'aspect': 'aspect', # type="QCodeListType" use="optional">
        # Indicates to which rights-related aspect(s) of an Item or part(s) of an Item the rightsInfo element applies - expressed by a URI. If the attribute does not exist then rightsInfo applies to all aspects. Mandatory NewsCodes scheme for the values: http://cv.iptc.org/newscodes/riaspect</xs:documentation>
        'aspecturi': 'aspecturi' # type="IRIListType" use="optional">
    }

    def __init__(self,  **kwargs):
        super(RightsInfo, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.accountable = Accountable(
                xmlelement = xmlelement.find(NEWSMLG2+'accountable')
            )
            self.copyrightHolder = CopyrightHolder(
                xmlelement = xmlelement.find(NEWSMLG2+'copyrightHolder')
            )
            self.copyrightNoticeArray = CopyrightNoticeArray(
                xmlarray = xmlelement.findall(NEWSMLG2+'copyrightNotice')
            )
            self.usageTermsArray = UsageTermsArray(
                xmlarray = xmlelement.findall(NEWSMLG2+'usageTerms')
            )
            self.linkArray =LinkArray(
                xmlarray = xmlelement.findall(NEWSMLG2+'link')
            )
            self.rightsInfoExtPropertyArray = RightsInfoExtPropertyArray(
                xmlarray = xmlelement.findall(NEWSMLG2+'self.rightsInfoExtProperty')
            )
            self.rightsExpressionXMLArray = RightsExpressionXMLArray(
                xmlarray = xmlelement.findall(NEWSMLG2+'self.rightsExpressionXML')
            )
            self.rightsExpressionDataArray = RightsExpressionDataArray(
                xmlarray = xmlelement.findall(NEWSMLG2+'self.rightsExpressionData')
            )
 

class RightsInfoArray(GenericArray):
    element_class = RightsInfo


class ItemClass(QualRelPropType):
    """
    The nature of the item, set in accordance with the structure of its content.
    """
    pass


class Provider(FlexPartyPropType):
    """
    The party (person or organisation) responsible for the management of the Item.
    """
    pass


class VersionCreated(DateTimePropType):
    """
    The date and time on which the current version of the Item was created.
    """
    pass


class FirstCreated(DateTimePropType):
    """
    The date and time on which the first version of the Item was created.
    """
    pass


class Embargoed(DateTimeOrNullPropType):
    """
    The date and time on which the first version of the Item was created.
    """
    pass


class PubStatus(QualPropType):
    """
    The publishing status of the Item, its value is "usable" by default.
    """
    pass

class Role(QualPropType):
    """
    The role of the Item in the editorial workflow.
    """
    pass

class ServiceElement(QualPropType):
    """
    An editorial service to which an item is assigned by its provider.
    """
    pass

class Service(GenericArray):
    element_class = ServiceElement


class ItemMeta(BaseObject):
    """
    A set of properties directly associated with the Item
    """

    def __init__(self,  **kwargs):
        super(ItemMeta, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.itemClass = ItemClass(
                xmlelement = xmlelement.find(NEWSMLG2+'itemClass')
            )
            assert self.itemClass is not None, "itemClass is required in any NewsML-G2 Item"
            self.provider = Provider(
                xmlelement = xmlelement.find(NEWSMLG2+'provider')
            )
            assert self.provider is not None, "provider is required in any NewsML-G2 Item"
            self.versionCreated = VersionCreated(
                xmlelement = xmlelement.find(NEWSMLG2+'versionCreated')
            )
            assert self.versionCreated is not None, "versionCreated is required in any NewsML-G2 Item"
            self.firstCreated = FirstCreated(
                xmlelement = xmlelement.find(NEWSMLG2+'firstCreated')
            )
            self.embargoed = Embargoed(
                xmlelement = xmlelement.find(NEWSMLG2+'embargoed')
            )
            self.pubStatus = PubStatus(
                xmlelement = xmlelement.find(NEWSMLG2+'pubStatus')
            )
            self.service = Service(
                xmlarray = xmlelement.findall(NEWSMLG2+'service')
            )
    def getItemClass(self):
        return self.itemClass.getQcode()

    def getItemClassURI(self):
        return self.itemClass.getURI()

    def getProvider(self):
        return self.provider.getQcode()

    def getProviderURI(self):
        return self.provider.getURI()

    def getPubStatus(self):
        return self.pubStatus.getQcode()
    
    def getPubStatusURI(self):
        return self.pubStatus.getURI()

    def getService(self):
        return self.service[0].getQcode()

    def getServiceURI(self):
        return self.service[0].getURI()

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
