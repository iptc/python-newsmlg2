#!/usr/bin/env python

"""
Datatype components - Complex Types

These can only depend on simpletypes and attributegroups, or we get import loops.
"""

from lxml import etree

from .simpletypes import (
    DateOptTimeType, G2NormalizedString, UnionDateTimeType, UnionDateTimeEmptyStringType
)
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes
)

class DateTimePropType(CommonPowerAttributes):
    """
    The type of a property with date and time
    In XML Schema, extends xsd:dateTime
    """

    def __init__(self, **kwargs):
        super(DateTimePropType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.datetime = kwargs['xmlelement'].text.strip()

    def __str__(self):
        return self.datetime

    def get_datetime(self):
        return self.datetime

    # TODO add helper methods for date/time manipulation, timezone conversion etc
    pass

class DateOptTimePropType(DateOptTimeType, CommonPowerAttributes):
    """
    The type of a property with date and time
    In XML Schema, extends xsd:dateTime
    """

    pass

class DateTimeOrNullPropType(UnionDateTimeEmptyStringType, CommonPowerAttributes):
    """
    The type of a property with date and time - or Nothing
    """
    pass

class TruncatedDateTimePropType(CommonPowerAttributes):
    """
    The type of a calendar date with an optional time part which
    may be truncated from the seconds part to the month part
    """
    pass
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
    pass


class IntlStringType2(str, CommonPowerAttributes, I18NAttributes):
    """
    The type for an internationalized and unrestricted string, where the language
    and directionality in which the information is writte are indirected
    """
    pass

class VersionedStringType(IntlStringType):
    """
    The type extending IntlStringType by a version information
    """
    attributes = {
        # The version of a processing resource.
        'versioninfo': 'versioninfo'  # type="xs:string" use="optional">
    }
