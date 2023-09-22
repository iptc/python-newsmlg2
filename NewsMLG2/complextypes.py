#!/usr/bin/env python

"""
Datatype components - Complex Types

These can only depend on simpletypes and attributegroups, or we get import loops.
"""

from lxml import etree

from .simpletypes import (
    DateOptTimeType, G2NormalizedString, TruncatedDateTimeType,
    UnionDateTimeType, UnionDateTimeEmptyStringType
)
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, TimeValidityAttributes
)

class DateTimePropType(CommonPowerAttributes):
    """
    The type of a property with date and time
    In XML Schema, extends xsd:dateTime

    TODO add helper methods for date/time manipulation, timezone conversion etc
    """

class DateOptTimePropType(DateOptTimeType, CommonPowerAttributes):
    """
    The type of a property with date and time
    In XML Schema, extends xsd:dateTime
    """


class DateTimeOrNullPropType(UnionDateTimeEmptyStringType, CommonPowerAttributes):
    """
    The type of a property with date and time - or Nothing
    """


class TruncatedDateTimePropType(TruncatedDateTimeType, CommonPowerAttributes):
    """
    The type of a calendar date with an optional time part which
    may be truncated from the seconds part to the month part
    """


class ApproximateDateTimePropType(UnionDateTimeType, CommonPowerAttributes):
    """
    The type of a calendar date with an optional time part and with an optional
    approximation range for the date.
    """

    attributes = {
        # The date (and optionally time) at which the approximation range begins.
        'approxstart': {
            'xml_name': 'approxstart',
        },
        # The date (and optionally the time) at which the approximation range ends.
        'approxend': {
            'xml_name': 'approxend'
        }
    }


class IntlStringType(G2NormalizedString, CommonPowerAttributes, I18NAttributes):
    """
    The type for an internationalized and normalized string, where the language
    and directionality in which the information is written are indirected
    """


class IntlStringType2(CommonPowerAttributes, I18NAttributes):
    """
    The type for an internationalized and unrestricted string, where the language
    and directionality in which the information is writte are indirected
    """


class VersionedStringType(IntlStringType):
    """
    The type extending IntlStringType by a version information
    """

    attributes = {
        # The version of a processing resource.
        'versioninfo': {
            'xml_name': 'versioninfo',
            'xml_type': 'xs:string',
            'use': 'optional'
        }
    }


class ConceptNameType(TimeValidityAttributes, IntlStringType):
    """
    The type of a natural language name for the concept (Type defined in this
    XML Schema only)
    """
    xml_element_name = 'name'
    attributes = {
        # A refinement of the semantics of the name - expressed by a QCode
        'role': {
            'xml_name': 'role'
        },
        # A refinement of the semantics of the name - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri'
        },
        # Specifies which part of a full name this property provides - expressed
        # by a QCode
        'part': {
            'xml_name': 'part'
        },
        # Specifies which part of a full name this property provides - expressed
        # by a URI
        'parturi': {
            'xml_name': 'parturi'
        }
    }

    # TODO this lookup is currently not used...
    _name_role_mappings = {
        # http://cv.iptc.org/newscodes/namerole/
        # http://cv.iptc.org/newscodes/namerole/adjectival
        'nrol:adjectival': 'adjectival',
        # http://cv.iptc.org/newscodes/namerole/alternate
        'nrol:alternate': 'alternate',
        # http://cv.iptc.org/newscodes/namerole/display
        'nrol:display': 'display',
        # http://cv.iptc.org/newscodes/namerole/full
        'nrol:full': 'full',
        # http://cv.iptc.org/newscodes/namerole/mnemonic
        'nrol:mnemonic': 'mnemonic',
        # http://cv.iptc.org/newscodes/namerole/short
        'nrol:short': 'short',
        # http://cv.iptc.org/newscodes/namerole/sort
        'nrol:sort': 'sort',
        # http://cv.iptc.org/newscodes/namerole/synonym
        'nrol:synonym': 'synonym',
        # http://cv.iptc.org/newscodes/namepart/
        # http://cv.iptc.org/newscodes/namepart/acadTitle
        'nprt:acadTitle': 'acadTitle',
        # http://cv.iptc.org/newscodes/namepart/family
        'nprt:family': 'family',
        # http://cv.iptc.org/newscodes/namepart/given
        'nprt:given': 'given',
        # http://cv.iptc.org/newscodes/namepart/middle
        'nprt:middle': 'middle',
        # http://cv.iptc.org/newscodes/namepart/salutation
        'nprt:salutation': 'salutation',
        # these are incorrect but found in SportsML sample files
        'nprt:first': 'given',
        'nrol:first': 'given',
        'nprt:last': 'family',
        'nrol:last': 'family'
    }


class Name(ConceptNameType):
    """
    Instance of ConceptNameType.
    """
