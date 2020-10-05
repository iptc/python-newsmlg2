#!/usr/bin/env python

import json
import os

from lxml import etree

DEBUG = True

from .core import NEWSMLG2_NS, BaseObject
from .anyitem import AnyItem
from .newsmlg2 import CommonPowerAttributes, I18NAttributes

class NewsItem(AnyItem):
    """
    An Item containing news-related information
    """

    def __init__(self,  **kwargs):
        super(NewsItem, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            #self.contentMeta = ContentMeta(
            #    xmlelement = xmlelement.find(NEWSMLG2_NS+'contentMeta')
            #)
            #self.partMeta = PartMetaList(
            #    xmlarray = xmlelement.findall(NEWSMLG2_NS+'partMeta')
            #)
            #self.assertList = AssertList(
            #    xmlarray = xmlelement.findall(NEWSMLG2_NS+'assert')
            #)
            #self.inlineRefList = InlineRefList(
            #    xmlarray = xmlelement.findall(NEWSMLG2_NS+'inlineRef')
            #)
            #self.derivedFromList = DerivedFromList(
            #    xmlarray = xmlelement.findall(NEWSMLG2_NS+'derivedFrom')
            #)
            #self.derivedFromValueList = DerivedFromValueList(
            #    xmlarray = xmlelement.findall(NEWSMLG2_NS+'derivedFromValue')
            #)
            self.contentSet = ContentSet(
                xmlelement = xmlelement.find(NEWSMLG2_NS+'contentSet')
            )

    def to_xml(self):
        xmlelem = etree.Element(NEWSMLG2_NS+'newsItem')
        return xmlelem

#    def getItemClass(self):
#        return self.itemMeta.itemClass.getQcode()

#    def getItemClassURI(self):
#        return self.itemMeta.itemClass.getURI()

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
                xmlelement = xmlelement.find(NEWSMLG2_NS+'inlineXML')
            )
 

