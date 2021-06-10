#!/usr/bin/env python

"""
contentMeta classes
"""

from .core import BaseObject, GenericArray
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, MediaContentCharacteristics1,
    RankingAttributes
)
from .concepts import (
    FlexAuthorPropType, FlexLocationPropType, Flex1ConceptPropType,
    Flex1PartyPropType
)
from .complextypes import IntlStringType, TruncatedDateTimePropType
from .extensionproperties import Flex2ExtPropType
from .flextypes import AudienceType
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


class IconElement(TargetResourceAttributes, CommonPowerAttributes,
    MediaContentCharacteristics1):
    """
    An iconic visual identification of the content
    """
    attributes = {
         # Identifies the rendition of the target resource - expressed by
        # a QCode. If the target resource is an item providing multiple
        # renditions then this attribute is used to identify the rendition
        # to be used.
        'rendition': 'rendition',  # type="QCodeType">
        # Identifies the rendition of the target resource - expressed by
        # a URI. If the target resource is an item providing multiple renditions
        # then this attribute is used to identify the rendition to be used.
        'renditionuri': 'renditionuri'  # type="IRIType">
    }


class Icon(GenericArray):
    """
    An array of IconElement objects.
    """
    element_class = IconElement


class LocatedElement(FlexLocationPropType):
    """
    The location from which the content originates.
    """


class Located(GenericArray):
    """
    An array of Located objects.
    """
    element_class = LocatedElement


class InfoSourceElement(Flex1PartyPropType):
    """
    A party (person or organisation) which originated, distributed, aggregated
    or supplied the content or provided some information used to create or
    enhance the content.
    """


class InfoSource(GenericArray):
    """
    An array of InfoSource objects.
    """
    element_class = InfoSourceElement


class CreatorElement(FlexAuthorPropType):
    """
    A party (person or organisation) which created the resource.
    """


class Creator(GenericArray):
    """
    An array of CreatorElement objects.
    """
    element_class = CreatorElement


class ContributorElement(FlexAuthorPropType):
    """
    A party (person or organisation) which modified or enhanced the content,
    preferably the name of a person.
    """


class Contributor(GenericArray):
    """
    An array of ContributorElement objects.
    """
    element_class = ContributorElement


class AudienceElement(AudienceType):
    """
    An intended audience for the content.
    """


class Audience(GenericArray):
    """
    An array of AudienceElement objects.
    """
    element_class = AudienceElement


class ExclAudienceElement(AudienceType):
    """
    An excluded audience for the content.
    """


class ExclAudience(GenericArray):
    """
    An array of ExclAudienceElement objects.
    """
    element_class = AudienceElement


class RatingElement(CommonPowerAttributes):
    """
    Expresses the rating of the content of this item by a party.
    """
    attributes = {
        # The rating of the content expressed as decimal value from a scale.
        'value': 'value',  # type="xs:decimal" use="required">
        # Indicates how the value was calculated (by methods like median,
        # average ...) - expressed by a QCode
        'valcalctype': 'valcalctype',  # type="QCodeType" use="optional">
        # Indicates how the value was calculated (by methods like median,
        # average ...) - expressed by a URI
        'valcalctypeuri': 'valcalctypeuri',  # type="IRIType" use="optional">
        # Indicates the value of the rating scale used for the lowest/worst
        # rating.
        'scalemin': 'scalemin',  # type="xs:decimal" use="required">
        # Indicates the value of the rating scale used for the highest/best
        # rating.
        'scalemax': 'scalemax',  # type="xs:decimal" use="required">
        # The units which apply to the rating scale - expressed by a QCode /
        # either the scaleunit or the scaleunituri attribute MUST be used
        'scaleunit': 'scaleunit',  # type="QCodeType">
        # The units which apply to the rating scale - expressed by a URI /
        # either the scaleunit or the scaleunituri attribute MUST be used
        'scaleunituri': 'scaleunituri',  # type="IRIType">
        # The number of parties acting as raters.
        'raters': 'raters',  # type="xs:nonNegativeInteger" use="optional">
        # The type of the rating parties - expressed by a QCode
        'ratertype': 'ratertype',  # type="QCodeType" use="optional">
        # The type of the rating parties - expressed by a URI
        'ratertypeuri': 'ratertypeuri',  # type="IRIType" use="optional">
        # Full definition of the rating - expressed by a QCode
        'ratingtype': 'ratingtype',  # type="QCodeType">
        # Full definition of the rating - expressed by a URI
        'ratingtypeuri': 'ratingtypeuri'  # type="IRIType">
    }


