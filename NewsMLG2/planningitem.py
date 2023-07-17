"""
Planning Item
"""

from .anyitem import (
    AnyItem, Assert, DerivedFrom, DerivedFromValue, InlineRef
)
from .attributegroups import (
    CommonPowerAttributes, NewsContentTypeAttributes, NewsContentCharacteristics
)
from .complextypes import ApproximateDateTimePropType
from .concepts import Flex1PartyPropType, QualPropType
from .contentmeta import (
    Audience, ContentMetadataAcDType, DescriptiveMetadataGroup, ExclAudience, Urgency
)
from .core import BaseObject
from .extensionproperties import Flex2ExtPropType
from .itemmanagement import EdNote, ItemClass
from .link import Link1Type


class PlanningItemContentMeta(ContentMetadataAcDType):
    """
    Content Metadata for a Planning Item
    """
    xml_element_name = 'contentMeta'


class G2ContentType(CommonPowerAttributes):
    """
    The kind of planned G2 item(s)
    """


class ItemCount(CommonPowerAttributes):
    """
    Number of planned G2 items of this kind expressed by a range.
    """
    attributes = {
        'rangefrom': {
            'xml_name': 'rangefrom',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'required'
        },
        'rangeto': {
            'xml_name': 'rangefrom',
            'xml_type': 'xs:positiveInteger',
            'use': 'required'
        }
    }


class AssignedTo(Flex1PartyPropType):
    """
    The party which is assigned to cover the event and produce the planned G2 item.
    """
    attributes = {
        # The starting date (and optionally, the time) by which this property
        # applies to the news coverage planning
        'coversfrom': {
            'xml_name': 'coversfrom',
            'xml_type': 'DateOptTimeType',
            'use': 'required'
        },
        # The end date (and optionally, the time) by which this property applies
        # to the news coverage planning
        'coversto': {
            'xml_name': 'coversto',
            'xml_type': 'DateOptTimeType',
            'use': 'required'
        }
    }


class Scheduled(ApproximateDateTimePropType):
    """
    The scheduled time of delivery for the planned G2 item(s).
    """


class Service(QualPropType):
    """
    An editorial service by which the planned G2 item(s) will be distributed.
    """


class NewsContentCharacteristicsElement(CommonPowerAttributes,
        NewsContentTypeAttributes, NewsContentCharacteristics):
    """
    The characteristics of the content of a News Item
    (NB: Class renamed as we already have an attributegroup with this name)
    """
    xml_element_name = 'newsContentCharacteristics'


class PlanningExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """


class Planning(CommonPowerAttributes):
    """
    Details about the planned news coverage by a specific kind of G2 item.
    """
    elements = [
        ('g2contenttype', {
            'type': 'single', 'xml_name': 'g2contentType',
            'element_class': G2ContentType
        }),
        ('itemclass', {
            'type': 'single', 'xml_name': 'itemClass',
            'element_class': ItemClass
        }),
        ('itemcount', {
            'type': 'single', 'xml_name': 'itemCount',
            'element_class': ItemCount
        }),
        ('assignedto', {
            'type': 'array', 'xml_name': 'assignedTo',
            'element_class': AssignedTo
        }),
        ('scheduled', {
            'type': 'single', 'xml_name': 'scheduled',
            'element_class': Scheduled
        }),
        ('service', {
            'type': 'array', 'xml_name': 'service',
            'element_class': Service
        })
    ] + DescriptiveMetadataGroup + [
        # Additional natural language information about the planned coverage
        # addressed to the editorial people receiving and processing the item.
        ('ednote', {
            'type': 'array', 'xml_name': 'edNote',
            'element_class': EdNote
        }),
        ('newscontentcharacteristics', {
            'type': 'single', 'xml_name': 'newsContentCharacteristics',
            'element_class': NewsContentCharacteristicsElement
        }),
        # The editorial urgency of the content, as scoped by the parent element.
        ('urgency', {
            'type': 'single', 'xml_name': 'urgency',
            'element_class': Urgency
        }),
        ('audience', {
            'type': 'single', 'xml_name': 'audience',
            'element_class': Audience
        }),
        ('exclaudience', {
            'type': 'array', 'xml_name': 'exclAudience',
            'element_class': ExclAudience
        }),
        ('planningextproperty', {
            'type': 'array', 'xml_name': 'planningExtProperty',
            'element_class': PlanningExtProperty
        })
    ]
    attributes = {
        # The starting date (and optionally, the time) by which this property
        # applies to the news coverage planning
        'coversfrom': {
            'xml_name': 'coversfrom',
            'xml_type': 'DateOptTimeType',
            'use': 'optional'
        },
        # The end date (and optionally, the time) by which this property
        # applies to the news coverage planning
        'coversto': {
            'xml_name': 'coversto',
            'xml_type': 'DateOptTimeType',
            'use': 'optional'
        }
    }


class DeliveredItemRef(Link1Type):
    """
    A reference to a G2 item which has been delivered under this news
    coverage definition.
    """


class Delivery(CommonPowerAttributes):
    """
    A set of references to G2 items which have been delivered under this news
    coverage definition.
    """
    elements = [
        ('delivereditemref', {
            'type': 'array', 'xml_name': 'deliveredItemRef',
            'element_class': DeliveredItemRef
        })
    ]


class NewsCoverageExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """


