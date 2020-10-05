#!/usr/bin/env python

from lxml import etree
import json

from .core import NEWSMLG2_NS, BaseObject, GenericArray


class TimeValidityAttributes(BaseObject):
    def __init__(self, **kwargs):
        super(TimeValidityAttributes, self).__init__(**kwargs)
        # TODO
        pass

    def as_dict(self):
        super(TimeValidityAttributes, self).as_dict()
        # TODO
        return self.dict


class IntlStringType(BaseObject):
    # TODO
    pass


class ConceptNameType(TimeValidityAttributes, IntlStringType):
    """
    The type of a natural language name for the concept (Type defined in this XML Schema only)
    """
    name = None
    attributes = {
        # A refinement of the semantics of the name - expressed by a QCode
        'role': 'role',
        # A refinement of the semantics of the name - expressed by a URI
        'roleuri': 'roleuri',
        # Specifies which part of a full name this property provides - expressed by a QCode
        'part': 'part',
        # Specifies which part of a full name this property provides - expressed by a URI
        'parturi': 'parturi'
    }
    
    def __init__(self, **kwargs):
        super(ConceptNameType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.name = xmlelement.text.strip()

    name_role_mappings = {
        # http://cv.iptc.org/newscodes/namerole/
        'nrol:adjectival': 'adjectival',  # http://cv.iptc.org/newscodes/namerole/adjectival
        'nrol:alternate': 'alternate',    # http://cv.iptc.org/newscodes/namerole/alternate
        'nrol:display': 'display',        # http://cv.iptc.org/newscodes/namerole/display
        'nrol:full': 'full',              # http://cv.iptc.org/newscodes/namerole/full
        'nrol:mnemonic': 'mnemonic',      # http://cv.iptc.org/newscodes/namerole/mnemonic
        'nrol:short': 'short',            # http://cv.iptc.org/newscodes/namerole/short
        'nrol:sort': 'sort',              # http://cv.iptc.org/newscodes/namerole/sort
        'nrol:synonym': 'synonym',        # http://cv.iptc.org/newscodes/namerole/synonym
        # http://cv.iptc.org/newscodes/namepart/
        'nprt:acadTitle': 'acadTitle',    # http://cv.iptc.org/newscodes/namepart/acadTitle
        'nprt:family': 'family',          # http://cv.iptc.org/newscodes/namepart/family
        'nprt:given': 'given',            # http://cv.iptc.org/newscodes/namepart/given
        'nprt:middle': 'middle',          # http://cv.iptc.org/newscodes/namepart/middle
        'nprt:salutation': 'salutation',  # http://cv.iptc.org/newscodes/namepart/salutation
        # temporary hacks while we decide what to fix
        'nprt:first': 'given',
        'nrol:first': 'given',
        'nprt:last': 'family',
        'nrol:last': 'family',
    }

    def as_dict(self):
        super(ConceptNameType, self).as_dict()
        # the only place where we diverge from a direct match with the SportsML
        role = self.attr_values.get('role', None)
        part = self.attr_values.get('part', None)
        if role and role in self.name_role_mappings.keys():
            self.dict.update({
                self.name_role_mappings[role]: self.name or ""
            })
            del self.dict['role']
        elif part and part in self.name_role_mappings.keys():
            self.dict.update({
                self.name_role_mappings[part]: self.name or ""
            })
            del self.dict['part']
        # elif self.name:
        else:
            self.dict.update({'name': self.name or ""})
        return self.dict

    def __str__(self):
        return self.name

class Names(GenericArray):
    """
    Array of ConceptNameType objects.
    """
    element_class = ConceptNameType


class FlexAttributes(BaseObject):
    """
    A group of attributes associated with flexible properties
    """
    attributes = {
        # A qualified code which identifies a concept.
        'qcode': 'qcode', # type="QCodeType"
        # A URI which identifies a concept.
        'uri': 'uri', # type="IRIType"
        # A free-text value assigned as property value.
        'literal': 'literal', # type="g2normalizedString"
        # The type of the concept assigned as controlled property value - expressed by a QCode
        'type': 'type', # type="QCodeType"
        # The type of the concept assigned as controlled property value - expressed by a URI
        'typeuri': 'typeuri', # type="IRIType"
    }


class CommonPowerAttributes(BaseObject):
    """
    A group of attributes for all elements of a G2 Item except its root
    element, the itemMeta element and all of its children which are mandatory.
    """
    attributes = {
        # The local identifier of the property.
        'id': 'id',
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a
        # QCode. If the attribute is non-empty, specifies which entity
        # (person, organisation or system) has edited the property.
        'creator': 'creator',
        # If the attribute is empty, specifies which entity (person,
        # organisation or system) will edit the property - expressed by a
        # URI. If the attribute is non-empty, specifies which entity
        # (person, organisation or system) has edited the property.
        'creatoruri': 'creatoruri',
        # The date (and, optionally, the time) when the property was last
        # modified. The initial value is the date (and, optionally, the
        # time) of creation of the property.
        'modified': 'modified',
        # If set to true the corresponding property was added to the G2
        # Item for a specific customer or group of customers only. The
        # default value of this property is false which applies when this
        #  attribute is not used with the property.
        'custom': 'custom',
        # Indicates by which means the value was extracted from the
        # content - expressed by a QCode
        'how': 'how',
        # Indicates by which means the value was extracted from the
        # content - expressed by a URI
        'howuri': 'howuri',
        # Why the metadata has been included - expressed by a QCode
        'why': 'why',
        # Why the metadata has been included - expressed by a URI
        'whyuri': 'whyuri',
        # One or many constraints that apply to publishing the value of
        # the property - expressed by a QCode. Each constraint applies
        # to all descendant elements.
        'pubconstraint': 'pubconstraint',
        # One or many constraints that apply to publishing the value of
        # the property - expressed by a URI. Each constraint applies to
        # all descendant elements.
        'pubconstrainturi': 'pubconstrainturi'
    }


class I18NAttributes(BaseObject):
    """
    A group of attributes for language and script related information
    """
    attributes = {
        # Specifies the language of this property and potentially all
        # descendant properties. xml:lang values of descendant properties
        # override this value. Values are determined by Internet BCP 47.
        'xml:lang': 'xmlLang',
        # The directionality of textual content
        # (enumeration: ltr, rtl)
        'dir': 'dir'
    }


class TruncatedDateTimeType(CommonPowerAttributes):
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
        self.dict.update({self.element_name: self.date_time })
        return self.dict


class TruncatedDateTimePropType(CommonPowerAttributes):
    """
    The type of a calendar date with an optional time part which
    may be truncated from the seconds part to the month part
    """
    pass
    """
            <xs:extension base="TruncatedDateTimeType">
                <xs:attributeGroup ref="commonPowerAttributes" />
                <xs:anyAttribute namespace="##other" processContents="lax" />
            </xs:extension>
    """


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
                xmlarray = xmlelement.findall(NEWSMLG2_NS+'name')
            )
            self.definition = xmlelement.findtext(NEWSMLG2_NS+'definition')
            self.note = xmlelement.findtext(NEWSMLG2_NS+'note')
            self.facet = xmlelement.findtext(NEWSMLG2_NS+'facet')
            self.remote_info= xmlelement.findtext(NEWSMLG2_NS+'remoteInfo')
            self.hierarchy_info = xmlelement.findtext(NEWSMLG2_NS+'hierarchyInfo')

    def as_dict(self):
        super(ConceptDefinitionGroup, self).as_dict()
        if self.names:
            self.dict.update({'names': self.names.as_dict() })
        if self.definition:
            self.dict.update({'definition': self.definition })
        if self.note:
            self.dict.update({'note': self.note })
        if self.facet:
            self.dict.update({'facet': self.facet })
        if self.remote_info:
            self.dict.update({'remoteInfo': self.remote_info })
        if self.hierarchy_info:
            self.dict.update({'hierarchyInfo': self.hierarchy_info })
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


