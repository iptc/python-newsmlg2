#!/usr/bin/env python

# Simple Types

from .core import NSMAP, NEWSMLG2, BaseObject
from lxml import etree

class DateOptTimeType(BaseObject):
    """
    The type of a date (required) and a time (optional).
    TODO:
    <xs:union memberTypes="xs:date xs:dateTime"/>
    """
    pass


class TruncatedDateTimeType(BaseObject):
    """
    The type of a calendar date with an optional time part
    which may be truncated from the second part to the month part
    XSD definition: <xs:union memberTypes="xs:date xs:dateTime xs:gYearMonth xs:gYear" />
    """
    # store name of the tag used, this can vary
    element_name = None
    # value of the date-time
    date_time = None

    def __init__(self, **kwargs):
        super(TruncatedDateTimeType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.element_name = xmlelement.tag
            self.date_time = xmlelement.text.strip()

    def as_dict(self):
        super(TruncatedDateTimeType, self).as_dict()
        # TODO maybe: convert tag name/element name into camelCase?
        self.dict.update({self.element_name: self.date_time})
        return self.dict


class UnionDateTimeType(BaseObject):
    """
    The base type for approximate dates.</xs:documentation>
    TODO:
    <xs:union memberTypes="xs:dateTime xs:date xs:gYearMonth xs:gYear xs:gMonth xs:gMonthDay xs:gDay"/>
    """


class UnionDateTimeEmptyStringType(BaseObject):
    """
    The base type for dateTimes which may be empty</xs:documentation>
    """
    # value of the date-time
    date_time = None

    def __init__(self, **kwargs):
        super(UnionDateTimeEmptyStringType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.element_name = xmlelement.tag
            self.date_time = xmlelement.text.strip()

    def as_dict(self):
        super(UnionDateTimeEmptyStringType, self).as_dict()
        self.dict.update({self.element_name: self.date_time})
        return self.dict

    def __str__(self):
        return self.date_time

class EmptyStringType(BaseObject):
    """
    The base typ for an empty string
    TODO
          <xs:restriction base="xs:string">
         <xs:length value="0"/>
      </xs:restriction>
    """
    pass

class Int1to9Type(BaseObject):
    """
    The type of an integer in the range 1...9.
    TODO:
          <xs:restriction base="xs:integer">
         <xs:minInclusive value="1"/>
         <xs:maxInclusive value="9"/>
      </xs:restriction>
    """
    pass

class Int100Type(BaseObject):
    """
    The type of an integer in the range 0...100.
    TODO:
          <xs:restriction base="xs:integer">
         <xs:minInclusive value="0"/>
         <xs:maxInclusive value="100"/>
      </xs:restriction>
    """
    pass

class IRIType(BaseObject):
    """
    The type of an Internationalized Resource Identifier Reference, as defined in RFC 3987. Identical to xs : anyURI.
    TODO:
          <xs:restriction base="xs:anyURI"/>
    """
    pass

class IRIListType(BaseObject):
    """
    TODO:
    <xs:simpleType name="IRIListType">
      <xs:list itemType="IRIType"/>
    </xs:simpleType>
    """
    pass

class QCodeType(BaseObject):
    """
    <xs:documentation>The type of a qualified code, i.e. a scheme alias, followed by a colon (“:”), followed by a code. A string of this type cannot contain white space characters. The code may contain colons.</xs:documentation>
    <xs:documentation>The Backus Naur Form (BNF) expression for this is:
&lt;qcode&gt; ::= &lt;scheme&gt; ":" &lt;code&gt;
&lt;scheme&gt; is a string containing any character except white space or the ':' character, required &lt;code&gt; is a string containing any character except white space, required </xs:documentation>
      </xs:annotation>
      <xs:restriction base="xs:string">
         <xs:pattern value="[^\s:]+:[^\s]+"/>
      </xs:restriction>
   </xs:simpleType>
    """
    pass

class QCodeListType(BaseObject):
    """
    The type of space separated strings of QCodes.
    <xs:list itemType="QCodeType"/>
    """
    pass

class G2NormalizedString(BaseObject):
    """
    The type of a string without whitespace except spaces
    TODO:
    <xs:restriction base="xs:string">
        <xs:pattern value="[\S ]*"/>
    </xs:restriction>
    """
    pass