class NewsContentAttributes():
    """
    A group of typical attributes associated with a content rendition
    """
    attributes = {
        # The local identifier of the element which MUST be persistent for all versions of the item, i.e. for its entire lifecycle.
        'id': 'id', # type="xs:ID"
        # If the attribute is empty, specifies which entity (person, organisation or system) will edit the property - expressed by a QCode. If the attribute is non-empty, specifies which entity (person, organisation or system) has edited the property.
        'creator': 'creator', # type="QCodeType"
        # If the attribute is empty, specifies which entity (person, organisation or system) will edit the property - expressed by a URI. If the attribute is non-empty, specifies which entity (person, organisation or system) has edited the property.
        'creatoruri': 'creatoruri', # type="IRIType"
        # The date (and, optionally, the time) when the property was last modified. The initial value is the date (and, optionally, the time) of creation of the property.
        'modified': 'modified', # type="DateOptTimeType"
        # If set to true the corresponding property was added to the G2 Item for a specific customer or group of customers only. The default value of this property is false which applies when this attribute is not used with the property.
        'custom': 'custom', # type="xs:boolean"
        # Indicates by which means the value was extracted from the content - expressed by a QCode
        'how': 'how', # type="QCodeType"
        # Indicates by which means the value was extracted from the content - expressed by a URI
        'howuri': 'howuri', # type="IRIType"
        # Why the metadata has been included - expressed by a QCode
        'why': 'why', # type="QCodeType"
        # Why the metadata has been included - expressed by a URI
        'whyuri': 'whyuri', # type="IRIType"
        # The specific rendition of content this component represents - expressed by a QCode
        'rendition': 'rendition', # type="QCodeType"
        # The specific rendition of content this component represents - expressed by a URI
        'renditionuri': 'renditionuri', # type="IRIType"
        # The name and version of the software tool used to generate the content
        'generator': 'generator', # type="xs:string"
        # The date (and, optionally, the time) when the content was generated
        'generated': 'generated', # type="DateOptTimeType"
        # Indicates if the digital data of this rendition is available or not.
        'hascontent': 'hascontent', # type="xs:boolean"
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
        # The orientation of the visual content of an image in regard to the standard rendition of the digital image data
        'orientation': 'orientation', # type="xs:nonNegativeInteger" use="optional">
        # Indicates whether the human interpretation of the top of the image is aligned to its short or long side - expressed by a QCode
        'layoutorientation': 'layoutorientation', # type="QCodeType" use="optional">
        # Indicates whether the human interpretation of the top of the image is aligned to its short or long side - expressed by a URI
        'layoutorientationuri': 'layoutorientationuri', # type="IRIType" use="optional">
        # The colour space of an image - expressed by a QCode
        'colourspace': 'colourspace', # type="QCodeType" use="optional">
        # The colour space of an image - expressed by a URI
        'colourspaceuri': 'colourspaceuri', # type="IRIType" use="optional">
        # Indicates whether the still or moving image is coloured or black and white. The recommended vocabulary is the IPTC Colour Indicator NewsCodes http://cv.iptc.org/newscodes/colourindicator/  - expressed by a QCode
        'colourindicator': 'colourindicator', # type="QCodeType" use="optional">
        # Indicates whether the still or moving image is coloured or black and white. The recommended vocabulary is the IPTC Colour Indicator NewsCodes http://cv.iptc.org/newscodes/colourindicator/  - expressed by a URI
        'colourindicatoruri': 'colourindicatoruri', # type="IRIType" use="optional">
        # The bit depth defining the spread of colour data within each sample.
        'colourdepth': 'colourdepth', # type="xs:nonNegativeInteger" use="optional">
        # The bit depth defining the spread of colour data within each sample.
        'colourdepth': 'colourdepth', # type="xs:nonNegativeInteger" use="optional">
        # The recommended printing resolution for an image in dots per inch
        'resolution': 'resolution', # type="xs:positiveInteger" use="optional">
        # The clip duration in time units defined by durationUnit. The default time unit is seconds. Applies to audio-visual content.
        'duration': 'duration', # type="xs:string" use="optional">
        # If present it defines the time unit for the duration attribute. Only codes for integer value time units of the recommended CV (available at http://cv.iptc.org/newscodes/timeunit/ )  must be applied - expressed by a QCode
        'durationunit': 'durationunit', # type="QCodeType" use="optional">
        # If present it defines the time unit for the duration attribute. Only codes for integer value time units of the recommended CV (available at http://cv.iptc.org/newscodes/timeunit/ )  must be applied - expressed by a URI
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
        # The number of video frames per second, i.e. the rate at which the material should be shown in order to achieve the intended visual effect
        'videoframerate': 'videoframerate', # type="xs:decimal" use="optional">
        # The video scan technique, progressive or interlaced
        'videoscan': 'videoscan', # <xs:enumeration value="progressive"/> <xs:enumeration value="interlaced"/>
        # The video aspect ratio
        'videoaspectratio': 'videoaspectratio', # type="g2normalizedString" use="optional">
        # The video sampling method
        'videosampling': 'videosampling', # type="g2normalizedString" use="optional">
        # Indicates how the original content was scaled to this format - expressed by a QCode. The recommended vocabulary is the IPTC Video Scaling NewsCodes http://cv.iptc.org/newscodes/videoscaling/ 
        'videoscaling': 'videoscaling', # type="QCodeType" use="optional">
        # Indicates how the original content was scaled to this format - expressed by a URI. The recommended vocabulary is the IPTC Video Scaling NewsCodes http://cv.iptc.org/newscodes/videoscaling/
        'videoscalinguri': 'videoscalinguri', # type="IRIType" use="optional">
        # Indicates which video definition is applied to this rendition of video content - expressed by a QCode - but it does not imply any particular technical characteristics of the video.The recommended vocabulary is the IPTC Video Definition NewsCodes http://cv.iptc.org/newscodes/videodefinition/
        'videodefinition': 'videodefinition', # type="QCodeType" use="optional">
        # Indicates which video definition is applied to this rendition of video content - expressed by a URI - but it does not imply any particular technical characteristics of the video.The recommended vocabulary is the IPTC Video Definition NewsCodes http://cv.iptc.org/newscodes/videodefinition/ 
        'videodefinitionuri': 'videodefinitionuri', # type="IRIType" use="optional">
    }

class InlineXML(NewsContentAttributes, NewsContentTypeAttributes, NewsContentCharacteristics, I18NAttributes):
    """
    A rendition of the content using an XML language
    """
    def __init__(self,  **kwargs):
        super(InlineXML, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            pass
