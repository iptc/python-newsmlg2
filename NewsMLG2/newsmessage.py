"""
NewsMessage classes

A container to exchange one or more items
"""

from .attributegroups import CommonPowerAttributes, QualifyingAttributes
from .catalog import Catalog, CatalogRef
from .complextypes import DateTimePropType
from .core import BaseObject
from .extensionproperties import Flex2ExtPropType
from .itemmanagement import Signal
from .simpletypes import Int1to9Type

class StringType(CommonPowerAttributes):
    """
    The type of a string value. Type defined in this XML Schema only (ie Newsmessage.xsd)
    """


class Sent(DateTimePropType):
    """
    The date-and-time of transmission of the message
    """


class Sender(StringType, QualifyingAttributes):
    """
    The sender of the items, which may be an organisation or a person
    """


class TransmitId(StringType):
    """
    The transmission identifier associated with the message
    """


class Priority(Int1to9Type, CommonPowerAttributes):
    """
    The priority of this message in the overall transmission process.
    A value of 1 corresponds to the highest priority, a value of 9 to the lowest.
    """


class Origin(StringType, QualifyingAttributes):
    """
    The point of origin of the transmission of this message
    """


class Timestamp(DateTimePropType):
    """
    A date-and-time associated with the message, other than the
    date-and-time the message was sent
    """
    attributes = {
        # A refinement of the semantics of the property.
        # The string value may take a QCode. That the string should be
        # interpreted as a QCode has to be defined outside of the G2
        # specification by the creator of the News Message.
        'role': {
            'xml_name': 'role',
            'xml_type': 'xs:string'
        }
    }


class Destination(StringType, QualifyingAttributes):
    """
    A point of destination for this message.
    """


class Channel(StringType, QualifyingAttributes):
    """
    A transmission channel used by the message
    """
    attributes = {
        # DO NOT USE this attribute, for G2 internal maintenance purposes only.
        'g2flag': {
            'xml_name': 'g2flag',
            'xml_type': 'xs:string',
            'fixed': 'NMSG'
        }
    }


class HeaderExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """


class Header(BaseObject):
    """
    A group of properties providing information about the exchange.
    """ 
    elements = [
        ('sent', {
            'type': 'single',
            'xml_name': 'sent',
            'element_class': Sent
        }),
        ('catalogref', {
            'type': 'array', 'xml_name': 'catalogRef',
            'element_class': CatalogRef
        }),
        ('catalog', {
            'type': 'array', 'xml_name': 'catalog',
            'element_class': Catalog
        }),
        ('sender', {
            'type': 'single', 'xml_name': 'sender',
            'element_class': Sender
        }),
        ('transmitid', {
            'type': 'single', 'xml_name': 'transmitId',
            'element_class': TransmitId
        }),
        ('priority', {
            'type': 'single', 'xml_name': 'priority',
            'element_class': Priority
        }),
        ('origin', {
            'type': 'single', 'xml_name': 'origin',
            'element_class': Origin
        }),
        ('timestamp', {
            'type': 'array', 'xml_name': 'timestamp',
            'element_class': Timestamp
        }),
        ('destination', {
            'type': 'array', 'xml_name': 'destination',
            'element_class': Destination
        }),
        ('channel', {
            'type': 'array', 'xml_name': 'channel',
            'element_class': Channel
        }),
        ('signal', {
            'type': 'array', 'xml_name': 'signal',
            'element_class': Signal
        }),
        ('headerextproperty', {
            'type': 'array', 'xml_name': 'headerExtProperty',
            'element_class': HeaderExtProperty
        })
    ]


class ItemSet(CommonPowerAttributes):
    """
    The set of items to be exchanged.
    (Note: in the XML Schema, this element has an "xs:any" declaration allowing
     any number of elements from the NewsML-G2 spec to be used. We don't yet
     implement xs:any so currently newsMessage is of limited use)
    """


class NewsMessage(BaseObject):
    """
    A container to exchange one or more items
    """
    elements = [
        ('header', {
            'type': 'single',
            'xml_name': 'header',
            'element_class': Header
        }),
        ('itemset', {
            'type': 'single',
            'xml_name': 'itemSet',
            'element_class': ItemSet
        })
    ]
