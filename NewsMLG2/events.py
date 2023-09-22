#!/usr/bin/env python

"""
Handle elements originally created for EventsML-G2 and merged
in to NewsML-G2 in NAR version 1.8
"""

from .core import BaseObject
from .attributegroups import (
    CommonPowerAttributes, ConfirmationStatusAttributes
)
from .complextypes import (
    ApproximateDateTimePropType, DateOptTimePropType, Name
)
from .concepts import (
    Definition, Flex1ConceptPropType, Flex1PartyPropType, Flex1PropType, FlexLocationPropType, Note, QualPropType
)
from .conceptrelationships import (
    ConceptRelationshipsGroup, Facet, QCodePropType
)
from .contentmeta import (
    DescriptiveMetadataGroup, Keyword, Language
)
from .entities import ContactInfoType
from .itemmanagement import (
    EdNote, ItemClass
)
from .labeltypes import BlockType
from .planningitem import (
    AssignedTo, G2ContentType, Scheduled, Service
)


class RecurrenceRuleAttributes(BaseObject):
    """
    A group of attributes aligning with iCalendar RECUR - see http://www.ietf.org/rfc/rfc2445.txt
    """
    attributes = {
        # The FREQ rule part identifies the type of recurrence rule.
        'freq': {
            'xml_name': 'freq',
            'xml_type': 'xs:string',
            'use': 'required'
            # TODO enumeration:
            #   <xs:enumeration value="SECONDLY"/>
            #   <xs:enumeration value="MINUTELY"/>
            #   <xs:enumeration value="HOURLY"/>
            #   <xs:enumeration value="DAILY"/>
            #   <xs:enumeration value="WEEKLY"/>
            #   <xs:enumeration value="MONTHLY"/>
            #   <xs:enumeration value="YEARLY"/>
        },
        # The INTERVAL rule part contains a positive integer representing how
        # often the recurrence rule repeats.
        'interval': {
            'xml_name': 'interval',
            'xml_type': 'xs:positiveInteger'
        },
        # The UNTIL rule part defines a date-time value which bounds the
        # recurrence rule in an inclusive manner.
        'until': {
            'xml_name': 'until',
            'xml_type': 'DateOptTimeType'
        },
        # The COUNT rule part defines the number of occurrences at which to
        # range-bound the recurrence.
        'count': {
            'xml_name': 'count',
            'xml_type': 'xs:positiveInteger'
        },
        # The BYSECOND rule part specifies a space separated list of seconds within a minute
        'bysecond': {
            'xml_name': 'bysecond'
            # TODO 
            # <xs:restriction base="BySecondListType">
            #    <xs:minLength value="1"/>
            # </xs:restriction>
            #
            # BySecondListType:
            # <xs:restriction base="xs:nonNegativeInteger">
            #   <xs:minInclusive value="0"/>
            #   <xs:maxInclusive value="59"/>
            # </xs:restriction>
        },
        # The BYMINUTE rule part specifies a space separated list of minutes within an hour.
        'byminute': {
            'xml_name': 'byminute'
            # TODO
            # <xs:restriction base="ByMinuteListType">
            #    <xs:minLength value="1"/>
            # </xs:restriction>
            #
            # ByMinuteListType:
            # <xs:restriction base="xs:nonNegativeInteger">
            #    <xs:minInclusive value="0"/>
            #    <xs:maxInclusive value="59"/>
            # </xs:restriction>
        },
        # The BYHOUR rule part specifies space separated list of hours of the day.
        'byhour': {
            'xml_name': 'byhour',
            # TODO
            # <xs:restriction base="ByHourListType">
            #    <xs:minLength value="1"/>
            # </xs:restriction>
            #
            # ByHourListType:
            # <xs:restriction base="xs:nonNegativeInteger">
            #    <xs:minInclusive value="0"/>
            #    <xs:maxInclusive value="23"/>
            # </xs:restriction>
        },
        # The BYDAY rule part specifies a space separated list of days of the week
        'byday': {
            'xml_name': 'byday',
            # TODO
            # <xs:restriction base="ByDayListType">
            #    <xs:minLength value="1"/>
            # </xs:restriction>
            #
            # ByDayListType:
            # <xs:restriction base="xs:string">
            #    <xs:pattern value="(\-|\+)?([0-9]){0,2}(MO|TU|WE|TH|FR|SA|SU)"/>
            # </xs:restriction>
        },
        # The BYMONTHDAY rule part specifies a space separated list of days of the month.
        'bymonthday': {
            'xml_name': 'bymonthday',
            # TODO
            # <xs:restriction base="ByMonthDayListType">
            #    <xs:minLength value="1"/>
            # </xs:restriction>
            #
            # ByMonthDayListType:
            # <xs:union>
            #    <xs:simpleType>
            #       <xs:annotation>
            #          <xs:documentation>bymonthdayPosType</xs:documentation>
            #          <xs:documentation>Helper datatype for bymonthdayListType</xs:documentation>
            #       </xs:annotation>
            #       <xs:restriction base="xs:integer">
            #          <xs:minInclusive value="1"/>
            #          <xs:maxInclusive value="31"/>
            #       </xs:restriction>
            #    </xs:simpleType>
            #       </xs:restriction>
            #    </xs:simpleType>
            #    <xs:simpleType>
            #       <xs:annotation>
            #          <xs:documentation>bymonthdayNegType</xs:documentation>
            #          <xs:documentation>Helper datatype for bymonthdayListType</xs:documentation>
            #       </xs:annotation>
            #       <xs:restriction base="xs:integer">
            #          <xs:minInclusive value="-31"/>
            #          <xs:maxInclusive value="-1"/>
            #       </xs:restriction>
            #    </xs:simpleType>
            # </xs:union>
        },
        # The BYMONTH rule part specifies a space separated list of months of the year.
        'bymonth': {
            'xml_name': 'bymonth',
            # TODO
            # <xs:restriction base="ByMonthListType">
            #    <xs:minLength value="1"/>
            # </xs:restriction>
            #
            # ByMonthListType:
            # <xs:restriction base="xs:nonNegativeInteger">
            #    <xs:minInclusive value="1"/>
            #    <xs:maxInclusive value="12"/>
            # </xs:restriction>
        },
        # The BYYEARDAY rule part specifies a  space separated list of days of
        # the year.
        'byyearday': {
            'xml_name': 'byyearday',
            # TODO
            # <xs:restriction base="ByYearDayListType">
            #    <xs:minLength value="1"/>
            # </xs:restriction>
            #
            # ByYearDayListType:
            # <xs:union>
            #    <xs:simpleType>
            #       <xs:restriction base="xs:integer">
            #          <xs:minInclusive value="1"/>
            #          <xs:maxInclusive value="366"/>
            #       </xs:restriction>
            #    </xs:simpleType>
            #    <xs:simpleType>
            #       <xs:restriction base="xs:integer">
            #          <xs:minInclusive value="-366"/>
            #          <xs:maxInclusive value="-1"/>
            #       </xs:restriction>
            #    </xs:simpleType>
            # </xs:union>
        },
        # The BYWEEKNO rule part specifies a space separated list of ordinals
        # specifying weeks of the year.
        'byweekno': {
            'xml_name': 'byyearday',
            # TODO
            # <xs:restriction base="ByWeekNoListType">
            #    <xs:minLength value="1"/>
            # </xs:restriction>
            #
            # ByWeekNoListType:
            # <xs:union>
            #    <xs:simpleType>
            #       <xs:restriction base="xs:integer">
            #         <xs:minInclusive value="1"/>
            #         <xs:maxInclusive value="53"/>
            #       </xs:restriction>
            #    </xs:simpleType>
            #    <xs:simpleType>
            #       <xs:restriction base="xs:integer">
            #          <xs:minInclusive value="-53"/>
            #          <xs:maxInclusive value="-1"/>
            #       </xs:restriction>
            #    </xs:simpleType>
            # </xs:union>
        },
        # The BYSETPOS rule part specifies a space separated list of values
        # which corresponds to the nth occurrence within the set of events
        # specified by the rule.
        'bysetpos': {
            'xml_name': 'bysetpos',
            # TODO
            # <xs:restriction base="BySetposListType">
            #    <xs:minLength value="1"/>
            # </xs:restriction>
            #
            # BySetposListType:
            # <xs:union>
            #    <xs:simpleType>
            #       <xs:restriction base="xs:integer">
            #          <xs:minInclusive value="1"/>
            #          <xs:maxInclusive value="366"/>
            #       </xs:restriction>
            #    </xs:simpleType>
            #    <xs:simpleType>
            #       <xs:restriction base="xs:integer">
            #          <xs:minInclusive value="-366"/>
            #          <xs:maxInclusive value="-1"/>
            #       </xs:restriction>
            #    </xs:simpleType>
            # </xs:union>
        },
        # The WKST rule part specifies the day on which the workweek starts.
        'wkst': {
            'xml_name': 'wkst',
            'xml_type': 'xs:string',
            # TODO
            #   <xs:enumeration value="MO"/>
            #   <xs:enumeration value="TU"/>
            #   <xs:enumeration value="WE"/>
            #   <xs:enumeration value="TH"/>
            #   <xs:enumeration value="FR"/>
            #   <xs:enumeration value="SA"/>
            #   <xs:enumeration value="SU"/>
        }
    }