class FlexPropType(CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible generic type for both controlled and uncontrolled values
    """
    def __init__(self, **kwargs):
        super(FlexPropType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.names = Names(
                xmlarray = xmlelement.findall(NEWSMLG2_NS+'name')
            )
            # TODO hierarchyInfo

    def as_dict(self, **kwargs):
        super(FlexPropType, self).as_dict()
        if self.names:
            self.dict.update({'names': self.names.as_dict() })
        return self.dict


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
                # note camelCase element name, this is correct
                xmlelement = xmlelement.find(NEWSMLG2_NS+'geoAreaDetails')
            )
            self.poi_details = POIDetails(
                # note case of element name, this is correct
                xmlelement = xmlelement.find(NEWSMLG2_NS+'POIDetails')
            )

    def as_dict(self):
        super(FlexLocationPropType, self).as_dict()
        if self.geo_area_details:
            self.dict.update({'geoAreaDetails': self.geo_area_details.as_dict() })
        if self.poi_details:
            self.dict.update({'POIDetails': self.poi_details.as_dict() })
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


class Flex1PropType(ConceptDefinitionGroup, ConceptRelationshipsGroup, CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible generic PCL-type for both controlled and uncontrolled values
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
                            <xs:attribute name="radius" type="xs:double" use="required">
                                <xs:annotation>
                                    <xs:documentation>The radius of the circle</xs:documentation>
                                </xs:annotation>
                            </xs:attribute>
                            <xs:attribute name="radunit" type="QCodeType">
                                <xs:annotation>
                                    <xs:documentation>The dimension unit of the radius - expressed by a QCode / either the radunit or the radunituri attribute MUST be used</xs:documentation>
                                </xs:annotation>
                            </xs:attribute>
                            <xs:attribute name="radunituri" type="IRIType">
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
                            <xs:attribute name="role" type="QCodeType">
                                <xs:annotation>
                                    <xs:documentation>Refines the semantics of line - expressed by a QCode</xs:documentation>
                                </xs:annotation>
                            </xs:attribute>
                            <xs:attribute name="roleuri" type="IRIType">
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


class Country(Flex1PropType):
    """
    A country part of the address.
    """
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
                xmlarray = xmlelement.findall(NEWSMLG2_NS+'line')
            )
            self.localities = Localities(
                xmlarray = xmlelement.findall(NEWSMLG2_NS+'locality')
            )
            self.areas = Areas(
                xmlarray = xmlelement.findall(NEWSMLG2_NS+'area')
            )
            self.country = Country(
                xmlelement = xmlelement.find(NEWSMLG2_NS+'country')
            )
            self.postal_code = PostalCode(
                xmlelement = xmlelement.find(NEWSMLG2_NS+'postal-code')
            )

    def as_dict(self):
        super(Address, self).as_dict()
        if self.lines:
            self.dict.update({'lines': self.lines.as_dict() })
        if self.localities:
            self.dict.update({'localities': self.localities.as_dict() })
        if self.areas:
            self.dict.update({'areas': self.areas.as_dict() })
        if self.country:
            self.dict.update({'country': self.country.as_dict() })
        if self.postal_code:
            self.dict.update({'postalCode': self.postal_code.as_dict() })
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
                xmlelement = xmlelement.find(NEWSMLG2_NS+'address')
            )
        # TODO finish this

    def as_dict(self):
        super(POIDetails, self).as_dict()
        if self.address:
            self.dict.update({'address': self.address.as_dict() })
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


class Locality(Flex1RolePropType):
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


class Localities(GenericArray):
    """
    A set of Locality objects.
    """
    element_class = Locality


class SameAs(FlexPropType, TimeValidityAttributes):
    """
    The type for an identifier of an equivalent concept (Type defined in this XML Schema only)
    """
    pass


class RelatedConceptType(BaseObject):
    """
    The type for an identifier of a related concept
    """
    pass

    """
    <xs:element name="sameAs" type="SameAsType">
    </xs:element>
    <xs:element name="broader" type="RelatedConceptType">
        <xs:annotation>
            <xs:documentation>An identifier of a more generic concept.</xs:documentation>
        </xs:annotation>
    </xs:element>
    <xs:element name="narrower" type="RelatedConceptType">
        <xs:annotation>
            <xs:documentation>An identifier of a more specific concept.</xs:documentation>
        </xs:annotation>
    </xs:element>
    <xs:element name="related" type="FlexRelatedConceptType">
        <xs:annotation>
            <xs:documentation>A related concept, where the relationship is different from 'sameAs', 'broader' or 'narrower'.</xs:documentation>
        </xs:annotation>
    </xs:element>
    """

class CatalogRef(BaseObject):
    """
    A reference to a remote catalog. A hyperlink to a set of scheme alias declarations.
    """
    attributes = {
        # A short natural language name for the catalog.
        'title': 'title',
        # A hyperlink to a remote Catalog.
        'href': 'href'
    }


class CatalogRefs(GenericArray):
    """
    A reference to document(s) listing externally-supplied controlled vocabularies.
    The catalog file can be in NewsML 1.
    """
    element_class = CatalogRef


class QualRelPropType(CommonPowerAttributes):
    attributes = {
        # A qualified code which identifies a concept  - either the  qcode or the uri attribute MUST be used
        'qcode': 'qcode',
        # A URI which identifies a concept  - either the  qcode or the uri attribute MUST be used
        'uri': 'uri'
    }

    def getQcode(self):
        qcode = self.get_attr('qcode')
        if qcode:
            return qcode
        else:
            raise NotImplementedError("TODO: convert URI to qcode using catalog")

    def getURI(self):
        uri = self.get_attr('uri')
        if uri:
            return uri
        else:
            raise NotImplementedError("TODO: convert qcode to URI using catalog")

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

    def getQcode(self):
        qcode = self.get_attr('qcode')
        if qcode:
            return qcode
        else:
            return "TODO: convert qcode to URI using catalog"

    def getURI(self):
        uri = self.get_attr('uri')
        if uri:
            return uri
        else:
            raise NotImplementedError("TODO: convert URI to qcode using catalog")

class DateTimePropType(CommonPowerAttributes):
    """
    The type of a property with date and time
    In XML Schema, extends xsd:dateTime
    """
    def __init__(self, **kwargs):
        super(DateTimePropType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.datetime = kwargs['xmlelement'].text.strip()

    def __str__(self):
        return self.datetime

    def getDateTime(self):
        return self.datetime

    # TODO add helper methods for date/time manipulation, timezone conversion etc
    pass



class BlockType(CommonPowerAttributes, I18NAttributes):
    """
    The type for nformation about the content as natural language string with minimal markup and line breaks
    """
    attributes = {
        # An indication of the target media type(s) values as defined by the Cascading Style Sheets (CSS) specification.
        'media': 'media', # type="xs:NMTOKENS" 
        # A refinement of the semantics of the block.
        'role': 'role', # type="QCodeListType"
        # A URI identifying the refined semantics of the definition.
        'roleuri': 'roleuri', # type="IRIType"
    }

    def __init__(self, **kwargs):
        super(BlockType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            pass

            """
            # TODO: implement these block elements, or just store everything as a block?
              <xs:choice minOccurs="0" maxOccurs="unbounded">
                 <xs:element ref="a"/>
                 <xs:element ref="span"/>
                 <xs:element ref="ruby"/>
                 <xs:element ref="br"/>
                 <xs:element ref="inline"/>
              </xs:choice>
            """


class RightsBlockType(BlockType):
    """
    An expression of rights in natural language or as a reference to remote information
    """
    attributes = {
        # The locator of a remote expression of rights
        'href': 'href', # type="IRIType"
    }
    def __init__(self, **kwargs):
        super(RightsBlockType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if xmlelement.text:
            self.text = xmlelement.text.strip()

    def __str__(self):
        return self.text


