#!/usr/bin/env python

"""
Handle NewsItems - one of the core NewsML-G2 Item types
"""

from .core import GenericArray
from .anyitem import AnyItem
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, NewsContentAttributes,
    NewsContentCharacteristics, NewsContentTypeAttributes,
    TimeValidityAttributes
)
from .contentmeta import ContentMetadataAfDType
from .itemmanagement import Signal
from .link import TargetResourceAttributes
from .ids import AltId, Hash


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
    xml_element_name = 'inlineData'
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


class ChannelElement(CommonPowerAttributes, NewsContentCharacteristics):
    """
    Information about a specific content channel.
    """
    attributes = {
        # A logical identifier of the channel
        'chnlid': 'chnlid',  # type="xs:positiveInteger">
        # The media type of the data conveyed by the channel - expressed by
        # a QCode
        'type': 'type',  # " type="QCodeType">
        # The media type of the data conveyed by the channel - expressed by
        # a URI
        'typeuri': 'typeuri',  # " type="IRIType">
        # The role the data of this channel plays in the scope of the full
        # content - expressed by a QCode
        'role': 'role',  # " type="QCodeType">
        # The role the data of this channel plays in the scope of the full
        # content - expressed by a URI
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
        'channel': {
            'type': 'array', 'xml_name': 'channel', 'element_class': Channel
        },
        'altid': {
            'type': 'array', 'xml_name': 'altId', 'element_class': AltId
        },
        # TODO
        # 'altloc': {
        #    'type': 'array', 'xml_name': 'altLoc', 'element_class': AltLoc
        #},
        'hash': {
            'type': 'array', 'xml_name': 'hash', 'element_class': Hash
        },
        'signal': {
            'type': 'array', 'xml_name': 'signal', 'element_class': Signal
        #},
        # TODO
        # 'remotecontentextproperty': {
        #    'type': 'array', 'xml_name': 'remoteContentExtProperty',
        #    'element_class': RemoteContentExtProperty
        }
    }
    attributes = {
        # The language of the remote content
        'language': 'language'  # type="xs:language">
    }


class RemoteContentElement(RemoteContentPropType):
    """
    A rendition of the content using a reference/link to a resource representing
    the content data at a remote location
    """


class RemoteContent(RemoteContentPropType):
    """
    An array of RemoteContentElement objects.
    """
    element_class = RemoteContentElement


class ContentSet(CommonPowerAttributes):
    """
    A set of alternate renditions of the Item content
    """

    attributes = {
        # A local reference to the original piece of content, from which all
        # renditions have been derived
        'original': 'original'  # type="xs:IDREF"
    }

    elements = {
        'inlinexml': {
            'type': 'array', 'xml_name': 'inlineXML',
            'element_class': InlineXML
        },
        'inlinedata': {
            'type': 'array', 'xml_name': 'inlineData',
            'element_class': InlineData
        },
        'remotecontent': {
            'type': 'array', 'xml_name': 'remoteContent',
            'element_class': RemoteContent
        }
    }


class NewsItemContentMeta(ContentMetadataAfDType):
    """
    A set of properties about the content
    """
    xml_element_name = 'contentMeta'


class NewsItem(AnyItem):
    """
    An Item containing news-related information
    """

    elements = {
        'contentmeta': {
            'type': 'single', 'xml_name': 'contentMeta',
            'element_class': NewsItemContentMeta
        },
        # TODO - implement these classes!
        #'partmeta': {
        #    'type': 'array', 'xml_name': 'partMeta', 'element_class': PartMeta
        #},
        #'assert': {
        #    'type': 'array', 'xml_name': 'assert', 'element_class': Assert
        #},
        #'inlineref': {
        #    'type': 'array', 'xml_name': 'inlineRef', 'element_class': InlineRef
        #},
        #'derivedfrom': {
        #    'type': 'array', 'xml_name': 'derivedFrom', 'element_class': DerivedFrom
        #},
        #'derivedfromvalue': {
        #    'type': 'array', 'xml_name': 'derivedFromValue',
        #    'element_class': DerivedFromValue
        #},
        'contentset': {
            'type': 'single', 'xml_name': 'contentSet',
            'element_class': ContentSet
        }
    }
