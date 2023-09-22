#!/usr/bin/env python

"""
Various attribute groups used throughout the schema.
"""

from .core import BaseObject, XMLNSPREFIX, QCodeURIMixin


class CommonPowerAttributes(BaseObject):
    """
    A group of attributes for all elements of a G2 Item except its root
    element, the itemMeta element and all of its children which are mandatory.
    """
    attributes = {
        # The local identifier of the property.
        'id': {
            'xml_name': 'id'
        },
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a
        # QCode. If the attribute is non-empty, specifies which entity
        # (person, organisation or system) has edited the property.
        'creator': {
            'xml_name': 'creator'
        },
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a
        # URI. If the attribute is non-empty, specifies which entity
        # (person, organisation or system) has edited the property.
        'creatoruri': {
            'xml_name': 'creatoruri'
        },
        # The date (and, optionally, the time) when the property was last
        # modified. The initial value is the date (and, optionally, the
        # time) of creation of the property.
        'modified': {
            'xml_name': 'modified'
        },
        # If set to true the corresponding property was added to the G2
        # Item for a specific customer or group of customers only. The
        # default value of this property is false which applies when this
        #  attribute is not used with the property.
        'custom': {
            'xml_name': 'custom'
        },
        # Indicates by which means the value was extracted from the
        # content - expressed by a QCode
        'how': {
            'xml_name': 'how'
        },
        # Indicates by which means the value was extracted from the
        # content - expressed by a URI
        'howuri': {
            'xml_name': 'howuri'
        },
        # Why the metadata has been included - expressed by a QCode
        'why': {
            'xml_name': 'why'
        },
        # Why the metadata has been included - expressed by a URI
        'whyuri': {
            'xml_name': 'whyuri'
        },
        # One or many constraints that apply to publishing the value of
        # the property - expressed by a QCode. Each constraint applies
        # to all descendant elements.
        'pubconstraint': {
            'xml_name': 'pubconstraint'
        },
        # One or many constraints that apply to publishing the value of
        # the property - expressed by a URI. Each constraint applies to
        # all descendant elements.
        'pubconstrainturi': {
            'xml_name': 'pubconstrainturi'
        }
    }

class I18NAttributes(BaseObject):
    """
    A group of attributes for language and script related information
    """
    attributes = {
        # Specifies the language of this property and potentially all
        # descendant properties. xml:lang values of descendant properties
        # override this value. Values are determined by Internet BCP 47.
        'xml_lang': {
            'xml_name': XMLNSPREFIX+'lang'
        },
        # The directionality of textual content
        # (TODO enumeration: ltr, rtl)
        'dir': {
            'xml_name': 'dir'
        }
    }


class AuthorityAttributes(BaseObject):
    """
    A group of attributes for defining the authority that manages/maintains
    a catalog or scheme

    Added in NewsML-G2 2.32
    """
    attributes = {
        # Defines the authority controlling this catalog
        'authority': {
            'xml_name': 'authority'
        },
        # The status of the Authority associated with the Scheme - expressed as a QCode.
        'authoritystatus': {
            'xml_name': 'authoritystatus',
            'xml_type': 'QCodeType'
        },
        # The status of the Authority associated with the Scheme - expressed as a URI.
        'authoritystatusuri': {
            'xml_name': 'authoritystatusuri',
            'xml_type': 'IRIType'
        }
    }


class QuantifyAttributes(BaseObject):
    """
    A group of attriubutes quantifying the property value
    """
    attributes = {
        # The confidence with which the metadata has been assigned.
        'confidence': {
            'xml_name': 'confidence',
            'xml_type': 'Int100Type',
            'use': 'optional'
        },
        # The relevance of the metadata to the news content to which it is
        # attached.
        'relevance': {
            'xml_name': 'relevance',
            'xml_type': 'Int100Type',
            'use': 'optional'
        },
        # A reference to the concept from which the concept identified by qcode
        # was derived/inferred - use DEPRECATED in NewsML-G2 2.12 and higher,
        # use the derivedFrom element
        'derivedfrom': {
            'xml_name': 'derivedfrom',
            'xml_type': 'QCodeListType',
            'use': 'optional'
        }
    }


