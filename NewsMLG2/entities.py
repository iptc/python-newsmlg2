#!/usr/bin/env python

"""
Party details - Person and Organisation
"""

from .attributegroups import CommonPowerAttributes, TimeValidityAttributes
from .complextypes import IntlStringType, TruncatedDateTimePropType
from .concepts import (
    Flex1RolePropType, Flex1PropType, FlexLocationPropType,
    FlexOrganisationPropType, Note
)
from .contentmeta import Creator
from .rights import CopyrightNotice
from .simpletypes import IRIType

class Born(TruncatedDateTimePropType):
    """
    The date the person was born.
    """

class Died(TruncatedDateTimePropType):
    """
    The date the person died.
    """


class PersonAffiliationType(FlexOrganisationPropType, TimeValidityAttributes):
    """
    The type for an affliation of a person to an organisation (Type defined in this XML Schema only)
    """


class PersonAffiliation(PersonAffiliationType):
    """
    An affiliation of the person with an organisation.
    """


class ElectronicAddressType(CommonPowerAttributes):
    """
    The type for an electronic address
    """
    attributes = {
        # A refinement of the semantics of the electronic address - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeListType',
            'use': 'optional'
        },
        # A refinement of the semantics of the electronic address - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIListType',
            'use': 'optional'
        }
    }


class ElectronicAddressTechType(CommonPowerAttributes):
    """
    The type for an electronic address with a technical qualifier
    """
    attributes = {
        # A refinement of the semantics of the technical type of the electronic
        # address - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeListType',
            'use': 'optional'
        },
        # A refinement of the semantics of the technical type of the electronic
        # address - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIListType',
            'use': 'optional'
        },
        # The technical variant of the electronic address - expressed by a QCode
        'tech': {
            'xml_name': 'tech',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The technical variant of the electronic address - expressed by a URI
        'techuri': {
            'xml_name': 'techuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        }
    }


class Email(ElectronicAddressType):
    """
    An email address.
    """


class IM(ElectronicAddressTechType):
    """
    An instant messaging address.
    """


class Phone(ElectronicAddressTechType):
    """
    A phone number, preferred in an international format.
    """


class Fax(ElectronicAddressType):
    """
    A fax number, preferred in an international format.
    """


class Web(IRIType, CommonPowerAttributes):
    """
    A web address.
    """
    attributes = {
        # A refinement of the semantics of the web address - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeListType'
        },
        # A refinement of the semantics of the web address - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIListType'
        }
    }


class AddressLine(IntlStringType):
    """
    A line of address information, in the format expected by a recipient postal
    service. City, country area, country and postal code are expressed
    separately.
    """
    attributes = {
        # Refines the semantics of line - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeType'
        },
        # Refines the semantics of line - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIType'
        }
    }


class Area(Flex1RolePropType):
    """
    A subdivision of a country part of the address.
    """


class PostalCode(IntlStringType):
    """
    A postal code part of the address.
    """


class Country(Flex1PropType):
    """
    A country part of the address.
    """


class Locality(Flex1RolePropType):
    """
    A city/town/village etc. part of the address.
    """


class WorldRegion(Flex1PropType):
    """
    A concept or name only defining the world region part of an address.
    """

class Address(CommonPowerAttributes):
    """
    A postal address for the location of a Point Of Interest
    """
    elements = [
        ('line', {
            'type': 'array', 'xml_name': 'line', 'element_class': AddressLine
        }),
        ('worldregion', {
            'type': 'single', 'xml_name': 'worldRegion',
            'element_class': WorldRegion
        }),
        ('locality', {
            'type': 'array', 'xml_name': 'locality', 'element_class': Locality
        }),
        ('area', {
            'type': 'array', 'xml_name': 'area', 'element_class': Area
        }),
        ('country', {
            'type': 'single', 'xml_name': 'country', 'element_class': Country
        }),
        ('postalcode', {
            'type': 'single', 'xml_name': 'postalCode',
            'element_class': PostalCode
        })
    ]
    attributes = {
        # A refinement of the semantics of the postal address - expressed by
        # a QCode
        'role': {
            'xml_name': 'role'
        },
        # A refinement of the semantics of the postal address - expressed by
        # a URI
        'roleuri': {
            'xml_name': 'roleuri'
        }
    }


class ContactInfoType(CommonPowerAttributes):
    """
    The type for information to get in contact with a party
    (Type defined in this XML Schema only)
    """
    elements = [
        ('email', { 'type': 'array', 'xml_name': 'email', 'element_class': Email }),
        ('im', { 'type': 'array', 'xml_name': 'im', 'element_class': IM }),
        ('phone', { 'type': 'array', 'xml_name': 'phone', 'element_class': Phone }),
        ('fax', { 'type': 'array', 'xml_name': 'fax', 'element_class': Fax }),
        ('web', { 'type': 'array', 'xml_name': 'web', 'element_class': Web }),
        ('address', { 'type': 'array', 'xml_name': 'address', 'element_class': Address }),
        ('note', { 'type': 'array', 'xml_name': 'note', 'element_class': Note })
    ]
    attributes = {
        # A refinement of the semantics of a contact information - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeListType',
            'use': 'optional'
        },
        # A refinement of the semantics of a contact information - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIListType',
            'use': 'optional'
        }
    }


