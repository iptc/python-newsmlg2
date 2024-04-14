#!/usr/bin/env python

"""
contentMeta classes
"""

from .core import BaseObject
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, MediaContentCharacteristics1,
    RankingAttributes, QuantifyAttributes
)
from .concepts import (
    FlexAuthorPropType, FlexLocationPropType, Flex1ConceptPropType,
    Flex1PartyPropType, Flex1PropType
)
from .conceptrelationships import FlexPropType
from .complextypes import IntlStringType, TruncatedDateTimePropType
from .extensionproperties import Flex2ExtPropType
from .ids import AltId
from .labeltypes import BlockType, Label1Type
from .link import TargetResourceAttributes
from .simpletypes import Int1to9Type

class Urgency(Int1to9Type, CommonPowerAttributes):
    """
    The editorial urgency of the content, as scoped by the parent element.
    """


class ContentCreated(TruncatedDateTimePropType):
    """
    The date (and optionally the time) on which the content was created.
    """


class ContentModified(TruncatedDateTimePropType):
    """
    The date (and optionally the time) on which the content was last modified.
    """


class DigitalSourceType(FlexPropType):
    """
    Indicates the source type from which the content was created. The recommended vocabulary is the IPTC Digital Source Type NewsCodes http://cv.iptc.org/newscodes/digitalsourcetype/
    """

class Icon(TargetResourceAttributes, CommonPowerAttributes,
    MediaContentCharacteristics1):
    """
    An iconic visual identification of the content
    """
    attributes = {
         # Identifies the rendition of the target resource - expressed by
        # a QCode. If the target resource is an item providing multiple
        # renditions then this attribute is used to identify the rendition
        # to be used.
        'rendition': {
            'xml_name': 'rendition',
            'xml_type': 'QCodeType'
        },
        # Identifies the rendition of the target resource - expressed by
        # a URI. If the target resource is an item providing multiple renditions
        # then this attribute is used to identify the rendition to be used.
        'renditionuri': {
            'xml_name': 'renditionuri',
            'xml_type': 'IRIType'
        }
    }


class Located(FlexLocationPropType):
    """
    The location from which the content originates.
    """


class InfoSource(Flex1PartyPropType):
    """
    A party (person or organisation) which originated, distributed, aggregated
    or supplied the content or provided some information used to create or
    enhance the content.
    """


class Creator(FlexAuthorPropType):
    """
    A party (person or organisation) which created the resource.
    """


class Contributor(FlexAuthorPropType):
    """
    A party (person or organisation) which modified or enhanced the content,
    preferably the name of a person.
    """


class AudienceType(Flex1PropType, QuantifyAttributes):
    """
    The type to cover all qualifers for an audience property
    """
    attributes = {
        # A qualifier which indicates the expected significance of the content
        # for this specific audience.
        'significance': {
            'xml_name': 'significance',
            'xml_type': 'Int1to9Type',
            'use': 'optional'
        }
    }


class Audience(AudienceType):
    """
    An intended audience for the content.
    """


class ExclAudience(AudienceType):
    """
    An excluded audience for the content.
    """


