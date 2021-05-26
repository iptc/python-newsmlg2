#!/usr/bin/env python

import json
from lxml import etree
import os

from .core import NSMAP, NEWSMLG2, BaseObject
from .anyitem import AnyItem
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes,
    NewsContentCharacteristics, NewsContentTypeAttributes
)

DEBUG = True

class NewsItem(AnyItem):
    """
    An Item containing news-related information
    """

    def __init__(self,  **kwargs):
        super(NewsItem, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            #self.contentMeta = ContentMeta(
            #    xmlelement = xmlelement.find(NEWSMLG2+'contentMeta')
            #)
            #self.partMeta = PartMetaList(
            #    xmlarray = xmlelement.findall(NEWSMLG2+'partMeta')
            #)
            #self.assertList = AssertList(
            #    xmlarray = xmlelement.findall(NEWSMLG2+'assert')
            #)
            #self.inlineRefList = InlineRefList(
            #    xmlarray = xmlelement.findall(NEWSMLG2+'inlineRef')
            #)
            #self.derivedFromList = DerivedFromList(
            #    xmlarray = xmlelement.findall(NEWSMLG2+'derivedFrom')
            #)
            #self.derivedFromValueList = DerivedFromValueList(
            #    xmlarray = xmlelement.findall(NEWSMLG2+'derivedFromValue')
            #)
            self.contentSet = ContentSet(
                xmlelement = xmlelement.find(NEWSMLG2+'contentSet')
            )

    def to_xml(self):
        xmlelem = etree.Element(NEWSMLG2+'newsItem', nsmap=NSMAP)
        return xmlelem


class ContentSet(CommonPowerAttributes):
    """
    A set of alternate renditions of the Item content

            <xs:element name="inlineData">
               <xs:annotation>
               A rendition of the content using plain-text or encoded inline data
               </xs:annotation>
               <xs:complexType>
                  <xs:simpleContent>
                     <xs:extension base="xs:string">
                        <xs:attributeGroup ref="newsContentAttributes"/>
                        <xs:attributeGroup ref="newsContentTypeAttributes"/>
                          'encoding': '', # type="QCodeType">
                           <xs:annotation>
                           The encoding applied to the content before inclusion - expressed by a QCode
                           </xs:annotation>
                        </xs:attribute>
                          'encodinguri': '', # type="IRIType">
                           <xs:annotation>
                           The encoding applied to the content before inclusion - expressed by a URI
                           </xs:annotation>
                        </xs:attribute>
                        <xs:attributeGroup ref="newsContentCharacteristics"/>
                        <xs:attributeGroup ref="i18nAttributes"/>
                        <xs:anyAttribute namespace="##other" processContents="lax"/>
                     </xs:extension>
                  </xs:simpleContent>
               </xs:complexType>
            </xs:element>

            <xs:element name="remoteContent': '', # type="RemoteContentPropType">
               <xs:annotation>
               A rendition of the content using a reference/link to a resource representing the content data at a remote location
               </xs:annotation>
            </xs:element>
         </xs:choice>

         <xs:attributeGroup ref="commonPowerAttributes"/>

           'original': '', # type="xs:IDREF">
            <xs:annotation>
            A local reference to the original piece of content, from which all renditions have been derived
            </xs:annotation>
         </xs:attribute>
         <xs:anyAttribute namespace="##other" processContents="lax"/>
      </xs:complexType>
    """

    attributes = {
        # A local reference to the original piece of content, from which all renditions have been derived
        # TODO type="xs:IDREF"
        'original': 'original'
    }

    def __init__(self,  **kwargs):
        super(ContentSet, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.inlineXML = InlineXML(
                xmlelement = xmlelement.find(NEWSMLG2+'inlineXML')
            )
 

class NewsContentAttributes(BaseObject):
    """
    A group of typical attributes associated with a content rendition
    """
    attributes = {
        # The local identifier of the element which MUST be persistent for all
        # versions of the item, i.e. for its entire lifecycle.
        'id': 'id', # type="xs:ID"
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a QCode.
        # If the attribute is non-empty, specifies which entity (person,
        # organisation or system) has edited the property.
        'creator': 'creator', # type="QCodeType"
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a URI.
        # If the attribute is non-empty, specifies which entity (person,
        # organisation or system) has edited the property.
        'creatoruri': 'creatoruri', # type="IRIType"
        # The date (and, optionally, the time) when the property was last
        # modified. The initial value is the date (and, optionally, the time) of
        # creation of the property.
        'modified': 'modified', # type="DateOptTimeType"
        # If set to true the corresponding property was added to the G2 Item for
        # a specific customer or group of customers only. The default value of
        # this property is false which applies when this attribute is not used
        # with the property.
        'custom': 'custom', # type="xs:boolean"
        # Indicates by which means the value was extracted from the content -
        # expressed by a QCode
        'how': 'how', # type="QCodeType"
        # Indicates by which means the value was extracted from the content -
        # expressed by a URI
        'howuri': 'howuri', # type="IRIType"
        # Why the metadata has been included - expressed by a QCode
        'why': 'why', # type="QCodeType"
        # Why the metadata has been included - expressed by a URI
        'whyuri': 'whyuri', # type="IRIType"
        # The specific rendition of content this component represents -
        # expressed by a QCode
        'rendition': 'rendition', # type="QCodeType"
        # The specific rendition of content this component represents -
        # expressed by a URI
        'renditionuri': 'renditionuri', # type="IRIType"
        # The name and version of the software tool used to generate the content
        'generator': 'generator', # type="xs:string"
        # The date (and, optionally, the time) when the content was generated
        'generated': 'generated', # type="DateOptTimeType"
        # Indicates if the digital data of this rendition is available or not.
        'hascontent': 'hascontent' # type="xs:boolean"
    }


class InlineXML(NewsContentAttributes, NewsContentTypeAttributes,
        NewsContentCharacteristics, I18NAttributes):
    """
    A rendition of the content using an XML language
    """
    def __init__(self,  **kwargs):
        super(InlineXML, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            pass