class ContactInfo(ContactInfoType):
    """
    Information how to contact the person.
    """


class PersonDetails(CommonPowerAttributes):
    """
    A set of properties specific to a person
    """

    elements = [
        ('born', { 'type': 'single', 'xml_name': 'born', 'element_class': Born }),
        ('died', { 'type': 'single', 'xml_name': 'died', 'element_class': Died }),
        ('affiliation', {
            'type': 'array', 'xml_name': 'affiliation',
            'element_class': PersonAffiliation
        }),
        ('contactinfo', {
            'type': 'array', 'xml_name': 'contactInfo',
            'element_class': ContactInfo
        })
    ]


class OrganisationFounded(TruncatedDateTimePropType):
    """
    The date the organisation was founded/established.
    """
    xml_element_name = 'founded'


class OrganisationDissolved(TruncatedDateTimePropType):
    """
    The date the organisation was dissolved.
    """
    xml_element_name = 'dissolved'


class OrganisationLocation(FlexLocationPropType):
    """
    A place where the organisation is located.
    """
    xml_element_name = 'location'


class OrganisationAffiliationType(FlexOrganisationPropType, TimeValidityAttributes):
    """
    The type for an affliation of an organisation to another organisation
    (Type defined in this XML Schema only)
    """


class OrganisationAffiliation(OrganisationAffiliationType):
    """
    An affiliation of the organisation with another organisation.
    """
    xml_element_name = 'affiliation'


class HasInstrument(CommonPowerAttributes):
    """
    Defines a financial instrument which is related to a company
    """
    attributes = {
        # A symbol for the financial instrument
        'symbol': {
            'xml_name': 'symbol',
            'xml_type': 'xs:string',
            'use': 'required'
        },
        # The  source of the financial instrument symbol - expressed by a QCode
        'symbolsrc': {
            'xml_name': 'symbolsrc',
            'xml_type': 'QCodeType'
        },
        # The  source of the financial instrument symbol - expressed by a URI
        'symbolsrcuri': {
            'xml_name': 'symbolsrcuri',
            'xml_type': 'IRIType'
        },
        # A venue in which this financial instrument is traded - expressed by a QCode
        'market': {
            'xml_name': 'market',
            'xml_type': 'QCodeType'
        },
        # A venue in which this financial instrument is traded - expressed by a URI
        'marketuri': {
            'xml_name': 'marketuri',
            'xml_type': 'IRIType'
        },
        # The label used for the market
        'marketlabel': {
            'xml_name': 'marketlabel',
            'xml_type': 'xs:string'
        },
        # The source of the market label - expressed by a QCode
        'marketlabelsrc': {
            'xml_name': 'marketlabelsrc',
            'xml_type': 'QCodeType'
        },
        # The source of the market label - expressed by a URI
        'marketlabelsrcuri': {
            'xml_name': 'marketlabelsrcuri',
            'xml_type': 'IRIType'
        },
        # The type(s) of the financial instrument - expressed by a QCode
        'type': {
            'xml_name': 'type',
            'xml_type': 'QCodeListType'
        },
        # The type(s) of the financial instrument - expressed by a URI
        'typeuri': {
            'xml_name': 'typeuri',
            'xml_type': 'IRIListType'
        },
        # Indicates the relative importance among financial instruments of the same type.
        'rank': {
            'xml_name': 'rank',
            'xml_type': 'xs:nonNegativeInteger'
        }
    }

class OrganisationDetails(CommonPowerAttributes):
    """
    A group of properties specific to an organisation
    """

    elements = [
        ('founded', {
            'type': 'single', 'xml_name': 'founded',
            'element_class': OrganisationFounded
        }),
        ('dissolved', {
            'type': 'single', 'xml_name': 'dissolved',
            'element_class': OrganisationDissolved
        }),
        ('location', {
            'type': 'array', 'xml_name': 'location',
            'element_class': OrganisationLocation
        }),
        ('affiliation', {
            'type': 'array', 'xml_name': 'affiliation',
            'element_class': OrganisationAffiliation
        }),
        ('contactinfo', {
            'type': 'array', 'xml_name': 'contactInfo',
            'element_class': ContactInfo
        }),
        # deprecated in NewsML-G2 2.31 but still allowed
        ('hasinstrument', {
            'type': 'array', 'xml_name': 'hasInstrument',
            'element_class': HasInstrument,
            'status': 'deprecated'
        })
    ]


class ObjectCreated(TruncatedDateTimePropType):
    """
    The date (and optionally the time) on which this object was created
    """


class ObjectCeasedToExist(TruncatedDateTimePropType):
    """
    The date (and optionally the time) on which this object ceased to exist.
    """


class ObjectDetails(CommonPowerAttributes):
    """
    A group of properties specific to an object
    """

    elements = [
        ('created', {
            'type': 'single', 'xml_name': 'created',
            'element_class': ObjectCreated
        }),
        ('copyrightnotice', {
            'type': 'array', 'xml_name': 'copyrightNotice',
            'element_class': CopyrightNotice
        }),
        ('creator', {
            'type': 'array', 'xml_name': 'creator',
            'element_class': Creator
        }),
        ('ceasedtoexist', {
            'type': 'single', 'xml_name': 'ceasedToExist',
            'element_class': ObjectCeasedToExist
        })
    ]
