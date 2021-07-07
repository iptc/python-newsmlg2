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
        'id': 'id',
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a
        # QCode. If the attribute is non-empty, specifies which entity
        # (person, organisation or system) has edited the property.
        'creator': 'creator',
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a
        # URI. If the attribute is non-empty, specifies which entity
        # (person, organisation or system) has edited the property.
        'creatoruri': 'creatoruri',
        # The date (and, optionally, the time) when the property was last
        # modified. The initial value is the date (and, optionally, the
        # time) of creation of the property.
        'modified': 'modified',
        # If set to true the corresponding property was added to the G2
        # Item for a specific customer or group of customers only. The
        # default value of this property is false which applies when this
        #  attribute is not used with the property.
        'custom': 'custom',
        # Indicates by which means the value was extracted from the
        # content - expressed by a QCode
        'how': 'how',
        # Indicates by which means the value was extracted from the
        # content - expressed by a URI
        'howuri': 'howuri',
        # Why the metadata has been included - expressed by a QCode
        'why': 'why',
        # Why the metadata has been included - expressed by a URI
        'whyuri': 'whyuri',
        # One or many constraints that apply to publishing the value of
        # the property - expressed by a QCode. Each constraint applies
        # to all descendant elements.
        'pubconstraint': 'pubconstraint',
        # One or many constraints that apply to publishing the value of
        # the property - expressed by a URI. Each constraint applies to
        # all descendant elements.
        'pubconstrainturi': 'pubconstrainturi'
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
            # 'default': 'en-GB'
        },
        # The directionality of textual content
        # (enumeration: ltr, rtl)
        'dir': 'dir'
    }


class QuantifyAttributes(BaseObject):
    """
    A group of attriubutes quantifying the property value
    """
    attributes = {
        # The confidence with which the metadata has been assigned.
        'confidence': 'confidence', # type="Int100Type" use="optional">
        # The relevance of the metadata to the news content to which it is
        # attached.
        'relevance': 'relevance', # type="Int100Type" use="optional">
        # A reference to the concept from which the concept identified by qcode
        # was derived/inferred - use DEPRECATED in NewsML-G2 2.12 and higher,
        # use the derivedFrom element
        'derivedfrom': 'derivedfrom', # type="QCodeListType" use="optional">
    }


class TimeValidityAttributes(BaseObject):
    """
    A group of attributes expressing the time period of validity of a relationship
    """
    attributes = {
        # The date (and, optionally, the time) before which a relationship is not valid.
        'validfrom': 'validfrom', # type="DateOptTimeType" use="optional">
        # The date (and, optionally, the time) after which a relationship is not valid.
        'validto': 'validto', # type="DateOptTimeType" use="optional">
    }


class FlexAttributes(QCodeURIMixin):
    """
    A group of attributes associated with flexible properties
    """
    attributes = {
        # we now get qcode and uri from QCodeURIMixin
        # # A qualified code which identifies a concept.
        # 'qcode': 'qcode',  # type="QCodeType"
        # # A URI which identifies a concept.
        # 'uri': 'uri',  # type="IRIType"
        # A free-text value assigned as property value.
        'literal': 'literal',  # type="g2normalizedString"
        # The type of the concept assigned as controlled property value - expressed by a QCode
        'type': 'type',  # type="QCodeType"
        # The type of the concept assigned as controlled property value - expressed by a URI
        'typeuri': 'typeuri',  # type="IRIType"
    }


class RankingAttributes(BaseObject):
    """
    A group of attributes for ranking properties of the same name
    """
    attributes = {
        # Indicates the relative importance of properties in a list.
        'rank': 'rank',  # type="xs:nonNegativeInteger" use="optional">
    }


class PersistentEditAttributes(BaseObject):
    """
    A group of attributes to keep track of by whom and when the property value
    was changed with a persistent ID
    """
    attributes = {
        # The local identifier of the element which MUST be persistent for all
        # versions of the item, i.e. for its entire lifecycle.
        'id': 'id',  # type="xs:ID" use="optional">
        # If the element is empty, specifies which entity (person, organisation
        # or system) will edit the property - expressed by a QCode. If the
        # element is non-empty, specifies which entity (person, organisation or
        # system) has edited the property.
        'creator': 'creator',  # type="QCodeType" use="optional">
        # If the element is empty, specifies which entity (person, organisation
        # or system) will edit the property - expressed by a URI. If the element
        # is non-empty, specifies which entity (person, organisation or system)
        # has edited the property.
        'creatoruri': 'creatoruri',  # type="IRIType" use="optional">
        # The date (and, optionally, the time) when the property was last
        # modified. The initial value is the date (and, optionally, the time) of
        # creation of the property.
        'modified': 'modified',  # type="DateOptTimeType" use="optional">
    }


