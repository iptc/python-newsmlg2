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
from .concepts import Names
from .complextypes import IntlStringType

class ConceptDefinitionGroup(BaseObject):
    """
    A group of properites required to define the concept
    """
    names = None
    definition = None
    note = None
    facet = None
    remote_info = None
    hierarchy_info = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            self.names = Names(
                xmlarray=xmlelement.findall(NEWSMLG2+'name')
            )
            self.definition = xmlelement.findtext(NEWSMLG2+'definition')
            self.note = xmlelement.findtext(NEWSMLG2+'note')
            self.facet = xmlelement.findtext(NEWSMLG2+'facet')
            self.remote_info = xmlelement.findtext(NEWSMLG2+'remoteInfo')
            self.hierarchy_info = xmlelement.findtext(NEWSMLG2+'hierarchyInfo')

    def as_dict(self):
        self.dict = super().as_dict()
        if self.names:
            self.dict.update({'names': self.names.as_dict()})
        if self.definition:
            self.dict.update({'definition': self.definition})
        if self.note:
            self.dict.update({'note': self.note})
        if self.facet:
            self.dict.update({'facet': self.facet})
        if self.remote_info:
            self.dict.update({'remoteInfo': self.remote_info})
        if self.hierarchy_info:
            self.dict.update({'hierarchyInfo': self.hierarchy_info})
        return self.dict


class ConceptRelationshipsGroup(BaseObject):
    """
    A group of properites required to indicate relationships of the concept
    to other concepts
    """

    """
    TODO
            <xs:choice minOccurs="0" maxOccurs="unbounded">
                <xs:element ref="sameAs" />
                <xs:element ref="broader" />
                <xs:element ref="narrower" />
                <xs:element ref="related" />
            </xs:choice>
    """

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
    TODO:
    <xs:sequence>
       <xs:element ref="bag" minOccurs="0"/>
       <xs:element ref="mainConcept" minOccurs="0"/>
       <xs:element ref="facetConcept" minOccurs="0" maxOccurs="unbounded"/>
    </xs:sequence>
    """


class FlexPersonPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible person data type for both controlled and uncontrolled values
    TODO:
             <xs:element ref="personDetails" minOccurs="0"/>
    """


class FlexOrganisationPropType(ConceptDefinitionGroup,
    ConceptRelationshipsGroup, CommonPowerAttributes, QualifyingAttributes,
    I18NAttributes):
    """
    Flexible organisation data type for both controlled and uncontrolled values
    TODO:
             <xs:element ref="organisationDetails" minOccurs="0"/>
    """


class FlexGeoAreaPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible geopolitical area data type for both controlled and uncontrolled
    values

    TODO
             <xs:element ref="geoAreaDetails" minOccurs="0"/>
    """


class FlexPOIPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible point-of-intrerest data type for both controlled and uncontrolled
    values

    TODO
             <xs:element ref="POIDetails" minOccurs="0"/>
    """


class FlexPartyPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes, QCodeURIMixin):
    """
    Flexible party (person or organisation) PCL-type for both controlled and
    uncontrolled values
  <xs:sequence>
     <xs:group ref="ConceptDefinitionGroup" minOccurs="0"/>
     <xs:group ref="ConceptRelationshipsGroup" minOccurs="0"/>
     <xs:choice minOccurs="0">
        <xs:element ref="personDetails"/>
        <xs:element ref="organisationDetails"/>
     </xs:choice>
     <xs:any namespace="##other"
             processContents="lax"
             minOccurs="0"
             maxOccurs="unbounded">
        <xs:annotation>
           <xs:documentation>Extension point for provider-defined
            properties from other namespaces</xs:documentation>
        </xs:annotation>
     </xs:any>
  </xs:sequence>
  <xs:attributeGroup ref="commonPowerAttributes"/>
  <xs:attributeGroup ref="flexAttributes"/>
  <xs:attributeGroup ref="i18nAttributes"/>
  <xs:anyAttribute namespace="##other" processContents="lax"/>
    """

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


class FlexLocationPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    FlexAttributes, CommonPowerAttributes, I18NAttributes):
    """
    Flexible location (geopolitical area of point-of-interest)
    data type for both controlled and uncontrolled values
    plus: <xs:anyAttribute namespace="##other" processContents="lax" />
    """
    geo_area_details = None
    poi_details = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            self.geo_area_details = GeoAreaDetails(
                # note lowerCamelCase element name, this is correct
                xmlelement=xmlelement.find(NEWSMLG2+'geoAreaDetails')
            )
            self.poi_details = POIDetails(
                # note case of element name, this is correct
                xmlelement=xmlelement.find(NEWSMLG2+'POIDetails')
            )

    def as_dict(self):
        self.dict = super().as_dict()
        if self.geo_area_details:
            self.dict.update(
                {'geoAreaDetails': self.geo_area_details.as_dict()})
        if self.poi_details:
            self.dict.update({'POIDetails': self.poi_details.as_dict()})
        return self.dict

    def __bool__(self):
        return self.geo_area_details is not None or self.poi_details is not None

    """
    <xs:complexType name="FlexLocationPropType">
        <xs:sequence>
            <xs:choice minOccurs="0">
                <xs:element ref="geoAreaDetails" />
                <xs:element ref="POIDetails" />
            </xs:choice>
            <xs:any namespace="##other" processContents="lax" minOccurs="0"
                maxOccurs="unbounded">
                <xs:annotation>
                    <xs:documentation>Extension point for provider-defined
                    properties from other namespaces</xs:documentation>
                </xs:annotation>
            </xs:any>
        </xs:sequence>
    </xs:complexType>
    """

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
    <xs:any namespace="##other" processContents="lax" minOccurs="0"
        maxOccurs="unbounded">
        <xs:annotation>
            <xs:documentation>Extension point for provider-defined properties
            from other namespaces</xs:documentation>
        </xs:annotation>
    </xs:any>
</xs:sequence>
    """

    def as_dict(self):
        return self.dict

class Lines(BaseObject):
    """
    <xs:element name="line" minOccurs="0" maxOccurs="unbounded">
        <xs:complexType>
            <xs:complexContent>
                <xs:extension base="IntlStringType">
                    'role': 'role', # type="QCodeType">
                        <xs:annotation>
                            <xs:documentation>Refines the semantics of line -
                            expressed by a QCode</xs:documentation>
                        </xs:annotation>
                    </xs:attribute>
                    'roleuri': 'roleuri', # type="IRIType">
                        <xs:annotation>
                            <xs:documentation>Refines the semantics of line -
                            expressed by a URI</xs:documentation>
                        </xs:annotation>
                    </xs:attribute>
                </xs:extension>
            </xs:complexContent>
        </xs:complexType>
    </xs:element>
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

class Address(CommonPowerAttributes):
    """
    A postal address for the location of a Point Of Interest
    """
    attributes = {
        # A refinement of the semantics of the postal address - expressed by
        # a QCode
        'role': 'role',
        # A refinement of the semantics of the postal address - expressed by
        # a URI
        'roleuri': 'roleuri'
    }
    # A line of address information, in the format expected by a recipient
    # postal service. City, country area, country and postal code are expressed
    # separately.
    lines = None
    localities = None
    # A subdivision of a country part of the address.
    areas = None
    # A country part of the address.
    country = None
    # A postal code part of the address.
    postal_code = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            self.lines = Lines(
                xmlarray=xmlelement.findall(NEWSMLG2+'line')
            )
            self.localities = Locality(
                xmlarray=xmlelement.findall(NEWSMLG2+'locality')
            )
            self.areas = Area(
                xmlarray=xmlelement.findall(NEWSMLG2+'area')
            )
            self.country = Country(
                xmlelement=xmlelement.find(NEWSMLG2+'country')
            )
            self.postal_code = PostalCode(
                xmlelement=xmlelement.find(NEWSMLG2+'postal-code')
            )

    def as_dict(self):
        self.dict = super().as_dict()
        if self.lines:
            self.dict.update({'lines': self.lines.as_dict()})
        if self.localities:
            self.dict.update({'localities': self.localities.as_dict()})
        if self.areas:
            self.dict.update({'areas': self.areas.as_dict()})
        if self.country:
            self.dict.update({'country': self.country.as_dict()})
        if self.postal_code:
            self.dict.update({'postalCode': self.postal_code.as_dict()})
        return self.dict


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

    """
    address:
    <xs:element name="locality" minOccurs="0" maxOccurs="unbounded"
        type="Flex1RolePropType">
        <xs:annotation>
            <xs:documentation>A city/town/village etc. part of the address.
            </xs:documentation>
        </xs:annotation>
    </xs:element>
    <xs:element name="area" minOccurs="0" maxOccurs="unbounded"
        type="Flex1RolePropType">
        <xs:annotation>
            <xs:documentation>A subdivision of a country part of the
            address.</xs:documentation>
        </xs:annotation>
    </xs:element>
    <xs:element name="country" minOccurs="0" type="Flex1PropType">
        <xs:annotation>
            <xs:documentation>A country part of the address.</xs:documentation>
        </xs:annotation>
    </xs:element>
    <xs:element name="postalCode" type="IntlStringType" minOccurs="0">
        <xs:annotation>
            <xs:documentation>A postal code part of the address.
            </xs:documentation>
        </xs:annotation>
    </xs:element>
    """


class Locality(GenericArray):
    """
    A set of LocalityElement objects.
    """
    element_class = LocalityElement
