#!/usr/bin/env python

"""
Handle concept groups, including all geographic and address objects.
"""

from lxml import etree

from .core import NEWSMLG2, BaseObject, GenericArray, QCodeURIMixin
from .attributegroups import (
    ArbitraryValueAttributes, CommonPowerAttributes, FlexAttributes,
    I18NAttributes, QualifyingAttributes, QuantifyAttributes,
    TimeValidityAttributes
)
from .concepts import Definition, Note, HierarchyInfo
from .conceptrelationships import Bag, Facet, MainConcept, FacetConcept, ConceptRelationshipsGroup
from .complextypes import IntlStringType, Name
from .link import RemoteInfo
from .parties import PersonDetails, OrganisationDetails

class ConceptDefinitionGroup(BaseObject):
    """
    A group of properites required to define the concept
    """

    elements = {
        'name': { 'type': 'array', 'xml_name': 'name', 'element_class': Name },
        'definition': { 'type': 'array', 'xml_name': 'definition', 'element_class': Definition },
        'note': { 'type': 'array', 'xml_name': 'note', 'element_class': Note },
        'facet': { 'type': 'array', 'xml_name': 'facet', 'element_class': Facet },
        'remoteinfo': { 'type': 'array', 'xml_name': 'remoteInfo', 'element_class': RemoteInfo },
        'hierarchyinfo': { 'type': 'array', 'xml_name': 'hierarchyInfo', 'element_class': HierarchyInfo }
    }

    def get_name(self):
        return self.element_values['name']


class Flex1PropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible generic PCL-type for both controlled and uncontrolled values
    Note: ConceptDefinitionGroup and ConceptRelationshipsGroup are actually in a
          sequence so we may have to handle this differently if we want to output
          schema-compliant documents
    """


class Flex1RolePropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible generic PCL-type for both controlled and uncontrolled values
    """
    attributes = {
        # Refines the semantics of the property - expressed by a QCode
        'role': 'role',
        # Refines the semantics of the property - expressed by a URI
        'roleuri': 'roleuri'
    }


class Flex1ExtPropType(Flex1PropType, ArbitraryValueAttributes):
    """
    Flexible generic PCL-type for controlled, uncontrolled values and arbitrary
    values
    """


class Flex2ExtPropType(Flex1ExtPropType, TimeValidityAttributes):
    """
    Flexible generic PCL-Type for controlled, uncontrolled values and arbitrary
    values, with mandatory relationship
    """
    attributes = {
        # The identifier of a concept defining the semantics of the property
        # - expressed by a QCode
        # either the rel or the reluri attribute MUST be used
        'rel': 'rel',
        # The identifier of a concept defining the semantics of the property
        # - expressed by a URI
        # either the rel or the reluri attribute MUST be used
        'reluri': 'reluri'
    }


class Flex1ConceptPropType(Flex1PropType, QuantifyAttributes):
    """
    Flexible generic PCL-type for both controlled and uncontrolled values, with
    optional attributes
    """

    elements = {
        'bag': { 'type': 'single', 'xml_name': 'bag', 'element_class': Bag },
        'main_concept': { 'type': 'single', 'xml_name': 'mainConcept', 'element_class': MainConcept },
        'facet_concept': { 'type': 'array', 'xml_name': 'facetConcept', 'element_class': FacetConcept }
    }

class FlexPersonPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible person data type for both controlled and uncontrolled values
    """

    elements = {
        'person_details': { 'type': 'single', 'xml_name': 'personDetails', 'element_class': PersonDetails }
    }


class FlexOrganisationPropType(ConceptDefinitionGroup,
    ConceptRelationshipsGroup, CommonPowerAttributes, QualifyingAttributes,
    I18NAttributes):
    """
    Flexible organisation data type for both controlled and uncontrolled values
    """

    elements = {
        'organisation_details': { 'type': 'single', 'xml_name': 'organisationDetails', 'element_class': OrganisationDetails }
    }


class FlexPartyPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes, QCodeURIMixin):
    """
    Flexible party (person or organisation) PCL-type for both controlled and
    uncontrolled values
    """
    elements = {
        # TODO implement these classes
        #'person_details': { 'type': 'single', 'xml_name': 'personDetails', 'element_class': PersonDetails },
        #'organisation_details': { 'type': 'single', 'xml_name': 'organisationDetails', 'element_class': OrganisationDetails }
    }

class Flex1PartyPropType(FlexPartyPropType):
    """
    Flexible party (person or organisation) PCL-type for both controlled and
    uncontrolled values
    """
    attributes = {
        # A refinement of the semantics of the property - expressed by a QCode.
        # In the scope of infoSource only: If a party did anything other than
        # originate information a role attribute with one or more roles must be
        # applied. The recommended vocabulary is the IPTC Information Source
        # Roles NewsCodes at http://cv.iptc.org/newscodes/infosourcerole/
        'role': 'role', # type="QCodeListType">
        # A refinement of the semantics of the property - expressed by a URI.
        # In the scope of infoSource only: If a party did anything other than
        # originate information a role attribute with one or more roles must be
        # applied. The recommended vocabulary is the IPTC Information Source
        # Roles NewsCodes at http://cv.iptc.org/newscodes/infosourcerole/
        'roleuri': 'roleuri', # type="IRIListType">
    }


class FlexAuthorPropType(FlexPartyPropType):
    """
    Flexible Author (creator or contributor) PCL-type for both controlled and
    uncontrolled values
    """
    attributes = {
        # A refinement of the semantics of the property - expressed by
        # a QCode
        'role': 'role', # type="QCodeListType" use="optional">
        # A refinement of the semantics of the property - expressed by
        # a URI
        'roleuri': 'roleuri', # type="IRIListType" use="optional">
        # The job title of the person who created or enhanced the content in
        # the news provider organisation - expressed by a QCode
        'jobtitle': 'jobtitle', # type="QCodeType" use="optional">
        # The job title of the person who created or enhanced the content in
        # the news provider organisation - expressed by a URI
        'jobtitleuri': 'jobtitleuri', # type="IRIType" use="optional">
    }


class GeoAreaDetails(CommonPowerAttributes):
    """
    A group of properties specific to a geopolitical area
    """
    position = None
    # The date the geopolitical area was founded/established.
    founded = None
    # The date the geopolitical area was dissolved.
    dissolved = None
    lines = None
    line_positions = None
    circles = None
    circle_positions = None

    """
    <xs:element ref="position" minOccurs="0" />
    <xs:element name="founded" type="TruncatedDateTimePropType" minOccurs="0">
    <xs:element name="dissolved" type="TruncatedDateTimePropType" minOccurs="0">
    <xs:choice minOccurs="0" maxOccurs="unbounded">
        <xs:element name="line">
            <xs:annotation>
                <xs:documentation>A line as a geographic area</xs:documentation>
            </xs:annotation>
            <xs:complexType>
                <xs:sequence>
                    <xs:element ref="position" maxOccurs="unbounded" />
                </xs:sequence>
                <xs:attributeGroup ref="commonPowerAttributes" />
            </xs:complexType>
        </xs:element>
        <xs:element name="circle">
            <xs:annotation>
                <xs:documentation>A circle as a geographic area</xs:documentation>
            </xs:annotation>
            <xs:complexType>
                <xs:sequence>
                    <xs:element ref="position" />
                </xs:sequence>
                <xs:attributeGroup ref="commonPowerAttributes" />
                'radius': 'radius', # type="xs:double" use="required">
                    <xs:annotation>
                        <xs:documentation>The radius of the circle</xs:documentation>
                    </xs:annotation>
                </xs:attribute>
                'radunit': 'radunit', # type="QCodeType">
                    <xs:annotation>
                        <xs:documentation>The dimension unit of the radius -
                        expressed by a QCode / either the radunit or the radunituri
                        attribute MUST be used</xs:documentation>
                    </xs:annotation>
                </xs:attribute>
                'radunituri': 'radunituri', # type="IRIType">
                    <xs:annotation>
                        <xs:documentation>The dimension unit of the radius -
                        expressed by a URI / either the radunit or the radunituri
                        attribute MUST be used</xs:documentation>
                    </xs:annotation>
                </xs:attribute>
            </xs:complexType>
        </xs:element>
        <xs:element name="polygon">
            <xs:annotation>
                <xs:documentation>A polygon as a geographic area
                </xs:documentation>
            </xs:annotation>
            <xs:complexType>
                <xs:sequence>
                    <xs:element ref="position" maxOccurs="unbounded" />
                </xs:sequence>
                <xs:attributeGroup ref="commonPowerAttributes" />
            </xs:complexType>
        </xs:element>
    </xs:choice>