class TimeValidityAttributes(BaseObject):
    """
    A group of attributes expressing the time period of validity of a relationship
    """
    attributes = {
        # The date (and, optionally, the time) before which a relationship is not valid.
        'validfrom': {
            'xml_name': 'validfrom',
            'xml_type': 'DateOptTimeType',
            'use': 'optional'
        },
        # The date (and, optionally, the time) after which a relationship is not valid.
        'validto': {
            'xml_name': 'validto',
            'xml_type': 'DateOptTimeType',
            'use': 'optional'
        }
    }


class FlexAttributes(QCodeURIMixin):
    """
    A group of attributes associated with flexible properties
    """
    attributes = {
        # we now get qcode and uri from QCodeURIMixin
        # # A qualified code which identifies a concept.
        # 'qcode': 'qcode', 'xml_type': 'QCodeType'
        # # A URI which identifies a concept.
        # 'uri': 'uri', 'xml_type': 'IRIType'
        # A free-text value assigned as property value.
        'literal': {
            'xml_name': 'literal',
            'xml_type': 'g2normalizedString'
        },
        # The type of the concept assigned as controlled property value - expressed by a QCode
        'type': {
            'xml_name': 'type',
            'xml_type': 'QCodeType'
        },
        # The type of the concept assigned as controlled property value - expressed by a URI
        'typeuri': {
            'xml_name': 'typeuri',
            'xml_type': 'IRIType'
        }
    }


class RankingAttributes(BaseObject):
    """
    A group of attributes for ranking properties of the same name
    """
    attributes = {
        # Indicates the relative importance of properties in a list.
        'rank': {
            'xml_name': 'rank',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        }
    }