class Rating(GenericArray):
    """
    An array of RatingElement objects.
    """
    element_class = RatingElement


class UserInteractionElement(CommonPowerAttributes):
    """
    Reflects a specific kind of user interaction with the content of this item.
    """
    attributes = {
        # The count of executed interactions.
        'interactions': 'interactions',  # " type="xs:nonNegativeInteger" use="required">
        # The type of interaction which is reflected by this property -
        # expressed by a QCode / either the interactiontype or the
        # interactiontypeuri attribute MUST be used
        'interactiontype': 'interactiontype',  # " type="QCodeType">
        # The type of interaction which is reflected by this property -
        # expressed by a URI  / either the interactiontype or the
        # interactiontypeuri attribute MUST be used
        'interactiontypeuri': 'interactiontypeuri'  # " type="IRIType">
    }


class UserInteraction(GenericArray):
    """
    An array of UserInteractionElement objects.
    """
    element_class = UserInteractionElement


class LanguageNameElement(IntlStringType):
    """
    A name for a concept assigned as property value.
    """


class LanguageName(GenericArray):
    """
    An array of LanguageNameElement objects.
    """
    element_class = LanguageNameElement


class LanguageElement(CommonPowerAttributes, RankingAttributes):
    """
    A language used by the news content
    """
    elements = {
        'name': { 'type': 'array', 'xml_name': 'name', 'element_class': LanguageName }
    }
    attributes = {
        # The language tag. Values must be valid BCP 47 language tags
        'tag': 'tag',  # " type="xs:language" use="required">
        # A refinement of the semantics of the property - expressed by a QCode
        'role': 'role',  # " type="QCodeListType" use="optional">
        # A refinement of the semantics of the property - expressed by a URI
        'roleuri': 'roleuri'  # " type="IRIListType" use="optional">
    }


class Language(GenericArray):
    """
    An array of LanguageElement objects.
    """
    element_class = LanguageElement


class GenreElement(Flex1ConceptPropType, RankingAttributes):
    """
    A nature, intellectual or journalistic form of the content
    """


class Genre(GenericArray):
    """
    An array of GenreElement objects
    """
    element_class = GenreElement


class KeywordElement(IntlStringType, RankingAttributes):
    """
    Free-text term to be used for indexing or finding the content of text-based search engines
    """
    attributes = {
        # A refinement of the semantics of the keyword - expressed by a QCode
        'role': 'role',  # " type="QCodeListType" use="optional">
        # A refinement of the semantics of the keyword - expressed by a URI
        'roleuri': 'roleuri',  # " type="IRIListType" use="optional">
        # The confidence with which the metadata has been assigned.
        'confidence': 'confidence',  # " type="Int100Type" use="optional">
        # The relevance of the metadata to the news content to which it was attached.
        'relevance': 'relevance'  # " type="Int100Type" use="optional">
    }


class Keyword(GenericArray):
    """
    An array of KeywordElement objects.
    """
    element_class = KeywordElement


class SubjectElement(Flex1ConceptPropType, RankingAttributes):
    """
    An important topic of the content; what the content is about
    """

class Subject(GenericArray):
    """
    An array of SubjectElement objects.
    """
    element_class = SubjectElement


