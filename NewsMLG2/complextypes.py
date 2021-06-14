#!/usr/bin/env python

"""
Datatype components - Complex Types

These can only depend on simpletypes and attributegroups, or we get import loops.
"""

from lxml import etree

from .core import GenericArray
from .simpletypes import (
    DateOptTimeType, G2NormalizedString, UnionDateTimeType,
    UnionDateTimeEmptyStringType
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

#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        xmlelement = kwargs.get('xmlelement')
#        if isinstance(xmlelement, etree._Element):
#            self.datetime = kwargs['xmlelement'].text.strip()
#
#    def __str__(self):
#        return self.datetime
#
#    def get_datetime(self):
#        return self.datetime


class DateOptTimePropType(DateOptTimeType, CommonPowerAttributes):
    """
    The type of a property with date and time
    In XML Schema, extends xsd:dateTime
    """


class DateTimeOrNullPropType(UnionDateTimeEmptyStringType, CommonPowerAttributes):
    """
    The type of a property with date and time - or Nothing
    """


class TruncatedDateTimePropType(CommonPowerAttributes):
    """
    The type of a calendar date with an optional time part which
    may be truncated from the seconds part to the month part
    """

    """
            <xs:extension base="TruncatedDateTimeType">
                <xs:attributeGroup ref="commonPowerAttributes" />
                <xs:anyAttribute namespace="##other" processContents="lax" />
            </xs:extension>
    """


class ApproximateDateTimePropType(UnionDateTimeType, CommonPowerAttributes):
    """
    The type of a calendar date with an optional time part and with an optional approximation range for the date.
    """

    attributes = {
        # The date (and optionally time) at which the approximation range begins.
        'approxstart': 'approxstart',
        # The date (and optionally the time) at which the approximation range ends.
        'approxend': 'approxend'
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
        'versioninfo': 'versioninfo'  # type="xs:string" use="optional">
    }


class ConceptNameType(TimeValidityAttributes, IntlStringType):
    """
    The type of a natural language name for the concept (Type defined in this
    XML Schema only)
    """
    xml_element_name = 'name'
    name = None
    attributes = {
        # A refinement of the semantics of the name - expressed by a QCode
        'role': 'role',
        # A refinement of the semantics of the name - expressed by a URI
        'roleuri': 'roleuri',
        # Specifies which part of a full name this property provides - expressed
        # by a QCode
        'part': 'part',
        # Specifies which part of a full name this property provides - expressed
        # by a URI
        'parturi': 'parturi'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            self.name = xmlelement.text.strip()

    name_role_mappings = {
        # http://cv.iptc.org/newscodes/namerole/
        # http://cv.iptc.org/newscodes/namerole/adjectival
        'nrol:adjectival': 'adjectival',
        'nrol:alternate': 'alternate',    # http://cv.iptc.org/newscodes/namerole/alternate
        'nrol:display': 'display',        # http://cv.iptc.org/newscodes/namerole/display
        'nrol:full': 'full',              # http://cv.iptc.org/newscodes/namerole/full
        'nrol:mnemonic': 'mnemonic',      # http://cv.iptc.org/newscodes/namerole/mnemonic
        'nrol:short': 'short',            # http://cv.iptc.org/newscodes/namerole/short
        'nrol:sort': 'sort',              # http://cv.iptc.org/newscodes/namerole/sort
        'nrol:synonym': 'synonym',        # http://cv.iptc.org/newscodes/namerole/synonym
        # http://cv.iptc.org/newscodes/namepart/
        'nprt:acadTitle': 'acadTitle',    # http://cv.iptc.org/newscodes/namepart/acadTitle
        'nprt:family': 'family',          # http://cv.iptc.org/newscodes/namepart/family
        'nprt:given': 'given',            # http://cv.iptc.org/newscodes/namepart/given
        'nprt:middle': 'middle',          # http://cv.iptc.org/newscodes/namepart/middle
        # http://cv.iptc.org/newscodes/namepart/salutation
        'nprt:salutation': 'salutation',
        # temporary hacks while we decide what to fix
        'nprt:first': 'given',
        'nrol:first': 'given',
        'nprt:last': 'family',
        'nrol:last': 'family',
    }

    def as_dict(self):
        super().as_dict()
        # the only place where we diverge from a direct match with the schema
        role = self.attr_values.get('role', None)
        part = self.attr_values.get('part', None)
        if role and role in self.name_role_mappings.keys():
            self.dict.update({
                self.name_role_mappings[role]: self.name or ""
            })
            del self.dict['role']
        elif part and part in self.name_role_mappings.keys():
            self.dict.update({
                self.name_role_mappings[part]: self.name or ""
            })
            del self.dict['part']
        # elif self.name:
        else:
            self.dict.update({'name': self.name or ""})
        return self.dict

    def __str__(self):
        return self.name


class Name(ConceptNameType):
    """
    Instance of ConceptNameType.
    """
