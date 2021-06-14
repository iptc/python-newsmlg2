#!/usr/bin/env python

"""
Properties from xs:group ItemManagementGroup
"""

from .core import BaseObject
from .attributegroups import (
    CommonPowerAttributes, NewsContentTypeAttributes,
    TimeValidityAttributes
)
from .complextypes import (
    DateOptTimePropType, DateTimeOrNullPropType, DateTimePropType,
    VersionedStringType
)
from .concepts import (
    Flex1PropType, FlexAuthorPropType, FlexPartyPropType, QualPropType
)
from .conceptrelationships import QualRelPropType, QCodePropType
from .ids import Hash
from .labeltypes import BlockType
from .link import Link1Type
from .simpletypes import G2NormalizedString, IRIType

class ItemClass(QualRelPropType):
    """
    The nature of the item, set in accordance with the structure of its content.
    """


class Provider(FlexPartyPropType):
    """
    The party (person or organisation) responsible for the management of the Item.
    """


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


class Generator(VersionedStringType):
    """
    The name and version of the software tool used to generate the Item.
    """
    attributes = {
        # Indentifies the stage at which this generator was used - expressed by a QCode
        'role', #  type="QCodeType"
        # Indentifies the stage at which this generator was used - expressed by a URI
        'roleuri' #  type="IRIType"
    }


class Profile(VersionedStringType):
    """
    This property provides information about the structure of an Item,
    e.g. a simple package or an article with one picture.
    """


class Service(QualPropType):
    """
    An editorial service to which an item is assigned by its provider.
    """


class Title(BaseObject):
    """
    A short natural language name for the Item.
    """


class EdNote(BlockType):
    """
    A note addressed to the editorial people receiving the Item.
    """


class MemberOf(Flex1PropType):
    """
    A set of Items around the same theme that this Item is part of.
    """


class InstanceOf(Flex1PropType):
    """
    A frequently updating information object that this Item is an instance of.
    """


class Signal(Flex1PropType):
    """
    An instruction to the processor that the content requires special handling.
    """
    attributes = {
        # Indicates how severe the impact from the signal is -
        # expressed by a QCode.
        # The recommended vocabulary is the IPTC Severity NewsCodes
        # http://cv.iptc.org/newscodes/severity/
        'severity':  'severity', # type="QCodeType"
        # Indicates how severe the impact from the signal is -
        # expressed by a URI.
        # The recommended vocabular is the IPTC Severity NewsCodes
        # http://cv.iptc.org/newscodes/severity/
        'severityuri': 'severityuri' #  type="IRIType"
    }


class AltRep(IRIType, CommonPowerAttributes, TimeValidityAttributes,
    NewsContentTypeAttributes):
    """
    An IRI which, upon dereferencing provides an alternative representation of
    the Item.
    """
    attributes = {
        # A qualifier which specifies the way the target Item is represented at
        # this location - expressed by a QCode
        'representation': 'representation', # type="QCodeType"
        # A qualifier which specifies the way the target Item is represented at
        # this location - expressed by a URI
        'representationuri': 'representationuri', # type="IRIType"
        # The size in bytes of the target resource.
        'size': 'size'# type="xs:nonNegativeInteger"
    }


class DeliverableOf(Link1Type):
    """
    A reference to the Planning Item under which this item has been published
    """


class Expires(DateOptTimePropType):
    """
    The date and time after which the NewsItem is no longer considered valid by its publisher
    """


class OrigRep(IRIType, CommonPowerAttributes):
    """
    An IRI which, upon dereferencing provides the original representation of the
    Item, the IRI should be persistent.
    """
    attributes = {
        # A qualifier which indicates the technical variant for accessing this
        # item (e.g. communication protocols) - expressed by a QCode
        'accesstype': 'accesstype', # type="QCodeType">
        # A qualifier which indicates the technical variant for accessing this
        # item (e.g. communication protocols) - expressed by a URI
        'accesstypeuri': 'accesstypeuri', # type="IRIType">
        # A qualifier which indicates the role of the stated repository -
        # expressed by a QCode
        'reposrole': 'reposrole', # type="QCodeType">
        # A qualifier which indicates the role of the stated repository -
        # expressed by a URI
        'reposroleuri': 'reposroleuri' # type="IRIType">
    }


class IncomingFeedId(QCodePropType):
    """
    The identifier of an incoming feed. A feed identifier may be defined by
    i/ the provider of the feed and/or
    ii/ the processor of the feed.
    """
    attributes = {
        # A refinement of the semantics of the property - expressed by a QCode
        'role': 'role', # type="QCodeType"
        # A refinement of the semantics of the property - expressed by a URI
        'roleuri': 'roleuri' # type="IRIType"
    }