class SluglineElement(IntlStringType, RankingAttributes):
    """
    A sequence of tokens associated with the content. The interpretation is
    provider specific.
    """
    attributes = {
        # The character string acting as a separator between the tokens in the slugline.
        'separator': 'separator',  #  type="xs:string" use="optional">
        # A refinement of the semantics of the slug - expressed by a QCode
        'role': 'role',  #  type="QCodeType" use="optional">
        # A refinement of the semantics of the slug - expressed by a URI
        'roleuri': 'roleuri',  #  type="IRIType" use="optional">
        # The confidence with which the metadata has been assigned.
        'confidence': 'confidence',  #  type="Int100Type" use="optional">
        # The relevance of the metadata to the news content to which it was attached.
        'relevance': 'relevance'  # type="Int100Type" use="optional">
    }

class Slugline(GenericArray):
    """
    An array of SluglineElement objects.
    """
    element_class = SluglineElement


class HeadlineElement(Label1Type, RankingAttributes):
    """
    A brief and snappy introduction to the content, designed to catch the reader's attention
    """
    attributes = {
        # The confidence with which the metadata has been assigned.
        'confidence': 'confidence',  # type="Int100Type" use="optional">
        # The relevance of the metadata to the news content to which it was attached.
        'relevance': 'relevance'  # type="Int100Type" use="optional">
    }


class Headline(GenericArray):
    """
    An array of HeadlineElement objects.
    """
    element_class = HeadlineElement


class DatelineElement(Label1Type, RankingAttributes):
    """
    A natural-language statement of the date and/or place of creation of the content
    """


class Dateline(GenericArray):
    """
    An array of DatelineElement objects.
    """
    element_class = DatelineElement


class ByElement(Label1Type, RankingAttributes):
    """
    A natural-language statement about the creator (author, photographer etc.) of the content
    """


class By(GenericArray):
    """
    An array of ByElement objects.
    """
    element_class = ByElement


class CreditlineElement(IntlStringType, RankingAttributes):
    """
    A free-form expression of the credit(s) for the content
    """


class Creditline(GenericArray):
    """
    An array of CreditlineElement objects.
    """
    element_class = CreditlineElement


class DescriptionElement(BlockType, RankingAttributes):
    """
    A free-form textual description of the content of the item
    """
    attributes = {
        # The confidence with which the metadata has been assigned.
        'confidence': 'confidence',  # type="Int100Type" use="optional">
        # The relevance of the metadata to the news content to which it was attached.
        'relevance': 'relevance'  # type="Int100Type" use="optional">
    }


class Description(GenericArray):
    """
    An array of DescriptionElement objects.
    """
    element_class = DescriptionElement