</xs:sequence>
    """


class LineElement(IntlStringType):
    """
    A line of address information, in the format expected by a recipient postal
    service. City, country area, country and postal code are expressed
    separately.
    """
    attributes = {
        # Refines the semantics of line - expressed by a QCode
        'role': 'role', # type="QCodeType">
        # Refines the semantics of line - expressed by a URI
        'roleuri': 'roleuri', # type="IRIType">
    }


class Line(GenericArray):
    """
    An array of LineElement objects.
    """


class AreaElement(Flex1RolePropType):
    """
    A subdivision of a country part of the address.
    """


class Area(GenericArray):
    """
    A set of AreaElement objects
    """
    element_class = AreaElement


class PostalCode(IntlStringType):
    """
    A postal code part of the address.
    """

class POIDetails(CommonPowerAttributes):
    """
    A group of properties specific to a point of interest
    """
    # The coordinates of the location
    position = None
    # A postal address for the location of a Point Of Interest
    address = None
    # Opening hours of the point of interest expressed in natural language
    open_hours = None
    # Total capacity of the point of interest expressed in natural language
    capacity = None
    # Information how to contact the point of interest.
    contact_info_set = None
    # Ways to access the place of the point of  interest, including directions.
    access_set = None
    # Detailed information about the precise location of the Point of Interest.
    details_set = None
    # The date (and optionally the time) on which this Point of Interest was
    # created
    created = None
    # The date (and optionally the time) on which this Point of Interest ceased
    # to exist
    ceased_to_exist = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            self.address = Address(
                xmlelement=xmlelement.find(NEWSMLG2+'address')
            )
        # TODO finish this

    def as_dict(self):
        self.dict = super().as_dict()
        if self.address:
            self.dict.update({'address': self.address.as_dict()})
        # TODO finish this
        return self.dict

    """
    <xs:complexType>
        <xs:sequence>
            <xs:element name="position" type="GeoCoordinatesType" minOccurs="0">
            <xs:element name="address" type="AddressType" minOccurs="0">
            <xs:element name="openHours" minOccurs="0" type="Label1Type">
            <xs:element name="capacity" minOccurs="0" type="Label1Type">
            <xs:choice minOccurs="0" maxOccurs="unbounded">
                <xs:element name="contactInfo" type="ContactInfoType">
                <xs:element name="access" type="BlockType">
                <xs:element name="details" type="BlockType">
            </xs:choice>
            <xs:element name="created" type="TruncatedDateTimePropType"
                minOccurs="0">
            <xs:element name="ceasedToExist" type="TruncatedDateTimePropType"
                minOccurs="0">
        </xs:sequence>
        <xs:attributeGroup ref="commonPowerAttributes" />
    </xs:complexType>
    """

class Country(Flex1PropType):
    """
    A country part of the address.
    """

class LocalityElement(Flex1RolePropType):
    """
    A city/town/village etc. part of the address.
    """


class Locality(GenericArray):
    """
    A set of LocalityElement objects.
    """
    element_class = LocalityElement


class WorldRegion(Flex1PropType):
    """
    A concept or name only defining the world region part of an address.
    """

class Address(CommonPowerAttributes):
    """
    A postal address for the location of a Point Of Interest
    """
    elements = {
        'line': { 'type': 'array', 'xml_name': 'line', 'element_class': Line },
        'worldregion': { 'type': 'single', 'xml_name': 'worldRegion', 'element_class': WorldRegion },
        'locality': { 'type': 'array', 'xml_name': 'locality', 'element_class': Locality },
        'area': { 'type': 'array', 'xml_name': 'area', 'element_class': Area },
        'country': { 'type': 'single', 'xml_name': 'country', 'element_class': Country },
        'postal_code': { 'type': 'single', 'xml_name': 'postalCode', 'element_class': PostalCode }
    }
    attributes = {
        # A refinement of the semantics of the postal address - expressed by
        # a QCode
        'role': 'role',
        # A refinement of the semantics of the postal address - expressed by
        # a URI
        'roleuri': 'roleuri'
    }


class FlexLocationPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    FlexAttributes, CommonPowerAttributes, I18NAttributes):
    """
    Flexible location (geopolitical area of point-of-interest)
    data type for both controlled and uncontrolled values
    """

    elements = {
        'geo_area_details': {
            'type': 'single',
            'xml_name': 'geoAreaDetails',
            'element_class': GeoAreaDetails
        },
        'poi_details': {
            'type': 'single',
            'xml_name': 'POIDetails',
            'element_class': POIDetails
        }
    }

    def __bool__(self):
        return self.geo_area_details is not None or self.poi_details is not None


class FlexGeoAreaPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible geopolitical area data type for both controlled and uncontrolled
    values
    """

    elements = {
        'geo_area_details': {
            'type': 'single',
            'xml_name': 'geoAreaDetails',
            'element_class': GeoAreaDetails
        }
    }


class FlexPOIPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible point-of-intrerest data type for both controlled and uncontrolled
    values
    """

    elements = {
        'poi_details': {
            'type': 'single',
            'xml_name': 'POIDetails',
            'element_class': POIDetails
        }
    }