class MetadataCreator(FlexAuthorPropType):
    """
    Specifies the entity (person, organisation or system) which has edited the
    metadata properties of this Item; an individual metadata property’s
    creator may be explicitly overridden using the property's @creator
    attribute.
    """


class ItemManagementGroup(BaseObject):
    """
    A set of properties directly associated with the Item
    """

    elements = {
        'itemclass': {
            'type': 'single',
            'xml_name': 'itemClass',
            'element_class': ItemClass
        },
        'provider': {
            'type': 'single',
            'xml_name': 'provider',
            'element_class': Provider
        },
        'versioncreated': {
            'type': 'single',
            'xml_name': 'versionCreated',
            'element_class': VersionCreated
        },
        'firstcreated': {
            'type': 'single',
            'xml_name': 'firstCreated',
            'element_class': FirstCreated
        },
        'embargoed': {
            'type': 'single',
            'xml_name': 'embargoed',
            'element_class': Embargoed
        },
        'pubstatus': {
            'type': 'single',
            'xml_name': 'pubStatus',
            'element_class': PubStatus
        },
        'role': { 'type': 'single', 'xml_name': 'role', 'element_class': Role },
        'filename': {
            'type': 'single',
            'xml_name': 'fileName',
            'element_class': FileName
        },
        'generator': {
            'type': 'array',
            'xml_name': 'generator',
            'element_class': Generator
        },
        'profile': { 'type': 'single', 'xml_name': 'profile', 'element_class': Profile
        },
        'service': { 'type': 'array', 'xml_name': 'service', 'element_class': Service },
        'title': { 'type': 'array', 'xml_name': 'title', 'element_class': Title },
        'ednote': { 'type': 'array', 'xml_name': 'edNote', 'element_class': EdNote },
        'memberif': {
            'type': 'array',
            'xml_name': 'memberOf',
            'element_class': MemberOf
        },
        'instanceof': {
            'type': 'array',
            'xml_name': 'instanceOf',
            'element_class': InstanceOf
        },
        'signal': { 'type': 'array', 'xml_name': 'signal', 'element_class': Signal },
        'altrep': { 'type': 'array', 'xml_name': 'altRep', 'element_class': AltRep },
        'deliverableof': {
            'type': 'array',
            'xml_name': 'deliverableOf',
            'element_class': DeliverableOf
        },
        'hash': { 'type': 'array', 'xml_name': 'hash', 'element_class': Hash },
        'expires': { 'type': 'array', 'xml_name': 'expires', 'element_class': Expires },
        'origrep': { 'type': 'array', 'xml_name': 'origRep', 'element_class': OrigRep },
        'incomingfeedid': {
            'type': 'array',
            'xml_name': 'incomingFeedId',
            'element_class': IncomingFeedId
        },
        'metadatacreator': {
            'type': 'single',
            'xml_name': 'metadataCreator',
            'element_class': MetadataCreator
        }
    }
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        assert self.itemclass is not None, "itemClass is required in any NewsML-G2 Item"
        assert self.provider is not None, "provider is required in any NewsML-G2 Item"
        assert self.versioncreated is not None, "versionCreated is required in any NewsML-G2 Item"

    def get_itemclass(self):
        """Return QCode for itemclass."""
        return self.get_element_value('itemclass').get_qcode()

    def get_itemclass_uri(self):
        """Return URI for itemclass."""
        return self.get_element_value('itemclass').get_uri()

    def get_provider(self):
        """Return QCode for provider."""
        return self.get_element_value('provider').get_qcode()

    def get_provider_uri(self):
        """Return URI for provider."""
        return self.get_element_value('provider').get_uri()

    def get_pubstatus(self):
        """Return QCode for pubstatus."""
        return self.get_element_value('pubstatus').get_qcode()

    def get_pubstatus_uri(self):
        """Return URI for pubstatus."""
        return self.get_element_value('pubstatus').get_uri()

    def get_service(self):
        """Return QCode for first service in services array."""
        return self.get_element_value('service')[0].get_qcode()

    def get_service_uri(self):
        """Return URI for first service in services array."""
        return self.get_element_value('service')[0].get_uri()

    def get_signal(self):
        """Return QCode for first signal in signals array."""
        return self.get_element_value('signal')[0].get_qcode()

    def get_signal_uri(self):
        """Return URI for first signal in signals array."""
        return self.get_element_value('signal')[0].get_uri()
