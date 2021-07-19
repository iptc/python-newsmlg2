#!/usr/bin/env python

"""
Handle NewsItems - one of the core NewsML-G2 Item types
"""

from .anyitem import (
    AnyItem, Assert, DerivedFrom, DerivedFromValue, InlineRef
)
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, NewsContentAttributes,
    NewsContentCharacteristics, NewsContentTypeAttributes,
    TimeValidityAttributes
)
from .contentmeta import ContentMetadataAfDType
from .extensionproperties import Flex2ExtPropType
from .itemmanagement import Signal
from .link import TargetResourceAttributes
from .ids import AltId, Hash
from .partmeta import PartMeta
from .simpletypes import IRIType


class InlineXML(NewsContentAttributes, NewsContentTypeAttributes,
        NewsContentCharacteristics, I18NAttributes):
    """
    A rendition of the content using an XML language
    """


class InlineData(NewsContentAttributes, NewsContentTypeAttributes,
        NewsContentCharacteristics, I18NAttributes):
    """
    A rendition of the content using plain-text or encoded inline data
    """
    xml_element_name = 'inlineData'
    attributes = {
        # The encoding applied to the content before inclusion - expressed by a QCode
        'encoding': {
            'xml_name': 'encoding',
            'xml_type': 'QCodeType',
        },
        # The encoding applied to the content before inclusion - expressed by a URI
        'encodinguri': {
            'xml_name': 'encodinguri'  # " type="IRIType',
        },
    }


class Channel(CommonPowerAttributes, NewsContentCharacteristics):
    """
    Information about a specific content channel.
    """
    attributes = {
        # A logical identifier of the channel
        'chnlid': {
            'xml_name': 'chnlid',
            'xml_type': 'xs:positiveInteger',
        },
        # The media type of the data conveyed by the channel - expressed by
        # a QCode
        'type': {
            'xml_name': 'type',
            'xml_type': 'QCodeType',
        },
        # The media type of the data conveyed by the channel - expressed by
        # a URI
        'typeuri': {
            'xml_name': 'typeuri',
            'xml_type': 'IRIType',
        },
        # The role the data of this channel plays in the scope of the full
        # content - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeType',
        },
        # The role the data of this channel plays in the scope of the full
        # content - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIType',
        },
        # The  language associated with the content of the channel
        'language': {
            'xml_name': 'language',
            'xml_type': 'xs:language',
        },
        # DO NOT USE this attribute, for G2 internal maintenance purposes only.
        'g2flag': {
            'xml_name': 'g2flag',
            'xml_type': 'xs:string',
            'use': 'optional',
            'fixed': 'RCONT'  # TODO handle this?
        }
    }


class AltLoc(IRIType, CommonPowerAttributes):
    """
    An alternative location of the content.
    """
    attributes = {
        # A qualifier which indicates the context within which the alternative
        # locator has been allocated - expressed by a QCode
        'type': {
            'xml_name': 'type',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # A qualifier which indicates the context within which the alternative
        # locator has been allocated - expressed by a URI
        'typeuri': {
            'xml_name': 'typeuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # A refinement of the semantics or business purpose of the property -
        # expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # A refinement of the semantics or business purpose of the property -
        # expressed by a URI
        'roleruri': {
            'xml_name': 'roleruri',
            'xml_type': 'IRIType',
            'use': 'optional'
        }
    }


class RemoteContentExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """

class RemoteContentPropType(NewsContentAttributes, TargetResourceAttributes,
    TimeValidityAttributes, NewsContentCharacteristics):
    """
    A type representing the structure of the remoteContent property
    """
    elements = [
        ('channel', {
            'type': 'array', 'xml_name': 'channel', 'element_class': Channel
        }),
        ('altid', {
            'type': 'array', 'xml_name': 'altId', 'element_class': AltId
        }),
        ('altloc', {
            'type': 'array', 'xml_name': 'altLoc', 'element_class': AltLoc
        }),
        ('hash', {
            'type': 'array', 'xml_name': 'hash', 'element_class': Hash
        }),
        ('signal', {
            'type': 'array', 'xml_name': 'signal', 'element_class': Signal
        }),
        ('remotecontentextproperty', {
            'type': 'array', 'xml_name': 'remoteContentExtProperty',
            'element_class': RemoteContentExtProperty
        })
    ]
    attributes = {
        # The language of the remote content
        'language': {
            'xml_name': 'language',
            'xml_type': 'xs:language'
        }
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
        # A local reference to the original piece of content, from which all
        # renditions have been derived
        'original': {
            'xml_name': 'original',
            'xml_type': 'xs:IDREF'
        }
    }

    elements = [
        ('inlinexml', {
            'type': 'array', 'xml_name': 'inlineXML',
            'element_class': InlineXML
        }),
        ('inlinedata', {
            'type': 'array', 'xml_name': 'inlineData',
            'element_class': InlineData
        }),
        ('remotecontent', {
            'type': 'array', 'xml_name': 'remoteContent',
            'element_class': RemoteContent
        })
    ]


class NewsItemContentMeta(ContentMetadataAfDType):
    """
    A set of properties about the content
    """
    xml_element_name = 'contentMeta'


class NewsItem(AnyItem):
    """
    An Item containing news-related information
    """

    elements = [
        ('contentmeta', {
            'type': 'single', 'xml_name': 'contentMeta',
            'element_class': NewsItemContentMeta
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
        ('contentset', {
            'type': 'single', 'xml_name': 'contentSet',
            'element_class': ContentSet
        })
    ]
