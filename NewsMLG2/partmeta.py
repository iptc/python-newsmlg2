"""
partMeta support
"""

from .attributegroups import CommonPowerAttributes, I18NAttributes
from .concepts import QualPropType
from .contentmeta import (
    AdministrativeMetadataGroup, DescriptiveMetadataGroup, Icon
)
from .extensionproperties import Flex2ExtPropType
from .itemmanagement import EdNote, Signal
from .link import Link

class TimeDelim(CommonPowerAttributes):
    """
    A delimiter for a piece of streaming media content, expressed in various
    time formats
    """
    attributes = {
        # The start time of the part in a timeline. The expressed time unit is
        # excluded. Using the Edit Unit requires the frame rate or sampling rate
        # to be known, this must be defined by the referenced rendition of the
        # content.
        'start': 'start',  # type="xs:string" use="required">
        # The end time of the part in a timeline. The expressed time unit is
        # included. Using the Edit Unit requires the frame rate or sampling rate
        # to be known, this must be defined by the referenced rendition of the
        # content.
        'end': 'end',  # type="xs:string" use="required">
        # The unit used for the start and end timestamps - expressed by a QCode
        # either the timeunit or the timeunituri attribute MUST be used
        'timeunit': 'timeunit',  # type="QCodeType">
        # The unit used for the start and end timestamps - expressed by a URI
        # either the timeunit or the timeunituri attribute MUST be used
        'timeunituri': 'timeunituri',  # type="IRIType">
        # Refers to the content rendition with this QCode as rendition attribute
        # value - expressed by a QCode
        'renditionref': 'renditionref',  # type="QCodeType">
        # Refers to the content rendition with this QCode as rendition attribute
        # value - expressed by a URI
        'renditionrefuri': 'renditionrefuri'  # type="IRIType">
    }


class RegionDelim(CommonPowerAttributes):
    """
    A delimiter for a rectangular region in a piece of visual content
    """
    attributes = {
        # The x-axis coordinate of the side of the rectangle which has the
        # smaller x-axis coordinate value in the current user coordinate system
        'x': 'x',  # type="xs:integer">
        # The y-axis coordinate of the side of the rectangle which has the
        # smaller y-axis coordinate value in the current user coordinate system
        'y': 'y',  # type="xs:integer">
        # The width of the rectangle</xs:documentation>
        'width': 'width',  # type="xs:integer">
        # The height of the rectangle</xs:documentation>
        'height': 'height'  # type="xs:nonNegativeInteger">
    }


class PartMetaRole(QualPropType):
    """
    The role [of this part] in the overall content stream.
    """


class PartMetaExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """


class PartMetaPropType(AdministrativeMetadataGroup, DescriptiveMetadataGroup,
    I18NAttributes):
    """
    A type representing the structure of a partMeta property
    """
    elements = {
        'icon': { 'type': 'array', 'xml_name': 'icon', 'element_class': Icon },
        'timedelim': {
            'type': 'array', 'xml_name': 'timeDelim',
            'element_class': TimeDelim
        },
        'regiondelim': {
            'type': 'single', 'xml_name': 'regionDelim',
            'element_class': RegionDelim
        },
        'role': {
            'type': 'single', 'xml_name': 'regionDelim',
            'element_class': RegionDelim
        },
        'partmetaextproperty': {
            'type': 'array', 'xml_name': 'partMetaExtProperty',
            'element_class': PartMetaExtProperty
        },
        'signal': {
            'type': 'array', 'xml_name': 'signal', 'element_class': Signal
        },
        'ednote': {
            'type': 'array', 'xml_name': 'edNote', 'element_class': EdNote
         },
        'link': {
            'type': 'array', 'xml_name': 'link', 'element_class': Link
        }
    }
    attributes = {
        # The identifier of the part
        'partid': 'partid',  # type="xs:ID" use="optional">
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a QCode.
        # If the attribute is non-empty, specifies which entity (person,
        # organisation or system) has edited the property.
        'creator': 'creator',  # type="QCodeType" use="optional">
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a URI.
        # If the attribute is non-empty, specifies which entity (person,
        # organisation or system) has edited the property.
        'creatoruri': 'creatoruri',  # type="IRIType" use="optional">
        # The date (and, optionally, the time) when the property was last
        # modified. The initial value is the date (and, optionally, the time) of
        # creation of the property.
        'modified': 'modified',  # type="DateOptTimeType" use="optional">
        # If set to true the corresponding property was added to the G2 Item for
        # a specific customer or group of customers only. The default value of
        # this property is false which applies when this attribute is not used
        # with the property.
        'custom': 'custom',  # type="xs:boolean" use="optional">
        # Indicates by which means the value was extracted from the content -
        # expressed by a QCode
        'how': 'how',  # type="QCodeType" use="optional">
        # Indicates by which means the value was extracted from the content -
        # expressed by a URI
        'howuri': 'howuri',  # type="IRIType" use="optional">
        # Why the metadata has been included - expressed by a QCode
        'why': 'why',  # type="QCodeType" use="optional">
        # Why the metadata has been included - expressed by a URI
        'whyuri': 'whyuri',  # type="IRIType" use="optional">
        # The sequence number of the part
        'seq': 'seq',  # type="xs:nonNegativeInteger" use="optional">
        # A list of identifiers of XML elements containing content which is
        # described by this partMeta structure.
        'contentrefs': 'contentrefs'  # type="xs:IDREFS" use="optional">
    }


class PartMeta(PartMetaPropType):
    """
    A set of properties describing a specific part of the content of the Item.
    The relationship of properties inside this partMeta and properties at a
    higher hierarchical level of the content parts structure is:
    - the semantic assertion of all properties at a higher level is inherited by
    this partMeta element as if these properities would be its children
    - a child property of a specific name wipes out for this partMeta element
    any semantic assertions of properties of the same name at higher levels
    - in this latter case: if the semantic assertion of a property at a higher
    level should be reinstated for this part of the content then this property
    has to appear again as child of this partMeta
    """
