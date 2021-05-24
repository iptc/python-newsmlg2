#!/usr/bin/env python

from lxml import etree

from .core import XML, NEWSMLG2, BaseObject, GenericArray
from .catalogstore import CATALOG_STORE
from .concepts import Names
from .attributegroups import (
    ArbitraryValueAttributes, CommonPowerAttributes, FlexAttributes, I18NAttributes, QualifyingAttributes, QuantifyAttributes, TimeValidityAttributes
)

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
        super(ConceptDefinitionGroup, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.names = Names(
                xmlarray=xmlelement.findall(NEWSMLG2+'name')
            )
            self.definition = xmlelement.findtext(NEWSMLG2+'definition')
            self.note = xmlelement.findtext(NEWSMLG2+'note')
            self.facet = xmlelement.findtext(NEWSMLG2+'facet')
            self.remote_info = xmlelement.findtext(NEWSMLG2+'remoteInfo')
            self.hierarchy_info = xmlelement.findtext(NEWSMLG2+'hierarchyInfo')

    def as_dict(self):
        super(ConceptDefinitionGroup, self).as_dict()
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
    A group of properites required to indicate relationships of the concept to other concepts
    """

    pass
    """
    TODO
            <xs:choice minOccurs="0" maxOccurs="unbounded">
                <xs:element ref="sameAs" />
                <xs:element ref="broader" />
                <xs:element ref="narrower" />
                <xs:element ref="related" />
            </xs:choice>
    """

class Flex1PropType(ConceptDefinitionGroup, ConceptRelationshipsGroup, CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible generic PCL-type for both controlled and uncontrolled values
    Note: ConceptDefinitionGroup and ConceptRelationshipsGroup are actually in a sequence so we may
          have to handle this differently if we want to output schema-compliant documents
    """
    pass


class Flex1RolePropType(ConceptDefinitionGroup, ConceptRelationshipsGroup, CommonPowerAttributes, FlexAttributes, I18NAttributes):
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
    Flexible generic PCL-type for controlled, uncontrolled values and arbitrary values
    """
    pass


class Flex2ExtPropType(Flex1ExtPropType, TimeValidityAttributes):
    """
    Flexible generic PCL-Type for controlled, uncontrolled values and arbitrary values, with mandatory relationship
    """
    attributes = {
        # The identifier of a concept defining the semantics of the property - expressed by a QCode
        # either the rel or the reluri attribute MUST be used
        'rel': 'rel',
        # The identifier of a concept defining the semantics of the property - expressed by a URI
        # either the rel or the reluri attribute MUST be used
        'reluri': 'reluri'
    }


class Flex1ConceptPropType(Flex1PropType, QuantifyAttributes):
    """ 
    Flexible generic PCL-type for both controlled and uncontrolled values, with optional attributes
    TODO:
            <xs:sequence>
               <xs:element ref="bag" minOccurs="0"/>
               <xs:element ref="mainConcept" minOccurs="0"/>
               <xs:element ref="facetConcept" minOccurs="0" maxOccurs="unbounded"/>
            </xs:sequence>
    """
    pass


class FlexPersonPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup, CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible person data type for both controlled and uncontrolled values
    TODO:
             <xs:element ref="personDetails" minOccurs="0"/>
    """
    pass


class FlexOrganisationPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup, CommonPowerAttributes, QualifyingAttributes, I18NAttributes):
    """
    Flexible organisation data type for both controlled and uncontrolled values
    TODO:
             <xs:element ref="organisationDetails" minOccurs="0"/>
    """
    pass


class FlexGeoAreaPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup, CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible geopolitical area data type for both controlled and uncontrolled values

    TODO
             <xs:element ref="geoAreaDetails" minOccurs="0"/>
    """
    pass


class FlexPOIPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup, CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible point-of-intrerest data type for both controlled and uncontrolled values

    TODO
             <xs:element ref="POIDetails" minOccurs="0"/>
    """
    pass


class FlexPartyPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup, CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible party (person or organisation) PCL-type for both controlled and uncontrolled values
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
               <xs:documentation>Extension point for provider-defined properties from other namespaces</xs:documentation>
            </xs:annotation>
         </xs:any>
      </xs:sequence>
      <xs:attributeGroup ref="commonPowerAttributes"/>
      <xs:attributeGroup ref="flexAttributes"/>
      <xs:attributeGroup ref="i18nAttributes"/>
      <xs:anyAttribute namespace="##other" processContents="lax"/>
    """
    attributes = {
        # A qualified code which identifies a concept  - either the  qcode or the uri attribute MUST be used
        'qcode': 'qcode',
        # A URI which identifies a concept  - either the  qcode or the uri attribute MUST be used
        'uri': 'uri'
    }
    # TODO copy and paste from FlexPartyPropType above, need to merge

    def getQcode(self):
        qcode = self.get_attr('qcode')
        if qcode:
            return qcode
        else:
            # convert URI to qcode:
            uri = self.get_attr('uri')
            urimainpart, code = uri.rsplit('/', 1)
            # get catalog
            scheme = CATALOG_STORE.getSchemeForURI(urimainpart)
            # look up catalog for URI, get prefix
            alias = scheme.alias
            return alias + ':' + code

    def getURI(self):
        uri = self.get_attr('uri')
        if uri:
            return uri
        else:
            # convert qcode to URI:
            qcode = self.get_attr('qcode')
            alias, code = qcode.split(':')
            # get catalog
            scheme = CATALOG_STORE.getSchemeForAlias(alias)
            # look up catalog for alias, get URI
            uri = scheme.uri
            return uri + code


class Flex1PartyPropType(FlexPartyPropType):
    """
    Flexible party (person or organisation) PCL-type for both controlled and uncontrolled values
    """
    attributes = {
        # A refinement of the semantics of the property - expressed by a QCode. In the scope of infoSource only: If a party did anything other than originate information a role attribute with one or more roles must be applied. The recommended vocabulary is the IPTC Information Source Roles NewsCodes at http://cv.iptc.org/newscodes/infosourcerole/
        'role': 'role', # type="QCodeListType">
        # A refinement of the semantics of the property - expressed by a URI. In the scope of infoSource only: If a party did anything other than originate information a role attribute with one or more roles must be applied. The recommended vocabulary is the IPTC Information Source Roles NewsCodes at http://cv.iptc.org/newscodes/infosourcerole/
        'roleuri': 'roleuri', # type="IRIListType">
    }


class FlexAuthorPropType(FlexPartyPropType):
    """
    Flexible Author (creator or contributor) PCL-type for both controlled and uncontrolled values
    """
    attributes = {
            # A refinement of the semantics of the property - expressed by a QCode</xs:documentation>
            'role': 'role', # type="QCodeListType" use="optional">
            # A refinement of the semantics of the property - expressed by a URI
            'roleuri': 'roleuri', # type="IRIListType" use="optional">
            # The job title of the person who created or enhanced the content in the news provider organisation - expressed by a QCode
            'jobtitle': 'jobtitle', # type="QCodeType" use="optional">
            # The job title of the person who created or enhanced the content in the news provider organisation - expressed by a URI
            'jobtitleuri': 'jobtitleuri', # type="IRIType" use="optional">
    }


class FlexLocationPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup, FlexAttributes, CommonPowerAttributes, I18NAttributes):
    """
    Flexible location (geopolitical area of point-of-interest)
    data type for both controlled and uncontrolled values
    plus: <xs:anyAttribute namespace="##other" processContents="lax" />
    """
    geo_area_details = None
    poi_details = None

    def __init__(self, **kwargs):
        super(FlexLocationPropType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.geo_area_details = GeoAreaDetails(
                # note lowerCamelCase element name, this is correct
                xmlelement=xmlelement.find(NEWSMLG2+'geoAreaDetails')
            )
            self.poi_details = POIDetails(
                # note case of element name, this is correct
                xmlelement=xmlelement.find(NEWSMLG2+'POIDetails')
            )

    def as_dict(self):
        super(FlexLocationPropType, self).as_dict()
        if self.geo_area_details:
            self.dict.update(
                {'geoAreaDetails': self.geo_area_details.as_dict()})
        if self.poi_details:
            self.dict.update({'POIDetails': self.poi_details.as_dict()})
        return self.dict

    def __bool__(self):
        # TODO
        return self.geo_area_details is not None or self.poi_details is not None

    """
    <xs:complexType name="FlexLocationPropType">
        <xs:sequence>
            <xs:choice minOccurs="0">
                <xs:element ref="geoAreaDetails" />
                <xs:element ref="POIDetails" />
            </xs:choice>
            <xs:any namespace="##other" processContents="lax" minOccurs="0" maxOccurs="unbounded">
                <xs:annotation>
                    <xs:documentation>Extension point for provider-defined properties from other namespaces</xs:documentation>
                </xs:annotation>
            </xs:any>
        </xs:sequence>
    </xs:complexType>
    """

class Country(Flex1PropType):
    """
    A country part of the address.
    """
    pass

class LocalityElement(Flex1RolePropType):
    """
    A city/town/village etc. part of the address.
    """
    pass

    """
    address:
            <xs:element name="locality" minOccurs="0" maxOccurs="unbounded" type="Flex1RolePropType">
                <xs:annotation>
                    <xs:documentation>A city/town/village etc. part of the address.</xs:documentation>
                </xs:annotation>
            </xs:element>
            <xs:element name="area" minOccurs="0" maxOccurs="unbounded" type="Flex1RolePropType">
                <xs:annotation>
                    <xs:documentation>A subdivision of a country part of the address.</xs:documentation>
                </xs:annotation>
            </xs:element>
            <xs:element name="country" minOccurs="0" type="Flex1PropType">
                <xs:annotation>
                    <xs:documentation>A country part of the address.</xs:documentation>
                </xs:annotation>
            </xs:element>
            <xs:element name="postalCode" type="IntlStringType" minOccurs="0">
                <xs:annotation>
                    <xs:documentation>A postal code part of the address.</xs:documentation>
                </xs:annotation>
            </xs:element>
    """
    pass

class Locality(GenericArray):
    """
    A set of LocalityElement objects.
    """
    element_class = LocalityElement