class Rating(CommonPowerAttributes):
    """
    Expresses the rating of the content of this item by a party.
    """
    attributes = {
        # The rating of the content expressed as decimal value from a scale.
        'value': {
            'xml_name': 'value',
            'xml_type': 'xs:decimal',
            'use': 'required'
        },
        # Indicates how the value was calculated (by methods like median,
        # average ...) - expressed by a QCode
        'valcalctype': {
            'xml_name': 'valcalctype',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # Indicates how the value was calculated (by methods like median,
        # average ...) - expressed by a URI
        'valcalctypeuri': {
            'xml_name': 'valcalctypeuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # Indicates the value of the rating scale used for the lowest/worst
        # rating.
        'scalemin': {
            'xml_name': 'scalemin',
            'xml_type': 'xs:decimal',
            'use': 'required'
        },
        # Indicates the value of the rating scale used for the highest/best
        # rating.
        'scalemax': {
            'xml_name': 'scalemax',
            'xml_type': 'xs:decimal',
            'use': 'required'
        },
        # The units which apply to the rating scale - expressed by a QCode /
        # either the scaleunit or the scaleunituri attribute MUST be used
        'scaleunit': {
            'xml_name': 'scaleunit',
            'xml_type': 'QCodeType'
        },
        # The units which apply to the rating scale - expressed by a URI /
        # either the scaleunit or the scaleunituri attribute MUST be used
        'scaleunituri': {
            'xml_name': 'scaleunituri',
            'xml_type': 'IRIType'
        },
        # The number of parties acting as raters.
        'raters': {
            'xml_name': 'raters',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # The type of the rating parties - expressed by a QCode
        'ratertype': {
            'xml_name': 'ratertype',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The type of the rating parties - expressed by a URI
        'ratertypeuri': {
            'xml_name': 'ratertypeuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # Full definition of the rating - expressed by a QCode
        'ratingtype': {
            'xml_name': 'ratingtype',
            'xml_type': 'QCodeType'
        },
        # Full definition of the rating - expressed by a URI
        'ratingtypeuri': {
            'xml_name': 'ratingtypeuri',
            'xml_type': 'IRIType'
        }
    }


class UserInteraction(CommonPowerAttributes):
    """
    Reflects a specific kind of user interaction with the content of this item.
    """
    attributes = {
        # The count of executed interactions.
        'interactions': {
            'xml_name': 'interactions',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'required'
        },
        # The type of interaction which is reflected by this property -
        # expressed by a QCode / either the interactiontype or the
        # interactiontypeuri attribute MUST be used
        'interactiontype': {
            'xml_name': 'interactiontype',
            'xml_type': 'QCodeType'
        },
        # The type of interaction which is reflected by this property -
        # expressed by a URI  / either the interactiontype or the
        # interactiontypeuri attribute MUST be used
        'interactiontypeuri': {
            'xml_name': 'interactiontypeuri',
            'xml_type': 'IRIType'
        }
    }


class LanguageName(IntlStringType):
    """
    A name for a concept assigned as property value.
    """


class Language(CommonPowerAttributes, RankingAttributes):
    """
    A language used by the news content
    """
    elements = [
        ('name', {
            'type': 'array', 'xml_name': 'name', 'element_class': LanguageName
        })
    ]
    attributes = {
        # The language tag. Values must be valid BCP 47 language tags
        'tag': {
            'xml_name': 'tag',
            'xml_type': 'xs:language',
            'use': 'required'
        },
        # A refinement of the semantics of the property - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeListType',
            'use': 'optional'
        },
        # A refinement of the semantics of the property - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIListType',
            'use': 'optional'
        }
    }


class Genre(Flex1ConceptPropType, RankingAttributes):
    """
    A nature, intellectual or journalistic form of the content
    """


class Keyword(IntlStringType, RankingAttributes):
    """
    Free-text term to be used for indexing or finding the content of text-based search engines
    """
    attributes = {
        # A refinement of the semantics of the keyword - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeListType',
            'use': 'optional'
        },
        # A refinement of the semantics of the keyword - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIListType',
            'use': 'optional'
        },
        # The confidence with which the metadata has been assigned.
        'confidence': {
            'xml_name': 'confidence',
            'xml_type': 'Int100Type',
            'use': 'optional'
        },
        # The relevance of the metadata to the news content to which it was attached.
        'relevance': {
            'xml_name': 'relevance',
            'xml_type': 'Int100Type',
            'use': 'optional'
        }
    }


class Subject(Flex1ConceptPropType, RankingAttributes):
    """
    An important topic of the content; what the content is about
    """


class Slugline(IntlStringType, RankingAttributes):
    """
    A sequence of tokens associated with the content. The interpretation is
    provider specific.
    """
    attributes = {
        # The character string acting as a separator between the tokens in the slugline.
        'separator': {
            'xml_name': 'separator',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # A refinement of the semantics of the slug - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # A refinement of the semantics of the slug - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The confidence with which the metadata has been assigned.
        'confidence': {
            'xml_name': 'confidence',
            'xml_type': 'Int100Type',
            'use': 'optional'
        },
        # The relevance of the metadata to the news content to which it was attached.
        'relevance': {
            'xml_name': 'relevance',
            'xml_type': 'Int100Type',
            'use': 'optional'
        }
    }


class Headline(Label1Type, RankingAttributes):
    """
    A brief and snappy introduction to the content, designed to catch the reader's attention
    """
    attributes = {
        # The confidence with which the metadata has been assigned.
        'confidence': {
            'xml_name': 'confidence',
            'xml_type': 'Int100Type',
            'use': 'optional'
        },
        # The relevance of the metadata to the news content to which it was attached.
        'relevance': {
            'xml_name': 'relevance',
            'xml_type': 'Int100Type',
            'use': 'optional'
        }
    }


class Dateline(Label1Type, RankingAttributes):
    """
    A natural-language statement of the date and/or place of creation of the content
    """


class By(Label1Type, RankingAttributes):
    """
    A natural-language statement about the creator (author, photographer etc.) of the content
    """


class Creditline(IntlStringType, RankingAttributes):
    """
    A free-form expression of the credit(s) for the content
    """


class Description(BlockType, RankingAttributes):
    """
    A free-form textual description of the content of the item
    """
    attributes = {
        # The confidence with which the metadata has been assigned.
        'confidence': {
            'xml_name': 'confidence',
            'xml_type': 'Int100Type',
            'use': 'optional'
        },
        # The relevance of the metadata to the news content to which it was attached.
        'relevance': {
            'xml_name': 'relevance',
            'xml_type': 'Int100Type',
            'use': 'optional'
        }
    }


class ContentMetaExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """


"""
A group of properties associated with the descriptive facet of news related
content.
"""
DescriptiveMetadataGroup = [
    ('language', { 'type': 'array', 'xml_name': 'language', 'element_class': Language }),
    ('genre', { 'type': 'array', 'xml_name': 'genre', 'element_class': Genre }),
    ('keyword', { 'type': 'array', 'xml_name': 'keyword', 'element_class': Keyword }),
    ('subject', { 'type': 'array', 'xml_name': 'subject', 'element_class': Subject }),
    ('slugline', { 'type': 'array', 'xml_name': 'slugline', 'element_class': Slugline }),
    ('headline', { 'type': 'array', 'xml_name': 'headline', 'element_class': Headline }),
    ('dateline', { 'type': 'array', 'xml_name': 'dateline', 'element_class': Dateline }),
    ('by', { 'type': 'array', 'xml_name': 'by', 'element_class': By }),
    ('creditline', { 'type': 'array', 'xml_name': 'creditline', 'element_class': Creditline }),
    ('description', { 'type': 'array', 'xml_name': 'description', 'element_class': Description })
]


"""
A group of properties associated with the core descriptive facet of news
related content.
"""
DescriptiveMetadataCoreGroup = [
    ('language', { 'type': 'array', 'xml_name': 'language', 'element_class': Language }),
    ('keyword', { 'type': 'array', 'xml_name': 'keyword', 'element_class': Keyword }),
    ('subject', { 'type': 'array', 'xml_name': 'subject', 'element_class': Subject }),
    ('slugline', { 'type': 'array', 'xml_name': 'slugline', 'element_class': Slugline }),
    ('headline', { 'type': 'array', 'xml_name': 'headline', 'element_class': Headline }),
    ('description', { 'type': 'array', 'xml_name': 'description', 'element_class': Description })
]


"""
A group of properties associated with the administrative facet of content.
"""
AdministrativeMetadataGroup = [
    ('urgency', {
        'type': 'single',
        'xml_name': 'urgency',
        'element_class': Urgency
    }),
    ('contentcreated', {
        'type': 'single',
        'xml_name': 'contentCreated',
        'element_class': ContentCreated
    }),
    ('contentmodified', {
        'type': 'single',
        'xml_name': 'contentModified',
        'element_class': ContentModified
    }),
    ('digitalsourcetype', {
        'type': 'single',
        'xml_name': 'digitalSourceType',
        'element_class': DigitalSourceType
    }),
    ('located', {
        'type': 'array',
        'xml_name': 'located',
        'element_class': Located
    }),
    ('infosource', {
        'type': 'array',
        'xml_name': 'infoSource',
        'element_class': InfoSource
    }),
    ('creator', {
        'type': 'array',
        'xml_name': 'creator',
        'element_class': Creator
    }),
    ('contributor', {
        'type': 'array',
        'xml_name': 'contributor',
        'element_class': Contributor
    }),
    ('audience', {
        'type': 'array',
        'xml_name': 'audience',
        'element_class': Audience
    }),
    ('exclaudience', {
        'type': 'array',
        'xml_name': 'exclaudience',
        'element_class': ExclAudience
    }),
    ('altid', {
        'type': 'array',
        'xml_name': 'altid',
        'element_class': AltId
    }),
    ('rating', {
        'type': 'array',
        'xml_name': 'rating',
        'element_class': Rating
    }),
    ('userinteraction', {
        'type': 'array',
        'xml_name': 'userInteraction',
        'element_class': UserInteraction
    })
]


class ContentMetadataAcDType(CommonPowerAttributes,I18NAttributes):
    """
    The type for a  set of metadata properties including Administrative and core
    Descriptive properties about the content
    """

    elements = [
        ('icon', { 'type': 'array', 'xml_name': 'icon', 'element_class': Icon })
    ] + AdministrativeMetadataGroup + DescriptiveMetadataCoreGroup + [
        ('contentMetaExtProperty', {
            'type': 'array',
            'xml_name': 'contentMetaExtProperty',
            'element_class': ContentMetaExtProperty
        })
    ]


class ContentMetadataAfDType(CommonPowerAttributes,I18NAttributes):
    """
    The type for a  set of metadata properties including Administrative and core
    Descriptive properties about the content
    """

    elements = [
        ('icon', { 'type': 'array', 'xml_name': 'icon', 'element_class': Icon })
    ] + AdministrativeMetadataGroup + DescriptiveMetadataGroup + [
        ('contentMetaExtProperty', {
            'type': 'array',
            'xml_name': 'contentMetaExtProperty',
            'element_class': ContentMetaExtProperty
        })
    ]


class ContentMetadataCatType(CommonPowerAttributes, I18NAttributes):
    """
    The type for a set of metadata properties of a catalog item
    """

    elements = [
        ('contentCreated', {
            'type': 'single',
            'xml_name': 'contentCreated',
            'element_class': ContentCreated
        }),
        ('contentModified', {
            'type': 'single',
            'xml_name': 'contentModified',
            'element_class': ContentModified
        }),
        ('creator', {
            'type': 'array',
            'xml_name': 'creator',
            'element_class': Creator
        }),
        ('contributor', {
            'type': 'array',
            'xml_name': 'contributor',
            'element_class': Contributor
        }),
        ('altid', {
            'type': 'array',
            'xml_name': 'altId',
            'element_class': AltId
        })
    ]