class ContentMetaExtPropertyElement(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """


class ContentMetaExtProperty(GenericArray):
    """
    An array of ContentMetaExtPropertyElement objects.
    """
    element_class = ContentMetaExtPropertyElement


class DescriptiveMetadataGroup(BaseObject):
    """
    A group of properties associated with the descriptive facet of news related
    content.
    """
    elements = {
        'language': { 'type': 'array', 'xml_name': 'language', 'element_class': Language },
        'genre': { 'type': 'array', 'xml_name': 'genre', 'element_class': Genre },
        'keyword': { 'type': 'array', 'xml_name': 'keyword', 'element_class': Keyword },
        'subject': { 'type': 'array', 'xml_name': 'subject', 'element_class': Subject },
        'slugline': { 'type': 'array', 'xml_name': 'slugline', 'element_class': Slugline },
        'headline': { 'type': 'array', 'xml_name': 'headline', 'element_class': Headline },
        'dateline': { 'type': 'array', 'xml_name': 'dateline', 'element_class': Dateline },
        'by': { 'type': 'array', 'xml_name': 'by', 'element_class': By },
        'creditline': { 'type': 'array', 'xml_name': 'creditline', 'element_class': Creditline },
        'description': { 'type': 'array', 'xml_name': 'description', 'element_class': Description }
    }


class DescriptiveMetadataCoreGroup(BaseObject):
    """
    A group of properties associated with the core descriptive facet of news
    related content.
    """
    elements = {
        'language': { 'type': 'array', 'xml_name': 'language', 'element_class': Language },
        'keyword': { 'type': 'array', 'xml_name': 'keyword', 'element_class': Keyword },
        'subject': { 'type': 'array', 'xml_name': 'subject', 'element_class': Subject },
        'slugline': { 'type': 'array', 'xml_name': 'slugline', 'element_class': Slugline },
        'headline': { 'type': 'array', 'xml_name': 'headline', 'element_class': Headline },
        'description': { 'type': 'array', 'xml_name': 'description', 'element_class': Description }
    }


class AdministrativeMetadataGroup(BaseObject):
    """
    A group of properties associated with the administrative facet of content.
    """
    elements = {
        'urgency': {
            'type': 'single',
            'xml_name': 'urgency',
            'element_class': Urgency
        },
        'contentcreated': {
            'type': 'single',
            'xml_name': 'contentCreated',
            'element_class': ContentCreated
        },
        'contentmodified': {
            'type': 'single',
            'xml_name': 'contentModified',
            'element_class': ContentModified
        },
        'located': {
            'type': 'array',
            'xml_name': 'located',
            'element_class': Located
        },
        'infosource': {
            'type': 'array',
            'xml_name': 'infoSource',
            'element_class': InfoSource
        },
        'creator': {
            'type': 'array',
            'xml_name': 'creator',
            'element_class': Creator
        },
        'contributor': {
            'type': 'array',
            'xml_name': 'contributor',
            'element_class': Contributor
        },
        'audience': {
            'type': 'array',
            'xml_name': 'audience',
            'element_class': Audience
        },
        'exclaudience': {
            'type': 'array',
            'xml_name': 'exclaudience',
            'element_class': ExclAudience
        },
        'altid': {
            'type': 'array',
            'xml_name': 'altid',
            'element_class': AltId
        },
        'rating': {
            'type': 'array',
            'xml_name': 'rating',
            'element_class': Rating
        },
        'userinteraction': {
            'type': 'array',
            'xml_name': 'userInteraction',
            'element_class': UserInteraction
        }
    }


class ContentMetadataAcDType(AdministrativeMetadataGroup,
    DescriptiveMetadataCoreGroup, CommonPowerAttributes,I18NAttributes):
    """
    The type for a  set of metadata properties including Administrative and core
    Descriptive properties about the content
    """

    elements = {
        'icon': { 'type': 'array', 'xml_name': 'icon', 'element_class': Icon },
        'contentMetaExtProperty': {
            'type': 'array',
            'xml_name': 'contentMetaExtProperty',
            'element_class': ContentMetaExtProperty
        }
    }


class ContentMetadataAfDType(AdministrativeMetadataGroup,
    DescriptiveMetadataGroup,CommonPowerAttributes,I18NAttributes):
    """
    The type for a  set of metadata properties including Administrative and core
    Descriptive properties about the content
    """

    elements = {
        'icon': { 'type': 'array', 'xml_name': 'icon', 'element_class': Icon },
        'contentMetaExtProperty': {
            'type': 'array',
            'xml_name': 'contentMetaExtProperty',
            'element_class': ContentMetaExtProperty
        }
    }

class ContentMetadataCatType(CommonPowerAttributes, I18NAttributes):
    """
    The type for a set of metadata properties of a catalog item
    """

    elements = {
        'contentCreated': {
            'type': 'single',
            'xml_name': 'contentCreated',
            'element_class': ContentCreated
        },
        'contentModified': {
            'type': 'single',
            'xml_name': 'contentModified',
            'element_class': ContentModified
        },
        'creator': {
            'type': 'array',
            'xml_name': 'creator',
            'element_class': Creator
        },
        'contributor': {
            'type': 'array',
            'xml_name': 'contributor',
            'element_class': Contributor
        },
        'altid': {
            'type': 'array',
            'xml_name': 'altId',
            'element_class': AltId
        }
    }