class RDate(DateOptTimePropType):
    """
    Explicit dates of recurrence.
    """

class RRule(CommonPowerAttributes, RecurrenceRuleAttributes):
    """
    Rule for recurrence.
    """

class ExDate(DateOptTimePropType):
    """
    Explicit dates to be excluded from any recurrence.
    """
 
class ExRule(CommonPowerAttributes, RecurrenceRuleAttributes):
    """
    Rule for dates to be excluded from recurrence.
    """


# A group of elements to express a recurrence
RecurrenceGroup = [
    # TODO require that there is at least one rDate or rRule element present
    ('rdate', { 
        'type': 'array', 'xml_name': 'rDate', 'element_class': RDate
    }),
    ('rrule', { 
        'type': 'array', 'xml_name': 'rRule', 'element_class': RRule
    }),
    ('exdate', { 
        'type': 'array', 'xml_name': 'exDate', 'element_class': ExDate
    }),
    ('exrule', { 
        'type': 'array', 'xml_name': 'exRule', 'element_class': ExRule
    })
]


class Start(ApproximateDateTimePropType, ConfirmationStatusAttributes):
    """
    The date the event commences.
    """


class End(ApproximateDateTimePropType, ConfirmationStatusAttributes):
    """
    The date the event ends.
    """


class Duration(CommonPowerAttributes, ConfirmationStatusAttributes):
    """
    The period the event will last.
    TODO base data type is xs:duration
    """


