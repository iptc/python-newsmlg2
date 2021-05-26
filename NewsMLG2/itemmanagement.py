#!/usr/bin/env python

import json
import os
from lxml import etree

"""
Properties from xs:group ItemManagementGroup
"""

from .core import BaseObject, GenericArray
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, NewsContentTypeAttributes,
    TimeValidityAttributes
)
from .complextypes import (
    DateOptTimePropType, DateTimeOrNullPropType, DateTimePropType,
    VersionedStringType
)
from .conceptgroups import (
    Flex1PropType, FlexAuthorPropType, FlexPartyPropType
)
from .labeltypes import BlockType
from .link import Link1Type
from .propertytypes import (
    QCodePropType, QualPropType, QualRelPropType
)
from .rights import RightsBlockType
from .simpletypes import G2NormalizedString, IRIType

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


class FileName(G2NormalizedString, CommonPowerAttributes):
    """
    The recommended file name for this Item.
    """


class GeneratorElement(VersionedStringType):
    """
    The name and version of the software tool used to generate the Item.
    """
    attributes = {
        # Indentifies the stage at which this generator was used - expressed by a QCode
        'role', #  type="QCodeType"
        # Indentifies the stage at which this generator was used - expressed by a URI
        'roleuri' #  type="IRIType"
    }


class Generator(GenericArray):
    element_class = GeneratorElement


class Profile(VersionedStringType):
    """
    This property provides information about the structure of an Item,
    e.g. a simple package or an article with one picture.
    """


class TitleElement:
    """
    A short natural language name for the Item.
    """

class Title(GenericArray):
    element_class = TitleElement


class EdNoteElement(BlockType):
    """
    A note addressed to the editorial people receiving the Item.
    """


class EdNote(GenericArray):
    element_class = EdNoteElement


class MemberOfElement(Flex1PropType):
    """
    A set of Items around the same theme that this Item is part of.
    """


class MemberOf(GenericArray):
    element_class = MemberOfElement


class InstanceOfElement(Flex1PropType):
    """
    A frequently updating information object that this Item is an instance of.
    """


class InstanceOf(GenericArray):
    element_class = InstanceOfElement


class SignalElement(Flex1PropType):
    """
    An instruction to the processor that the content requires special handling.
    """
    attributes = {
        # Indicates how severe the impact from the signal is - expressed by a QCode.
        # The recommended vocabular is the IPTC Severity NewsCodes  http://cv.iptc.org/newscodes/severity/
        'severity':  'severity', # type="QCodeType" 
        # Indicates how severe the impact from the signal is - expressed by a URI.
        # The recommended vocabular is the IPTC Severity NewsCodes  http://cv.iptc.org/newscodes/severity/
        'severityuri': 'severityuri' #  type="IRIType" 
    }


class Signal(GenericArray):
    element_class = SignalElement


class AltRepElement(IRIType, CommonPowerAttributes, TimeValidityAttributes, NewsContentTypeAttributes):
    """
    An IRI which, upon dereferencing provides an alternative representation of the Item.
    """
    attributes = {
        # A qualifier which specifies the way the target Item is represented at this location - expressed by a QCode
        'representation': 'representation', # type="QCodeType"
        # A qualifier which specifies the way the target Item is represented at this location - expressed by a URI
        'representationuri': 'representationuri', # type="IRIType"
        # The size in bytes of the target resource.
        'size': 'size'# type="xs:nonNegativeInteger"
    }


class AltRep(GenericArray):
    element_class = AltRepElement


class DeliverableOfElement(Link1Type):
    """
    A reference to the Planning Item under which this item has been published
    """


class DeliverableOf(GenericArray):
    element_class = DeliverableOfElement


class HashElement(CommonPowerAttributes):
    """
    Hash value of parts of an item as defined by the hashscope attribute
    """
    # TODO store xs:string value
    attributes = {
        # The hash algorithm used for creating the hash value - expressed by a QCode
        # either the hashtype or the hashtypeuri attribute MUST be used
        'hashtype': 'hashtype', # type="QCodeType"
        # The hash algorithm used for creating the hash value - expressed by a URI
        # either the hashtype or the hashtypeuri attribute MUST be used
        'hashtypeuri': 'hashtypeuri', # type="IRIType"
        # The scope of a G2 item's content which is the reference for creating the hash value - expressed by a QCode.
        # If the attribute is omitted http://cv.iptc.org/newscodes/hashscope/content is the default value.
        'scope': 'scope', #  type="QCodeType"
        # The scope of a G2 item's content which is the reference for creating the hash value - expressed by a URI.
        # If the attribute is omitted http://cv.iptc.org/newscodes/hashscope/content is the default value.
        'scopeuri': 'scopeuri' # type="IRIType"
    }


class Hash(GenericArray):
    element_class = HashElement


class ExpiresElement(DateOptTimePropType):
    """
    The date and time after which the NewsItem is no longer considered valid by its publisher
    """


class Expires(GenericArray):
    element_class = ExpiresElement


class OrigRepElement(IRIType, CommonPowerAttributes):
    """
    An IRI which, upon dereferencing provides the original representation of the Item, the IRI should be persistent.
    """
    attributes = {
        # A qualifier which indicates the technical variant for accessing this item (e.g. communication protocols) - expressed by a QCode
        'accesstype': 'accesstype', # type="QCodeType">
        # A qualifier which indicates the technical variant for accessing this item (e.g. communication protocols) - expressed by a URI</xs:documentation>
        'accesstypeuri': 'accesstypeuri', # type="IRIType">
        # A qualifier which indicates the role of the stated repository - expressed by a QCode</xs:documentation>
        'reposrole': 'reposrole', # type="QCodeType">
        # A qualifier which indicates the role of the stated repository - expressed by a URI</xs:documentation>
        'reposroleuri': 'reposroleuri' # type="IRIType">
    }


class OrigRep(GenericArray):
    element_class = OrigRepElement


class IncomingFeedIdElement(QCodePropType):
    """
    The identifier of an incoming feed. A feed identifier may be defined by i/ the provider of the feed and/or ii/ the processor of the feed.
    """
    attributes = {
        # A refinement of the semantics of the property - expressed by a QCode
        'role': 'role', # type="QCodeType"
        # A refinement of the semantics of the property - expressed by a URI
        'roleuri': 'roleuri' # type="IRIType"
    }

    
class IncomingFeedId(GenericArray):
    element_class = IncomingFeedIdElement


class MetadataCreatorElement(FlexAuthorPropType):
    """
    Specifies the entity (person, organisation or system) which has edited the metadata properties of this Item; an individual metadata property’s creator may be explicitly overridden using the property's @creator attribute.
    """


class MetadataCreator(GenericArray):
    element_class = MetadataCreatorElement
