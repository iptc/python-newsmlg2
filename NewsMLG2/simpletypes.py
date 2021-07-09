#!/usr/bin/env python

"""
Simple Types, used throughout the schema
"""

from lxml import etree

from .core import BaseObject


class DateOptTimeType(BaseObject):
    """
    The type of a date (required) and a time (optional).
    TODO: validation
    <xs:union memberTypes="xs:date xs:dateTime"/>
    """


class TruncatedDateTimeType(BaseObject):
    """
    The type of a calendar date with an optional time part
    which may be truncated from the second part to the month part
    XSD definition: <xs:union memberTypes="xs:date xs:dateTime xs:gYearMonth xs:gYear" />
    """
    # store name of the tag used, this can vary
    _element_name = None
    # value of the date-time
    _date_time = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            self._element_name = xmlelement.tag
            self._date_time = xmlelement.text.strip()


class UnionDateTimeType(BaseObject):
    """
    The base type for approximate dates.
    TODO: validation
    <xs:union memberTypes="xs:dateTime xs:date xs:gYearMonth xs:gYear xs:gMonth xs:gMonthDay xs:gDay"/>
    """


class UnionDateTimeEmptyStringType(BaseObject):
    """
    The base type for dateTimes which may be empty
    """
    # value of the date-time
    date_time = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            self._element_name = xmlelement.tag
            self._date_time = xmlelement.text.strip()

    def __str__(self):
        return self._date_time


class EmptyStringType(BaseObject):
    """
    The base typ for an empty string
    TODO: validation
      <xs:restriction base="xs:string">
         <xs:length value="0"/>
      </xs:restriction>
    """


class Int1to9Type(BaseObject):
    """
    The type of an integer in the range 1...9.
    TODO: validation
      <xs:restriction base="xs:integer">
         <xs:minInclusive value="1"/>
         <xs:maxInclusive value="9"/>
      </xs:restriction>
    """


class Int100Type(BaseObject):
    """
    The type of an integer in the range 0...100.
    TODO: validation
      <xs:restriction base="xs:integer">
         <xs:minInclusive value="0"/>
         <xs:maxInclusive value="100"/>
      </xs:restriction>
    """


class IRIType(BaseObject):
    """
    The type of an Internationalized Resource Identifier Reference, as defined
    in RFC 3987. Identical to xs:anyURI.

    TODO: validation
      <xs:restriction base="xs:anyURI"/>
    """


class IRIListType(BaseObject):
    """
    TODO: validation
    <xs:simpleType name="IRIListType">
      <xs:list itemType="IRIType"/>
    </xs:simpleType>
    """


class QCodeType(BaseObject):
    """
    The type of a qualified code, i.e. a scheme alias, followed by a colon
    (“:”), followed by a code. A string of this type cannot contain white
    space characters. The code may contain colons.
    The Backus Naur Form (BNF) expression for this is:
    <qcode> ::= <scheme> ":" <code>
    <scheme> is a string containing any character except white space or the ':'
    character, required <code> is a string containing any character except
    white space, required

    TODO: validation
      <xs:restriction base="xs:string">
         <xs:pattern value="[^\s:]+:[^\s]+"/>
      </xs:restriction>
   </xs:simpleType>
    """


class QCodeListType(BaseObject):
    """
    The type of space separated strings of QCodes.

    TODO: validation
    <xs:list itemType="QCodeType"/>
    """


class G2NormalizedString(BaseObject):
    """
    The type of a string without whitespace except spaces

    TODO: validation
    <xs:restriction base="xs:string">
        <xs:pattern value="[\S ]*"/>
    </xs:restriction>
    """