class Confirmation(QCodePropType):
    """
    DEPRECATED in NewsML-G2 2.24 and higher; use the @confirmationstatus
    or @confirmationstatusuri attributes on start, end and/or duration as
    required.
    (was: flags to indicate if start and/or end date and times are confirmed.)
    """

class Dates(CommonPowerAttributes):
    """
    All dates pertaining to the event, in particular the start and end date and any recurrence information
    """
    elements = [ 
        ('start', { 
            'type': 'single', 'xml_name': 'start', 'element_class': Start
        }),
        # TODO end and duration are mutually exclusive (defined as xs:choice in the schema)
        ('end', { 
            'type': 'single', 'xml_name': 'end', 'element_class': End
        }),
        ('duration', { 
            'type': 'single', 'xml_name': 'duration', 'element_class': Duration
        })
        ] + RecurrenceGroup + [
        ('confirmation', { 
            'type': 'single', 'xml_name': 'confirmation', 'element_class': Confirmation
        })
    ]
        

class OccurStatus(QualPropType):
    """
    Indicates the certainty of the occurrence of the event
    """

class NewsCoverageStatus(QualPropType):
    """
    The planning of the news coverage of the event
    """

class Registration(BlockType):
    """
    How and when to register for the event. Could also include information
    about cost, and so on. May also hold accreditation information
    """


class AccessStatus(QualPropType):
    """
    Indication of the accessibility of the event
    """


class ParticipationRequirement(Flex1PropType):
    """
    A requirement for participating in the event
    """
    attributes = {
        # Refinement of the semantics of the property - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeType'
        },
        # Refinement of the semantics of the property - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIType'
        }
    }


class EventDetailsSubject(Flex1ConceptPropType):
    """
    A subject covered by the event.
    """
    xml_element_name = 'subject'


class EventDetailsLocation(FlexLocationPropType):
    """
    A location (geographical area or point of interest) where the event takes place
    """
    attributes = {
        # Refinement of the semantics of the property - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeType'
        },
        # Refinement of the semantics of the property - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIType'
        }
    }


class Participant(Flex1PartyPropType):
    """
    A person or organisation (e.g. group of artists) participating in the event.
    """


class Organiser(Flex1PartyPropType):
    """
    A person or organisation organising the event.
    """