class ArbitraryValueAttributes(BaseObject):
    """
    Attributes for properties that take an arbitrary value, optionally with a
    value unit.
    """
    attributes = {
        # The related value (see more in the spec document)
        'value': 'value',  # type="xs:string" use="optional">
         # The datatype of the value attribute – it MUST be one of the
        # built-in datatypes defined by XML Schema version 1.0.
        'valuedatatype': 'valuedatatype',  # type="xs:QName" use="optional">
         # The unit of the value attribute.
        'valueunit': 'valueunit',  # type="QCodeType" use="optional">
         # The unit of the value attribute - expressed by a URI
        'valueunituri': 'valueunituri',  # type="IRIType" use="optional">
    }


class QualifyingAttributes(BaseObject):
    """
    A group of attributes used for a qualified expression of the property
    """
    attributes = {
        # A qualified code assigned as a property value.
        'qcode': 'qcode',  # type="QCodeType" use="optional">
        # A URI which identifies a concept.
        'uri': 'uri',  # type="IRIType" use="optional">
        # A free-text value assigned as a property value.
        'literal': 'literal',  # type="g2normalizedString" use="optional">
        # The type of the concept assigned as a controlled or an uncontrolled
        # property value - expressed by a QCode
        'type': 'type',  # type="QCodeType" use="optional">
        # The type of the concept assigned as a controlled or an uncontrolled
        # property value - expressed by a URI
        'typeuri': 'typeuri',  # type="IRIType" use="optional">
        # A refinement of the semantics of the property - expressed by a QCode
        'role': 'role',  # type="QCodeType" use="optional">
        # A refinement of the semantics of the property - expressed by a URI
        'roleuri': 'roleuri',  # type="IRIType" use="optional">
    }


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


class NewsContentTypeAttributes(BaseObject):
    """
    A group of attributes representing a content type
    """
    attributes = {
        # An IANA MIME type
        'contenttype': 'contenttype', # type="xs:string"
        # Version of the standard identified by contenttype.
        'contenttypestandardversion': 'contenttypestandardversion', # type="xs:string"
        # A refinement of a generic content type (i.e. IANA MIME type) by a literal string value.
        'contenttypevariant': 'contenttypevariant', # type="xs:string"
        # Version of the standard identified by contenttypevariant.
        'contenttypevariantstandardversion': 'contenttypevariantstandardversion', # type="xs:string"
        # A refinement of a generic content type (i.e. IANA MIME type) - expressed by a QCode
        'format': 'format', # type="QCodeType"
        # A refinement of a generic content type (i.e. IANA MIME type) - expressed by a URI
        'formaturi': 'formaturi', # type="IRIType"
        # Version of the standard identified by the format.
        'formatstandardversion': 'formatstandardversion', # type="xs:string"
    }


class MediaContentCharacteristics1(BaseObject):
    """
    A group of typical physical characteristics of media content
    """
    attributes = {
        # The width of visual content.
        'width': 'width',  # type="xs:nonNegativeInteger" use="optional">
        # If present defines the width unit for the width - expressed by a QCode
        'widthunit': 'widthunit',  # type="QCodeType" use="optional">
        # If present defines the width unit for the width - expressed by a URI
        'widthunituri': 'widthunituri',  # type="IRIType" use="optional">
        # The height of visual content.
        'height': 'height',  # type="xs:nonNegativeInteger" use="optional">
        # If present defines the height unit for the heigth - expressed by a QCode
        'heightunit': 'heightunit',  # type="QCodeType" use="optional">
        # If present defines the height unit for the heigth - expressed by a URI
        'heightunituri': 'heightunituri',  # type="IRIType" use="optional">
        # The orientation of the visual content of an image in regard to the
        # standard rendition of the digital image data. Values in the range of
        # 1 to 8 are compatible with the TIFF 6.0 and Exif 2.3 specifications.
        # Applies to image content.
        'orientation': 'orientation',  # type="xs:nonNegativeInteger" use="optional">
        # Indicates whether the human interpretation of the top of the image is
        # aligned to its short or long side - expressed by a QCode
        'layoutorientation': 'layoutorientation',  # type="QCodeType" use="optional">
        # Indicates whether the human interpretation of the top of the image is
        # aligned to its short or long side - expressed by a URI
        'layoutorientationuri': 'layoutorientationuri',  # type="IRIType" use="optional">
        # The colour space of an image. Applies to image icons - expressed by a QCode
        'colourspace': 'colourspace',  # type="QCodeType" use="optional">
        # The colour space of an image. Applies to image icons - expressed by a URI
        'colourspaceuri': 'colourspaceuri',  # type="IRIType" use="optional">
        # Indicates whether the still or moving image is coloured or black and
        # white. The recommended vocabulary is the IPTC Colour Indicator
        # NewsCodes http://cv.iptc.org/newscodes/colourindicator/ - expressed
        # by a QCode
        'colourindicator': 'colourindicator',  # type="QCodeType" use="optional">
        # Indicates whether the still or moving image is coloured or black and
        # white. The recommended vocabulary is the IPTC Colour Indicator
        # NewsCodes http://cv.iptc.org/newscodes/colourindicator/ - expressed
        # by a URI
        'colourindicatoruri': 'colourindicatoruri',  # type="IRIType" use="optional">
        # The applicable codec for video data. Applies to video icons -
        # expressed by a QCode
        'videocodec': 'videocodec',  # type="QCodeType" use="optional">
        # The applicable codec for video data. Applies to video icons -
        # expressed by a URI
        'videocodecuri': 'videocodecuri',  # type="IRIType" use="optional">
        # The bit depth defining the spread of colour data within each sample.
        'colourdepth': 'colourdepth',  # type="xs:nonNegativeInteger" use="optional">
    }