class NewsCoverage(BaseObject):
    """
    Information about the planned and delivered news coverage of the news
    provider.
    This information is aimed at the editorial staff of the receiver
    """
    elements = [
        ('planning', {
            'type': 'array', 'xml_name': 'planning',
            'element_class': Planning
        }),
        ('delivery', {
            'type': 'single', 'xml_name': 'delivery',
            'element_class': Delivery
        }),
        ('newscoverageextproperty', {
            'type': 'array', 'xml_name': 'newsCoverageExtProperty',
            'element_class': NewsCoverageExtProperty
        }),
    ]
    attributes = {
        # The local identifier of the element which MUST be persistent for all
        # versions of the item, i.e. for its entire lifecycle.
        'id': {
            'xml_name': 'id',
            'xml_type': 'xs:ID',
            'use': 'optional'
        },
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a QCode.
        # If the attribute is non-empty, specifies which entity (person,
        # organisation or system) has edited the property.
        'creator': {
            'xml_name': 'creator',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a URI.
        # If the attribute is non-empty, specifies which entity (person,
        # organisation or system) has edited the property.
        'creatoruri': {
            'xml_name': 'creatoruri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The date (and, optionally, the time) when the property was last
        # modified. The initial value is the date (and, optionally, the time) of
        # creation of the property.
        'modified': {
            'xml_name': 'modified',
            'xml_type': 'DateOptTimeType',
            'use': 'optional'
        },
        # If set to true the corresponding property was added to the G2 Item for
        # a specific customer or group of customers only. The default value of
        # this property is false which applies when this attribute is not used
        # with the property.
        'custom': {
            'xml_name': 'custom',
            'xml_type': 'xs:boolean',
            'use': 'optional'
        },
        # Indicates by which means the value was extracted from the content -
        # expressed by a QCode
        'how': {
            'xml_name': 'how',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # Indicates by which means the value was extracted from the content -
        # expressed by a URI
        'howuri': {
            'xml_name': 'howuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # Why the metadata has been included - expressed by a QCode
        'why': {
            'xml_name': 'why',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # Why the metadata has been included - expressed by a URI
        'whyuri': {
            'xml_name': 'whyuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        }
    }


class NewsCoverageSet(CommonPowerAttributes):
    """
    A set of data about planned and delivered news coverage
    """
    elements = [
        ('newscoverage', {
            'type': 'array', 'xml_name': 'newsCoverage',
            'element_class': NewsCoverage
        }),
    ]


class PlanningItem(AnyItem):
    """
    An Item containing information about the planning and delivery of news coverage
    """
    elements = [
        # Content Metadata for a Planning Item
        ('contentmeta', {
            'type': 'single', 'xml_name': 'contentMeta',
            'element_class': PlanningItemContentMeta
        }),
        ('assert', {
            'type': 'array', 'xml_name': 'assert', 'element_class': Assert
        }),
        ('inlineref', {
            'type': 'array', 'xml_name': 'inlineRef',
            'element_class': InlineRef
        }),
        ('derivedfrom', {
            'type': 'array', 'xml_name': 'derivedFrom',
            'element_class': DerivedFrom
        }),
        ('derivedfromvalue', {
            'type': 'array', 'xml_name': 'derivedFromValue',
            'element_class': DerivedFromValue
        }),
        ('newscoverageset', {
            'type': 'array', 'xml_name': 'newsCoverageSet',
            'element_class': NewsCoverageSet
        })
    ]