class ContactInfo(ContactInfoType):
    """
    Primary information for the public to get in contact with the event.
    """


class NewsCoverage(BaseObject):
    """
    (LEGACY, see spec document) Structured and textual information about the
    intended coverage by the news provider of this event information. This
    information is aimed at the editorial staff of the receiver.
    """
    elements = [
        ('g2contentType', { 
            'type': 'single', 'xml_name': 'g2contentType', 'element_class': G2ContentType
        }),
        # TODO end and duration are mutually exclusive (defined as xs:choice in the schema)
        ('itemclass', { 
            'type': 'single', 'xml_name': 'itemClass', 'element_class': ItemClass
        }),
        ('assignedto', { 
            'type': 'array', 'xml_name': 'assignedTo', 'element_class': AssignedTo
        }),
        ('scheduled', { 
            'type': 'single', 'xml_name': 'scheduled', 'element_class': Scheduled
        }),
        ('service', { 
            'type': 'array', 'xml_name': 'service', 'element_class': Service
        }),
        ('ednote', { 
            'type': 'array', 'xml_name': 'edNote', 'element_class': EdNote
        })
    ] + DescriptiveMetadataGroup

    attributes = {
        # Refinement of the semantics of the property - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeType'
        },
        # Refinement of the semantics of the property - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIType'
        }
    }


class EventDetails(CommonPowerAttributes):
    """
    A set of properties with details about an event (Used in the scope of EventsML-G2)
    """
    elements = [ 
        ('dates', { 
            'type': 'single', 'xml_name': 'dates', 'element_class': Dates
        }),
        ('occurstatus', { 
            'type': 'single', 'xml_name': 'occurStatus', 'element_class': OccurStatus
        }),
        ('newscoveragestatus', { 
            'type': 'single', 'xml_name': 'newsCoverageStatus', 'element_class': NewsCoverageStatus
        }),
        ('registration', { 
            'type': 'array', 'xml_name': 'registration', 'element_class': Registration
        }),
        ('keyword', { 
            'type': 'array', 'xml_name': 'keyword', 'element_class': Keyword
        }),
        ('accessstatus', { 
            'type': 'array', 'xml_name': 'accessStatus', 'element_class': AccessStatus
        }),
        ('participationrequirement', { 
            'type': 'array', 'xml_name': 'participationRequirement', 'element_class': ParticipationRequirement
        }),
        ('subject', { 
            'type': 'array', 'xml_name': 'subject', 'element_class': EventDetailsSubject
        }),
        ('location', { 
            'type': 'array', 'xml_name': 'location', 'element_class': EventDetailsLocation
        }),
        ('participant', { 
            'type': 'array', 'xml_name': 'participant', 'element_class': Participant
        }),
        ('organiser', { 
            'type': 'array', 'xml_name': 'organiser', 'element_class': Organiser
        }),
        ('contactinfo', { 
            'type': 'array', 'xml_name': 'contactInfo', 'element_class': ContactInfo
        }),
        ('language', { 
            'type': 'array', 'xml_name': 'language', 'element_class': Language
        }),
        ('newscoverage', { 
            'type': 'array', 'xml_name': 'newsCoverage', 'element_class': NewsCoverage
        })
    ]


class Event(CommonPowerAttributes):
    """
    Structured information about an event without a concept identifier, to be
    used only with News Items
    """
    elements = [
        ('name', { 
            'type': 'array', 'xml_name': 'name', 'element_class': Name,
            # TODO currently 'use': 'required' for elements has no effect
            'use': 'required' # minOccurs = 1
        }),
        ('definition', { 
            'type': 'array', 'xml_name': 'definition', 'element_class': Definition
        }),
        ('note', { 
            'type': 'array', 'xml_name': 'note', 'element_class': Note
        }),
        ('facet', { 
            'type': 'array', 'xml_name': 'facet', 'element_class': Facet
        })
    ] + ConceptRelationshipsGroup + [
        ('eventdetails', { 
            'type': 'single', 'xml_name': 'eventDetails', 'element_class': EventDetails
        })
    ]


class Events(CommonPowerAttributes):
    """
    A wrapper for events in a News Item.
    """
    elements = [
        ('event', { 
            'type': 'array', 'xml_name': 'event', 'element_class': Event,
            # TODO currently 'use': 'required' for elements has no effect
            'use': 'required' # minOccurs = 1
        })
    ]