class PersistentEditAttributes(BaseObject):
    """
    A group of attributes to keep track of by whom and when the property value
    was changed with a persistent ID
    """
    attributes = {
        # The local identifier of the element which MUST be persistent for all
        # versions of the item, i.e. for its entire lifecycle.
        'id': {
            'xml_name': 'id',
            'xml_type': 'xs:ID',
            'use': 'optional'
        },
        # If the element is empty, specifies which entity (person, organisation
        # or system) will edit the property - expressed by a QCode. If the
        # element is non-empty, specifies which entity (person, organisation or
        # system) has edited the property.
        'creator': {
            'xml_name': 'creator',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # If the element is empty, specifies which entity (person, organisation
        # or system) will edit the property - expressed by a URI. If the element
        # is non-empty, specifies which entity (person, organisation or system)
        # has edited the property.
        'creatoruri': {
            'xml_name': 'creatoruri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The date (and, optionally, the time) when the property was last
        # modified. The initial value is the date (and, optionally, the time) of
        # creation of the property.
        'modified': {
            'xml_name': 'modified',
            'xml_type': 'DateOptTimeType',
            'use': 'optional'
        }
    }


class ArbitraryValueAttributes(BaseObject):
    """
    Attributes for properties that take an arbitrary value, optionally with a
    value unit.
    """
    attributes = {
        # The related value (see more in the spec document)
        'value': {
            'xml_name': 'value',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # The datatype of the value attribute – it MUST be one of the
        # built-in datatypes defined by XML Schema version 1.0.
        'valuedatatype': {
            'xml_name': 'valuedatatype',
            'xml_type': 'xs:QName',
            'use': 'optional'
        },
         # The unit of the value attribute.
        'valueunit': {
            'xml_name': 'valueunit',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
         # The unit of the value attribute - expressed by a URI
        'valueunituri': {
            'xml_name': 'valueunituri',
            'xml_type': 'IRIType',
            'use': 'optional'
        }
    }


class QualifyingAttributes(BaseObject):
    """
    A group of attributes used for a qualified expression of the property
    """
    attributes = {
        # A qualified code assigned as a property value.
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
        # A free-text value assigned as a property value.
        'literal': {
            'xml_name': 'literal',
            'xml_type': 'g2normalizedString',
            'use': 'optional'
        },
        # The type of the concept assigned as a controlled or an uncontrolled
        # property value - expressed by a QCode
        'type': {
            'xml_name': 'type',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The type of the concept assigned as a controlled or an uncontrolled
        # property value - expressed by a URI
        'typeuri': {
            'xml_name': 'typeuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # A refinement of the semantics of the property - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # A refinement of the semantics of the property - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        }
    }


class NewsContentAttributes(BaseObject):
    """
    A group of typical attributes associated with a content rendition
    """
    attributes = {
        # The local identifier of the element which MUST be persistent for all
        # versions of the item, i.e. for its entire lifecycle.
        'id': {
            'xml_name': 'id',
            'xml_type': 'xs:ID'
        },
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a QCode.
        # If the attribute is non-empty, specifies which entity (person,
        # organisation or system) has edited the property.
        'creator': {
            'xml_name': 'creator',
            'xml_type': 'QCodeType'
        },
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a URI.
        # If the attribute is non-empty, specifies which entity (person,
        # organisation or system) has edited the property.
        'creatoruri': {
            'xml_name': 'creatoruri',
            'xml_type': 'IRIType'
        },
        # The date (and, optionally, the time) when the property was last
        # modified. The initial value is the date (and, optionally, the time) of
        # creation of the property.
        'modified': {
            'xml_name': 'modified',
            'xml_type': 'DateOptTimeType'
        },
        # If set to true the corresponding property was added to the G2 Item for
        # a specific customer or group of customers only. The default value of
        # this property is false which applies when this attribute is not used
        # with the property.
        'custom': {
            'xml_name': 'custom',
            'xml_type': 'xs:boolean'
        },
        # Indicates by which means the value was extracted from the content -
        # expressed by a QCode
        'how': {
            'xml_name': 'how',
            'xml_type': 'QCodeType'
        },
        # Indicates by which means the value was extracted from the content -
        # expressed by a URI
        'howuri': {
            'xml_name': 'howuri',
            'xml_type': 'IRIType'
        },
        # Why the metadata has been included - expressed by a QCode
        'why': {
            'xml_name': 'why',
            'xml_type': 'QCodeType'
        },
        # Why the metadata has been included - expressed by a URI
        'whyuri': {
            'xml_name': 'whyuri',
            'xml_type': 'IRIType'
        },
        # The specific rendition of content this component represents -
        # expressed by a QCode
        'rendition': {
            'xml_name': 'rendition',
            'xml_type': 'QCodeType'
        },
        # The specific rendition of content this component represents -
        # expressed by a URI
        'renditionuri': {
            'xml_name': 'renditionuri',
            'xml_type': 'IRIType'
        },
        # The name and version of the software tool used to generate the content
        'generator': {
            'xml_name': 'generator',
            'xml_type': 'xs:string'
        },
        # The date (and, optionally, the time) when the content was generated
        'generated': {
            'xml_name': 'generated',
            'xml_type': 'DateOptTimeType'
        },
        # Indicates if the digital data of this rendition is available or not.
        'hascontent': {
            'xml_name': 'hascontent',
            'xml_type': 'xs:boolean'
        }
    }


class NewsContentTypeAttributes(BaseObject):
    """
    A group of attributes representing a content type
    """
    attributes = {
        # An IANA MIME type
        'contenttype': {
            'xml_name': 'contenttype',
            'xml_type': 'xs:string'
        },
        # Version of the standard identified by contenttype.
        'contenttypestandardversion': {
            'xml_name': 'contenttypestandardversion',
            'xml_type': 'xs:string'
        },
        # A refinement of a generic content type (i.e. IANA MIME type) by a literal string value.
        'contenttypevariant': {
            'xml_name': 'contenttypevariant',
            'xml_type': 'xs:string'
        },
        # Version of the standard identified by contenttypevariant.
        'contenttypevariantstandardversion': {
            'xml_name': 'contenttypevariantstandardversion',
            'xml_type': 'xs:string'
        },
        # A refinement of a generic content type (i.e. IANA MIME type) - expressed by a QCode
        'format': {
            'xml_name': 'format',
            'xml_type': 'QCodeType'
        },
        # A refinement of a generic content type (i.e. IANA MIME type) - expressed by a URI
        'formaturi': {
            'xml_name': 'formaturi',
            'xml_type': 'IRIType'
        },
        # Version of the standard identified by the format.
        'formatstandardversion': {
            'xml_name': 'formatstandardversion',
            'xml_type': 'xs:string'
        }
    }


class MediaContentCharacteristics1(BaseObject):
    """
    A group of typical physical characteristics of media content
    """
    attributes = {
        # The width of visual content.
        'width': {
            'xml_name': 'width',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # If present defines the width unit for the width - expressed by a QCode
        'widthunit': {
            'xml_name': 'widthunit',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # If present defines the width unit for the width - expressed by a URI
        'widthunituri': {
            'xml_name': 'widthunituri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The height of visual content.
        'height': {
            'xml_name': 'height',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # If present defines the height unit for the heigth - expressed by a QCode
        'heightunit': {
            'xml_name': 'heightunit',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # If present defines the height unit for the heigth - expressed by a URI
        'heightunituri': {
            'xml_name': 'heightunituri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The orientation of the visual content of an image in regard to the
        # standard rendition of the digital image data. Values in the range of
        # 1 to 8 are compatible with the TIFF 6.0 and Exif 2.3 specifications.
        # Applies to image content.
        'orientation': {
            'xml_name': 'orientation',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # Indicates whether the human interpretation of the top of the image is
        # aligned to its short or long side - expressed by a QCode
        'layoutorientation': {
            'xml_name': 'layoutorientation',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # Indicates whether the human interpretation of the top of the image is
        # aligned to its short or long side - expressed by a URI
        'layoutorientationuri': {
            'xml_name': 'layoutorientationuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The colour space of an image. Applies to image icons - expressed by a QCode
        'colourspace': {
            'xml_name': 'colourspace',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The colour space of an image. Applies to image icons - expressed by a URI
        'colourspaceuri': {
            'xml_name': 'colourspaceuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # Indicates whether the still or moving image is coloured or black and
        # white. The recommended vocabulary is the IPTC Colour Indicator
        # NewsCodes http://cv.iptc.org/newscodes/colourindicator/ - expressed
        # by a QCode
        'colourindicator': {
            'xml_name': 'colourindicator',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # Indicates whether the still or moving image is coloured or black and
        # white. The recommended vocabulary is the IPTC Colour Indicator
        # NewsCodes http://cv.iptc.org/newscodes/colourindicator/ - expressed
        # by a URI
        'colourindicatoruri': {
            'xml_name': 'colourindicatoruri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The applicable codec for video data. Applies to video icons -
        # expressed by a QCode
        'videocodec': {
            'xml_name': 'videocodec',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The applicable codec for video data. Applies to video icons -
        # expressed by a URI
        'videocodecuri': {
            'xml_name': 'videocodecuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The bit depth defining the spread of colour data within each sample.
        'colourdepth': {
            'xml_name': 'colourdepth',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        }
    }


class NewsContentCharacteristics(BaseObject):
    """
    A group of typical physical characteristics of media content
    """
    attributes = {
        # The count of characters of textual content.
        'charcount': {
            'xml_name': 'charcount',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # The count of words of textual content.
        'wordcount': {
            'xml_name': 'wordcount',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # The count of lines of textual content
        'linecount': {
            'xml_name': 'linecount',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # The count of pages of the content
        'pagecount': {
            'xml_name': 'pagecount',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # The image width for visual content.
        'width': {
            'xml_name': 'width',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # If present defines the width unit for the width - expressed by a QCode
        'widthunit': {
            'xml_name': 'widthunit',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # If present defines the width unit for the width - expressed by a URI
        'widthunituri': {
            'xml_name': 'widthunituri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The height of visual content.
        'height': {
            'xml_name': 'height',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # If present defines the height unit for the heigth - expressed by a QCode
        'heightunit': {
            'xml_name': 'heightunit',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # If present defines the height unit for the heigth - expressed by a URI
        'heightunituri': {
            'xml_name': 'heightunituri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The orientation of the visual content of an image in regard to the
        # standard rendition of the digital image data
        'orientation': {
            'xml_name': 'orientation',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # Indicates whether the human interpretation of the top of the image is
        # aligned to its short or long side - expressed by a QCode
        'layoutorientation': {
            'xml_name': 'layoutorientation',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # Indicates whether the human interpretation of the top of the image is
        # aligned to its short or long side - expressed by a URI
        'layoutorientationuri': {
            'xml_name': 'layoutorientationuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The colour space of an image - expressed by a QCode
        'colourspace': {
            'xml_name': 'colourspace',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The colour space of an image - expressed by a URI
        'colourspaceuri': {
            'xml_name': 'colourspaceuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # Indicates whether the still or moving image is coloured or black and
        # white. The recommended vocabulary is the IPTC Colour Indicator
        # NewsCodes http://cv.iptc.org/newscodes/colourindicator/
        # - expressed by a QCode
        'colourindicator': {
            'xml_name': 'colourindicator',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # Indicates whether the still or moving image is coloured or black and
        # white. The recommended vocabulary is the IPTC Colour Indicator
        # NewsCodes http://cv.iptc.org/newscodes/colourindicator/
        # - expressed by a URI
        'colourindicatoruri': {
            'xml_name': 'colourindicatoruri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The bit depth defining the spread of colour data within each sample.
        'colourdepth': {
            'xml_name': 'colourdepth',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # The recommended printing resolution for an image in dots per inch
        'resolution': {
            'xml_name': 'resolution',
            'xml_type': 'xs:positiveInteger',
            'use': 'optional'
        },
        # The clip duration in time units defined by durationUnit. The default
        # time unit is seconds. Applies to audio-visual content.
        'duration': {
            'xml_name': 'duration',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # If present it defines the time unit for the duration attribute. Only
        # codes for integer value time units of the recommended CV (available at
        # http://cv.iptc.org/newscodes/timeunit/ ) must be applied
        # - expressed by a QCode
        'durationunit': {
            'xml_name': 'durationunit',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # If present it defines the time unit for the duration attribute. Only
        # codes for integer value time units of the recommended CV (available at
        # http://cv.iptc.org/newscodes/timeunit/ ) must be applied
        # - expressed by a URI
        'durationunituri': {
            'xml_name': 'durationunituri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The applicable codec for audio data - expressed by a QCode
        'audiocodec': {
            'xml_name': 'audiocodec',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The applicable codec for audio data - expressed by a URI
        'audiocodecuri': {
            'xml_name': 'audiocodecuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The audio bit rate in  bits per second
        'audiobitrate': {
            'xml_name': 'audiobitrate',
            'xml_type': 'xs:positiveInteger',
            'use': 'optional'
        },
        # An indication that the audio data is encoded with a variable bit rate
        'audiovbr': {
            'xml_name': 'audiovbr',
            'xml_type': 'xs:boolean',
            'use': 'optional'
        },
        # The number of bits per audio sample
        'audiosamplesize': {
            'xml_name': 'audiosamplesize',
            'xml_type': 'xs:positiveInteger',
            'use': 'optional'
        },
        # The number of audio samples per second, expressed as a sampling frequency in Hz
        'audiosamplerate': {
            'xml_name': 'audiosamplerate',
            'xml_type': 'xs:positiveInteger',
            'use': 'optional'
        },
        # The audio sound system - expressed by a QCode
        'audiochannels': {
            'xml_name': 'audiochannels',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The audio sound system - expressed by a URI
        'audiochannelsuri': {
            'xml_name': 'audiochannelsuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The applicable codec for video data - expressed by a QCode
        'videocodec': {
            'xml_name': 'videocodec',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The applicable codec for video data - expressed by a URI
        'videocodecuri': {
            'xml_name': 'videocodecuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The video average bit rate in bits per second. Used when the bit rate is variable
        'videoavgbitrate': {
            'xml_name': 'videoavgbitrate',
            'xml_type': 'xs:positiveInteger',
            'use': 'optional'
        },
        # An indication that video data is encoded with a variable bit rate
        'videovbr': {
            'xml_name': 'videovbr',
            'xml_type': 'xs:boolean',
            'use': 'optional'
        },
        # The number of video frames per second, i.e. the rate at which the
        # material should be shown in order to achieve the intended visual effect
        'videoframerate': {
            'xml_name': 'videoframerate',
            'xml_type': 'xs:decimal',
            'use': 'optional'
        },
        # The video scan technique, progressive or interlaced
        'videoscan': {
            'xml_name': 'videoscan',
            # TODO <xs:enumeration value="progressive"/> <xs:enumeration value="interlaced"/>
        },
        # The video aspect ratio
        'videoaspectratio': {
            'xml_name': 'videoaspectratio',
            'xml_type': 'g2normalizedString',
            'use': 'optional'
        },
        # The video sampling method
        'videosampling': {
            'xml_name': 'videosampling',
            'xml_type': 'g2normalizedString',
            'use': 'optional'
        },
        # Indicates how the original content was scaled to this format
        # - expressed by a QCode. The recommended vocabulary is the IPTC Video
        # Scaling NewsCodes http://cv.iptc.org/newscodes/videoscaling/
        'videoscaling': {
            'xml_name': 'videoscaling',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # Indicates how the original content was scaled to this format
        # - expressed by a URI. The recommended vocabulary is the IPTC Video
        # Scaling NewsCodes http://cv.iptc.org/newscodes/videoscaling/
        'videoscalinguri': {
            'xml_name': 'videoscalinguri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # Indicates which video definition is applied to this rendition of video
        # content - expressed by a QCode - but it does not imply any particular
        # technical characteristics of the video. The recommended vocabulary is
        # the IPTC Video Definition NewsCodes
        # http://cv.iptc.org/newscodes/videodefinition/
        'videodefinition': {
            'xml_name': 'videodefinition',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # Indicates which video definition is applied to this rendition of video
        # content - expressed by a URI - but it does not imply any particular
        # technical characteristics of the video.The recommended vocabulary is
        # the IPTC Video Definition NewsCodes
        # http://cv.iptc.org/newscodes/videodefinition/
        'videodefinitionuri': {
            'xml_name': 'videodefinitionuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        }
    }


class ConfirmationStatusAttributes(BaseObject):
    """
    A group of attributes reflecting the confirmation status of a date.
    """
    attributes = {
        # Indicates the confirmation status of the date/period/duration. The
        # recommended vocabulary is the IPTC Event Date Confirmation NewsCodes
        # - http://cv.iptc.org/newscodes/eventdateconfirm/ - expressed by a QCode.
        'confirmationstatus': {
            'xml_name': 'confirmationstatus',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # Indicates the confirmation status of the date/period/duration. The
        # recommended vocabulary is the IPTC Event Date Confirmation NewsCodes
        # - http://cv.iptc.org/newscodes/eventdateconfirm/ - expressed by a URI.
        'confirmationstatusuri': {
            'xml_name': 'confirmationstatusuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        }
    }