class NewsContentCharacteristics(BaseObject):
    """
    A group of typical physical characteristics of media content
    """
    attributes = {
        # The count of characters of textual content.
        'charcount': 'charcount', # type="xs:nonNegativeInteger" use="optional">
        # The count of words of textual content.
        'wordcount': 'wordcount', # type="xs:nonNegativeInteger" use="optional">
        # The count of lines of textual content
        'linecount': 'linecount', # type="xs:nonNegativeInteger" use="optional">
        # The count of pages of the content
        'pagecount': 'pagecount', # type="xs:nonNegativeInteger" use="optional">
        # The image width for visual content.
        'width': 'width', # type="xs:nonNegativeInteger" use="optional">
        # If present defines the width unit for the width - expressed by a QCode
        'widthunit': 'widthunit', # type="QCodeType" use="optional">
        # If present defines the width unit for the width - expressed by a URI
        'widthunituri': 'widthunituri', # type="IRIType" use="optional">
        # The height of visual content.
        'height': 'height', # type="xs:nonNegativeInteger" use="optional">
        # If present defines the height unit for the heigth - expressed by a QCode
        'heightunit': 'heightunit', # type="QCodeType" use="optional">
        # If present defines the height unit for the heigth - expressed by a URI
        'heightunituri': 'heightunituri', # type="IRIType" use="optional">
        # The orientation of the visual content of an image in regard to the
        # standard rendition of the digital image data
        'orientation': 'orientation', # type="xs:nonNegativeInteger" use="optional">
        # Indicates whether the human interpretation of the top of the image is
        # aligned to its short or long side - expressed by a QCode
        'layoutorientation': 'layoutorientation', # type="QCodeType" use="optional">
        # Indicates whether the human interpretation of the top of the image is
        # aligned to its short or long side - expressed by a URI
        'layoutorientationuri': 'layoutorientationuri', # type="IRIType" use="optional">
        # The colour space of an image - expressed by a QCode
        'colourspace': 'colourspace', # type="QCodeType" use="optional">
        # The colour space of an image - expressed by a URI
        'colourspaceuri': 'colourspaceuri', # type="IRIType" use="optional">
        # Indicates whether the still or moving image is coloured or black and
        # white. The recommended vocabulary is the IPTC Colour Indicator
        # NewsCodes http://cv.iptc.org/newscodes/colourindicator/
        # - expressed by a QCode
        'colourindicator': 'colourindicator', # type="QCodeType" use="optional">
        # Indicates whether the still or moving image is coloured or black and
        # white. The recommended vocabulary is the IPTC Colour Indicator
        # NewsCodes http://cv.iptc.org/newscodes/colourindicator/
        # - expressed by a URI
        'colourindicatoruri': 'colourindicatoruri', # type="IRIType" use="optional">
        # The bit depth defining the spread of colour data within each sample.
        'colourdepth': 'colourdepth', # type="xs:nonNegativeInteger" use="optional">
        # The recommended printing resolution for an image in dots per inch
        'resolution': 'resolution', # type="xs:positiveInteger" use="optional">
        # The clip duration in time units defined by durationUnit. The default
        # time unit is seconds. Applies to audio-visual content.
        'duration': 'duration', # type="xs:string" use="optional">
        # If present it defines the time unit for the duration attribute. Only
        # codes for integer value time units of the recommended CV (available at
        # http://cv.iptc.org/newscodes/timeunit/ ) must be applied
        # - expressed by a QCode
        'durationunit': 'durationunit', # type="QCodeType" use="optional">
        # If present it defines the time unit for the duration attribute. Only
        # codes for integer value time units of the recommended CV (available at
        # http://cv.iptc.org/newscodes/timeunit/ ) must be applied
        # - expressed by a URI
        'durationunituri': 'durationunituri', # type="IRIType" use="optional">
        # The applicable codec for audio data - expressed by a QCode
        'audiocodec': 'audiocodec', # type="QCodeType" use="optional">
        # The applicable codec for audio data - expressed by a URI
        'audiocodecuri': 'audiocodecuri', # type="IRIType" use="optional">
        # The audio bit rate in  bits per second
        'audiobitrate': 'audiobitrate', # type="xs:positiveInteger" use="optional">
        # An indication that the audio data is encoded with a variable bit rate
        'audiovbr': 'audiovbr', # type="xs:boolean" use="optional">
        # The number of bits per audio sample
        'audiosamplesize': 'audiosamplesize', # type="xs:positiveInteger" use="optional">
        # The number of audio samples per second, expressed as a sampling frequency in Hz
        'audiosamplerate': 'audiosamplerate', # type="xs:positiveInteger" use="optional">
        # The audio sound system - expressed by a QCode
        'audiochannels': 'audiochannels', # type="QCodeType" use="optional">
        # The audio sound system - expressed by a URI
        'audiochannelsuri': 'audiochannelsuri', # type="IRIType" use="optional">
        # The applicable codec for video data - expressed by a QCode
        'videocodec': 'videocodec', # type="QCodeType" use="optional">
        # The applicable codec for video data - expressed by a URI
        'videocodecuri': 'videocodecuri', # type="IRIType" use="optional">
        # The video average bit rate in bits per second. Used when the bit rate is variable
        'videoavgbitrate': 'videoavgbitrate', # type="xs:positiveInteger" use="optional">
        # An indication that video data is encoded with a variable bit rate
        'videovbr': 'videovbr', # type="xs:boolean" use="optional">
        # The number of video frames per second, i.e. the rate at which the
        # material should be shown in order to achieve the intended visual effect
        'videoframerate': 'videoframerate', # type="xs:decimal" use="optional">
        # The video scan technique, progressive or interlaced
        # TODO <xs:enumeration value="progressive"/> <xs:enumeration value="interlaced"/>
        'videoscan': 'videoscan',
        # The video aspect ratio
        'videoaspectratio': 'videoaspectratio', # type="g2normalizedString" use="optional">
        # The video sampling method
        'videosampling': 'videosampling', # type="g2normalizedString" use="optional">
        # Indicates how the original content was scaled to this format
        # - expressed by a QCode. The recommended vocabulary is the IPTC Video
        # Scaling NewsCodes http://cv.iptc.org/newscodes/videoscaling/
        'videoscaling': 'videoscaling', # type="QCodeType" use="optional">
        # Indicates how the original content was scaled to this format
        # - expressed by a URI. The recommended vocabulary is the IPTC Video
        # Scaling NewsCodes http://cv.iptc.org/newscodes/videoscaling/
        'videoscalinguri': 'videoscalinguri', # type="IRIType" use="optional">
        # Indicates which video definition is applied to this rendition of video
        # content - expressed by a QCode - but it does not imply any particular
        # technical characteristics of the video. The recommended vocabulary is
        # the IPTC Video Definition NewsCodes
        # http://cv.iptc.org/newscodes/videodefinition/
        'videodefinition': 'videodefinition', # type="QCodeType" use="optional">
        # Indicates which video definition is applied to this rendition of video
        # content - expressed by a URI - but it does not imply any particular
        # technical characteristics of the video.The recommended vocabulary is
        # the IPTC Video Definition NewsCodes
        # http://cv.iptc.org/newscodes/videodefinition/
        'videodefinitionuri': 'videodefinitionuri', # type="IRIType" use="optional">
    }


class ConfirmationStatusAttributes(BaseObject):
    """
    A group of attributes reflecting the confirmation status of a date.
    """
    attributes = {
        # Indicates the confirmation status of the date/period/duration. The
        # recommended vocabulary is the IPTC Event Date Confirmation NewsCodes
        # - http://cv.iptc.org/newscodes/eventdateconfirm/ - expressed by a QCode.
        'confirmationstatus': 'confirmationstatus',  # type="QCodeType" use="optional">
        # Indicates the confirmation status of the date/period/duration. The
        # recommended vocabulary is the IPTC Event Date Confirmation NewsCodes
        # - http://cv.iptc.org/newscodes/eventdateconfirm/ - expressed by a URI.
        'confirmationstatusuri': 'confirmationstatusuri',  # type="IRIType" use="optional">
    }
