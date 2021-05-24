#!/usr/bin/env python

# NAR Property Types

from .catalogstore import CATALOG_STORE

from .core import NSMAP, NEWSMLG2, BaseObject, GenericArray
from .complextypes import (
    IntlStringType
)
from .concepts import Names
from .complextypes import *
from .attributegroups import *

#from .attributegroups import (
#    ArbitraryValueAttributes, CommonPowerAttributes, FlexAttributes, I18NAttributes, QualifyingAttributes, QuantifyAttributes, TimeValidityAttributes
#)
from .conceptgroups import (
    ConceptDefinitionGroup, ConceptRelationshipsGroup
)

class QCodePropType(CommonPowerAttributes):
    """
    The type for a property with a QCode value in a qcode attribute
    """
    attributes = {
        # A qualified code which identifies a concept  - either the qcode or
        # the uri attribute MUST be used
        'qcode': 'qcode',
        # A URI which identifies a concept  - either the  qcode or the uri
        # attribute MUST be used
        'uri': 'uri'
    }

    def getQcode(self):
        #global CATALOG_STORE
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
            # raise NotImplementedError("TODO: convert URI to qcode using catalog")

    def getURI(self):
        global CATALOG_STORE
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


class QualPropType(QCodePropType, I18NAttributes):
    """
    Type type for a property with a  QCode value in a qcode attribute, a URI in a
    uri attribute and optional names
    """

    def __init__(self, **kwargs):
        super(QualPropType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.names = Names(
                xmlarray=xmlelement.findall(NEWSMLG2+'name')
            )
            # TODO hierarchyInfo

    def as_dict(self, **kwargs):
        super(FlexPropType, self).as_dict()
        if self.names:
            self.dict.update({'names': self.names.as_dict()})
        return self.dict

    """
    TODO:
    <xs:choice minOccurs="0" maxOccurs="unbounded">
        <!-- NAR1.1 rev3 : use newly defined global name -->
        <xs:element ref="name"/>
        <xs:element ref="hierarchyInfo"/>
    </xs:choice>
    """


class QualRelPropType(QCodePropType, I18NAttributes):
    """
    Type for a property with a  QCode value in a qcode attribute, a URI in
    a uri attribute and optional names and related concepts

    TODO:
    <xs:choice minOccurs="0" maxOccurs="unbounded">
        <xs:element ref="name"/>
        <xs:element ref="hierarchyInfo"/>
        <xs:element ref="related"/>
    </xs:choice>
    """
    pass


class TypedQualPropType(QualPropType):
    """
    The type for a property with a QCode, a type and optional names
    """
    attributes = {
        # The type of the concept assigned as property value - expressed by a QCode
        'type': 'type',  # type="QCodeType" use="optional">
        # The type of the concept assigned as property value - expressed by a URI
        'typeuri': 'typeuri',  # type="IRIType" use="optional">
    }


class FlexPropType(CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible generic type for both controlled and uncontrolled values
    """

    def __init__(self, **kwargs):
        super(FlexPropType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.names = Names(
                xmlarray=xmlelement.findall(NEWSMLG2+'name')
            )
            # TODO hierarchyInfo

    def as_dict(self, **kwargs):
        super(FlexPropType, self).as_dict()
        if self.names:
            self.dict.update({'names': self.names.as_dict()})
        return self.dict


class FlexProp2Type(CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible type for related concepts for both controlled and uncontrolled values
    """

    def __init__(self, **kwargs):
        super(FlexProp2Type, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.names = Names(
                xmlarray=xmlelement.findall(NEWSMLG2+'name')
            )
            """
            TODO
            <xs:choice minOccurs="0" maxOccurs="unbounded">
                <xs:element ref="name"/>
                <xs:element ref="hierarchyInfo"/>
                <xs:element ref="sameAs"/>
            </xs:choice>
            """

    def as_dict(self, **kwargs):
        super(FlexProp2Type, self).as_dict()
        if self.names:
            self.dict.update({'names': self.names.as_dict()})
        return self.dict


class FlexRelatedPropType(FlexProp2Type):
    """
    Flexible generic type for both controlled and uncontrolled values of a related concept
    """
    attributes = {
        # The identifier of the relationship between the concept containing the related property and the concept identified by the related value - expressed by a QCode
        'rel': 'rel',  # type="QCodeType" use="optional">
        # The identifier of the relationship between the concept containing the related property and the concept identified by the related value - expressed by a URI
        'reluri': 'reluri',  # type="IRIType" use="optional">
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

    pass
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
                                    <xs:documentation>The dimension unit of the radius - expressed by a QCode / either the radunit or the radunituri attribute MUST be used</xs:documentation>
                                </xs:annotation>
                            </xs:attribute>
                            'radunituri': 'radunituri', # type="IRIType">
                                <xs:annotation>
                                    <xs:documentation>The dimension unit of the radius - expressed by a URI / either the radunit or the radunituri attribute MUST be used</xs:documentation>
                                </xs:annotation>
                            </xs:attribute>
                        </xs:complexType>
                    </xs:element>
                    <xs:element name="polygon">
                        <xs:annotation>
                            <xs:documentation>A polygon as a geographic area</xs:documentation>
                        </xs:annotation>
                        <xs:complexType>
                            <xs:sequence>
                                <xs:element ref="position" maxOccurs="unbounded" />
                            </xs:sequence>
                            <xs:attributeGroup ref="commonPowerAttributes" />
                        </xs:complexType>
                    </xs:element>
                </xs:choice>
                <xs:any namespace="##other" processContents="lax" minOccurs="0" maxOccurs="unbounded">
                    <xs:annotation>
                        <xs:documentation>Extension point for provider-defined properties from other namespaces</xs:documentation>
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
                                    <xs:documentation>Refines the semantics of line - expressed by a QCode</xs:documentation>
                                </xs:annotation>
                            </xs:attribute>
                            'roleuri': 'roleuri', # type="IRIType">
                                <xs:annotation>
                                    <xs:documentation>Refines the semantics of line - expressed by a URI</xs:documentation>
                                </xs:annotation>
                            </xs:attribute>
                        </xs:extension>
                    </xs:complexContent>
                </xs:complexType>
            </xs:element>
    """
    pass


class Areas(BaseObject):
    pass


class PostalCode(IntlStringType):
    """
    A postal code part of the address.
    """
    pass


class Address(CommonPowerAttributes):
    attributes = {
        # A refinement of the semantics of the postal address - expressed by a QCode
        'role': 'role',
        # A refinement of the semantics of the postal address - expressed by a URI
        'roleuri': 'roleuri'
    }
    # A line of address information, in the format expected by a recipient postal service. City, country area, country and postal code are expressed separately.
    lines = None
    localities = None
    # A subdivision of a country part of the address.
    areas = None
    # A country part of the address.
    country = None
    # A postal code part of the address.
    postal_code = None

    def __init__(self, **kwargs):
        super(Address, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.lines = Lines(
                xmlarray=xmlelement.findall(NEWSMLG2+'line')
            )
            self.localities = Localities(
                xmlarray=xmlelement.findall(NEWSMLG2+'locality')
            )
            self.areas = Areas(
                xmlarray=xmlelement.findall(NEWSMLG2+'area')
            )
            self.country = Country(
                xmlelement=xmlelement.find(NEWSMLG2+'country')
            )
            self.postal_code = PostalCode(
                xmlelement=xmlelement.find(NEWSMLG2+'postal-code')
            )

    def as_dict(self):
        super(Address, self).as_dict()
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
    # The date (and optionally the time) on which this Point of Interest was created
    created = None
    # The date (and optionally the time) on which this Point of Interest ceased to exist
    ceased_to_exist = None

    def __init__(self, **kwargs):
        super(POIDetails, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.address = Address(
                xmlelement=xmlelement.find(NEWSMLG2+'address')
            )
        # TODO finish this

    def as_dict(self):
        super(POIDetails, self).as_dict()
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
                <xs:element name="created" type="TruncatedDateTimePropType" minOccurs="0">
                <xs:element name="ceasedToExist" type="TruncatedDateTimePropType" minOccurs="0">
            </xs:sequence>
            <xs:attributeGroup ref="commonPowerAttributes" />
        </xs:complexType>
    """
