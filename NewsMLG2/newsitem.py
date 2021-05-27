#!/usr/bin/env python

import json
from lxml import etree
import os

from .core import NSMAP, NEWSMLG2, BaseObject, GenericArray
from .anyitem import AnyItem
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes,
    NewsContentCharacteristics, NewsContentTypeAttributes,
    TimeValidityAttributes
)
from .link import TargetResourceAttributes
from .ids import AltId, Hash

DEBUG = True


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


class InlineXMLElement(NewsContentAttributes, NewsContentTypeAttributes,
        NewsContentCharacteristics, I18NAttributes):
    """
    A rendition of the content using an XML language
    """

class InlineXML(GenericArray):
    """
    An array of InlineXMLElement objects
    """
    element_class = InlineXMLElement


class InlineDataElement(NewsContentAttributes, NewsContentTypeAttributes,
        NewsContentCharacteristics, I18NAttributes):
    """
    A rendition of the content using plain-text or encoded inline data
    """
    attributes = {
        # The encoding applied to the content before inclusion - expressed by a QCode
        'encoding': 'encoding',  # " type="QCodeType">
        # The encoding applied to the content before inclusion - expressed by a URI
        'encodinguri': 'encodinguri'  # " type="IRIType">
    }

class InlineData(GenericArray):
    """
    An array of InlineDataElement objects
    """
    element_class = InlineDataElement


class ChannelElement(CommonPowerAttributes):
    """
    Information about a specific content channel.
    """
    attributes = {
        # A logical identifier of the channel
        'chnlid': 'chnlid',  # type="xs:positiveInteger">
        # The media type of the data conveyed by the channel - expressed by a QCode
        'type': 'type',  # " type="QCodeType">
        # The media type of the data conveyed by the channel - expressed by a URI
        'typeuri': 'typeuri',  # " type="IRIType">
        # The role the data of this channel plays in the scope of  the full content - expressed by a QCode
        'role': 'role',  # " type="QCodeType">
        # The role the data of this channel plays in the scope of  the full content - expressed by a URI
        'roleuri': 'roleuri',  # " type="IRIType">
        # The  language associated with the content of the channel
        'language': 'language',  # " type="xs:language">
        # DO NOT USE this attribute, for G2 internal maintenance purposes only.
        'g2flag': 'g2flag'  # " type="xs:string" use="optional" fixed="RCONT">
    }
    
class Channel(GenericArray):
    """
    An array of ChannelElement objects
    """
    element_class = ChannelElement

class RemoteContentPropType(NewsContentAttributes, TargetResourceAttributes,
    TimeValidityAttributes, NewsContentCharacteristics):
    """
    A type representing the structure of the remoteContent property
    """
    elements = {
        'channel': { 'type': 'array', 'xml_name': 'inlineXML', 'element_class': Channel },
        'altid': { 'type': 'array', 'xml_name': 'altId', 'element_class': AltId },
        'hash': { 'type': 'array', 'xml_name': 'hash', 'element_class': Hash },
        # TODO    
        #'signal': { 'type': 'array', 'xml_name': 'signal', 'element_class': Signal },
        #'remote_content_ext_property': { 'type': 'array', 'xml_name': 'remoteContentExtProperty', 'element_class': RemoteContentExtProperty },
    }
    attributes = {
        # The language of the remote content
        'language': 'language'  # type="xs:language">
    }

class RemoteContent(RemoteContentPropType):
    """
    A rendition of the content using a reference/link to a resource representing
    the content data at a remote location
    """

class ContentSet(CommonPowerAttributes):
    """
    A set of alternate renditions of the Item content
    """

    attributes = {
        # A local reference to the original piece of content, from which all renditions have been derived
        'original': 'original'  # TODO type="xs:IDREF"
    }

    elements = {
        'inlinexml': { 'type': 'array', 'xml_name': 'inlineXML', 'element_class': InlineXML },
        'inlinedata': { 'type': 'array', 'xml_name': 'inlineData', 'element_class': InlineData },
        'remotecontent': { 'type': 'array', 'xml_name': 'remoteContent', 'element_class': RemoteContent }
    }

    def get_inlinexml(self):
        return self.get_element_value('inlinexml')
 

class NewsItem(AnyItem):
    """
    An Item containing news-related information
    """

    elements = {
        # TODO - implement these classes!
        #'contentmeta': { 'type': 'single', 'xml_name': 'contentMeta', 'element_class': ContentMeta },
        #'partmeta': { 'type': 'array', 'xml_name': 'partMeta', 'element_class': PartMeta },
        #'assert': { 'type': 'array', 'xml_name': 'assert', 'element_class': Assert },
        #'inlineref': { 'type': 'array', 'xml_name': 'inlineRef', 'element_class': InlineRef },
        #'derivedfrom': { 'type': 'array', 'xml_name': 'derivedFrom', 'element_class': DerivedFrom },
        #'derivedfromvalue': { 'type': 'array', 'xml_name': 'derivedFromValue', 'element_class': DerivedFromValue },
        'contentset': { 'type': 'single', 'xml_name': 'contentSet', 'element_class': ContentSet }
    }

    def get_contentset(self):
        return self.get_element_value('contentset')

    def to_xml(self):
        xmlelem = etree.Element(NEWSMLG2+'newsItem', nsmap=NSMAP)
        return xmlelem



