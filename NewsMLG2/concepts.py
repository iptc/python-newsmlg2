"""
Handle concepts, including concept names.
"""

from .core import BaseObject, GenericArray, QCodeURIMixin
from .attributegroups import (
    CommonPowerAttributes, FlexAttributes,
    I18NAttributes, QualifyingAttributes, QuantifyAttributes,
    TimeValidityAttributes
)
from .complextypes import (
    ConceptNameType, Name, TruncatedDateTimePropType
)
from .conceptrelationships import (
    Bag, ConceptRelationshipsGroup, Facet, FacetConcept,
    HierarchyInfo, MainConcept, QCodePropType
)
from .labeltypes import BlockType, Label1Type


class DefinitionElement(BlockType, TimeValidityAttributes):
    """
    A natural language definition of the semantics of the concept. This
    definition is normative only for the scope of the use of this concept.
    """

class Definition(GenericArray):
    """
    Array of DefinitionElement objects.
    """
    element_class = ConceptNameType


class NoteElement(BlockType, TimeValidityAttributes):
    """
    Additional natural language information about the concept.
    """


class Note(GenericArray):
    """
    Array of NoteElement objects.
    """
    element_class = ConceptNameType


class ConceptDefinitionGroup(BaseObject):
    """
    A group of properites required to define the concept
    """

    elements = {
        'name': { 'type': 'array', 'xml_name': 'name', 'element_class': Name },
        'definition': {
            'type': 'array', 'xml_name': 'definition',
            'element_class': Definition
        },
        'note': { 'type': 'array', 'xml_name': 'note', 'element_class': Note},
        'facet': {
            'type': 'array', 'xml_name': 'facet', 'element_class': Facet
        },
        'remoteinfo': {
            'type': 'array', 'xml_name': 'remoteInfo',
            'element_class': 'link.RemoteInfo'
        },
        'hierarchyinfo': {
            'type': 'array', 'xml_name': 'hierarchyInfo',
            'element_class': HierarchyInfo
        }
    }


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


class Flex1ConceptPropType(Flex1PropType, QuantifyAttributes):
    """
    Flexible generic PCL-type for both controlled and uncontrolled values, with
    optional attributes
    """

    elements = {
        'bag': { 'type': 'single', 'xml_name': 'bag', 'element_class': Bag },
        'main_concept': {
            'type': 'single', 'xml_name': 'mainConcept',
            'element_class': MainConcept
        },
        'facet_concept': {
            'type': 'array', 'xml_name': 'facetConcept',
            'element_class': FacetConcept
        }
    }

class FlexPersonPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible person data type for both controlled and uncontrolled values
    """

    elements = {
        'person_details': {
            'type': 'single', 'xml_name': 'personDetails',
            'element_class': 'entities.PersonDetails'
        }
    }


class FlexOrganisationPropType(ConceptDefinitionGroup,
    ConceptRelationshipsGroup, CommonPowerAttributes, QualifyingAttributes,
    I18NAttributes):
    """
    Flexible organisation data type for both controlled and uncontrolled values
    """

    elements = {
        'organisation_details': {
            'type': 'single', 'xml_name': 'organisationDetails',
            'element_class': 'entities.OrganisationDetails'
        }
    }


class FlexPartyPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup,
    CommonPowerAttributes, FlexAttributes, I18NAttributes, QCodeURIMixin):
    """
    Flexible party (person or organisation) PCL-type for both controlled and
    uncontrolled values
    """
    elements = {
        'person_details': {
            'type': 'single', 'xml_name': 'personDetails',
            'element_class': 'entities.PersonDetails'
        },
        'organisation_details': {
            'type': 'single', 'xml_name': 'organisationDetails',
            'element_class': 'entities.OrganisationDetails'
        }
    }


class Party(FlexPartyPropType):
    """
    A party involved this hop of the Hop History
    (Defined as part of AnyItem)
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


class GeoCoordinatesType(CommonPowerAttributes):
    """
    The type for geographic coordinates (Type defined in this XML Schema only)
    """
    attributes = {
        # The latitude in decimal degrees.
        'latitude': 'latitude',  # type="xs:decimal" use="required">
        # The longitude in decimal degrees.
        'longitude': 'longitude',  # type="xs:decimal" use="required">
        # The altitude in meters above the zero elevation of the reference system (sea level).
        'altitude': 'altitude',  # type="xs:integer" use="optional">
        # The GPS datum associated with the measure.
        'gpsdatum': 'gpsdatum'  # type="xs:string" use="optional">
    }


class PositionElement(GeoCoordinatesType):
    """
    The coordinates of the location
    """


class Position(GenericArray):
    """
    An array of PositionElement objects.
    """
    element_class = PositionElement


class GeoAreaFounded(TruncatedDateTimePropType):
    """
    The date the geopolitical area was founded/established.
    """


class GeoAreaDissolved(TruncatedDateTimePropType):
    """
    The date the geopolitical area was dissolved.
    """


class GeoAreaLineElement(CommonPowerAttributes):
    """
    A line as a geographic area
    """
    elements = {
        'position': { 'type': 'array', 'xml_name': 'position', 'element_class': Position },
    }


class GeoAreaLine(GenericArray):
    """
    An array of GeoAreaLineElement objects.
    """
    element_class = GeoAreaLineElement


class GeoAreaCircleElement(CommonPowerAttributes):
    """
    A circle as a geographic area
    """
    elements = {
        'position': { 'type': 'array', 'xml_name': 'position', 'element_class': Position },
    }
    attributes = {
        # The radius of the circle
        'radius': 'radius',  # type="xs:double" use="required">
        # The dimension unit of the radius - expressed by a QCode /
        # either the radunit or the radunituri attribute MUST be used
        'radunit': 'radunit',  # type="QCodeType">
        # The dimension unit of the radius - expressed by a URI /
        # either the radunit or the radunituri attribute MUST be used
        'radunituri': 'radunituri'  # type="IRIType">
    }


class GeoAreaCircle(GenericArray):
    """
    An array of GeoAreaCircleElement objects.
    """
    element_class = GeoAreaCircleElement


class GeoAreaPolygonElement(CommonPowerAttributes):
    """
    A polygon as a geographic area
    """
    elements = {
        'position': { 'type': 'array', 'xml_name': 'position', 'element_class': Position },
    }


class GeoAreaPolygon(GenericArray):
    """
    An array of GeoAreaPolygonElement objects.
    """
    element_class = GeoAreaPolygonElement


class GeoAreaDetails(CommonPowerAttributes):
    """
    A group of properties specific to a geopolitical area
    """
    elements = {
        'position': {
            'type': 'single', 'xml_name': 'position',
            'element_class': PositionElement
        },
        'founded': {
            'type': 'single', 'xml_name': 'founded',
            'element_class': GeoAreaFounded
        },
        'dissolved': {
            'type': 'single', 'xml_name': 'dissolved',
            'element_class': GeoAreaDissolved
        },
        'line': {
            'type': 'array', 'xml_name': 'line', 'element_class': GeoAreaLine
        },
        'circle': {
            'type': 'array', 'xml_name': 'circle',
            'element_class': GeoAreaCircle
        },
        'polygon': {
            'type': 'array', 'xml_name': 'polygon',
            'element_class': GeoAreaPolygon
        }
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
            'element_class': 'concepts.POIDetails'
        }
    }

    def __bool__(self):
        return self.geo_area_details is not None or self.poi_details is not None


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
            'element_class': 'concepts.POIDetails'
        }
    }


class OpenHours(Label1Type):
    """
    Opening hours of the point of interest expressed in natural language
    """


class Capacity(Label1Type):
    """
    Total capacity of the point of interest expressed in natural language
    """


class AccessElement(BlockType):
    """
    Ways to access the place of the point of  interest, including directions.
    """


class Access(GenericArray):
    """
    Array of AccessElement objects.
    """
    element_class = AccessElement


class DetailsElement(BlockType):
    """
    Detailed information about the precise location of the Point of Interest.
    """


class Details(GenericArray):
    """
    Array of DetailsElement objects.
    """
    element_class = DetailsElement


class POICreated(TruncatedDateTimePropType):
    """
    The date (and optionally the time) on which this Point of Interest was created
    """


class POICeasedToExist(TruncatedDateTimePropType):
    """
    The date (and optionally the time) on which this Point of Interest ceased to exist
    """


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


class POIDetails(CommonPowerAttributes):
    """
    A group of properties specific to a point of interest
    """
    elements = {
        'position': {
            'type': 'single', 'xml_name': 'position',
            'element_class': PositionElement
        },
        'address': {
            'type': 'single', 'xml_name': 'address',
            'element_class': 'entities.Address'
        },
        'openhours': {
            'type': 'single', 'xml_name': 'openHours',
            'element_class': OpenHours
        },
        'capacity': {
            'type': 'single', 'xml_name': 'capacity', 'element_class': Capacity
        },
        'contactinfo': {
            'type': 'array', 'xml_name': 'contactInfo',
            'element_class': 'entities.ContactInfo'
        },
        'access': {
            'type': 'array', 'xml_name': 'access', 'element_class': Access
        },
        'details': {
            'type': 'array', 'xml_name': 'details', 'element_class': Details
        },
        'created': {
            'type': 'single', 'xml_name': 'created', 'element_class': POICreated
        },
        'ceasedtoexist': {
            'type': 'single', 'xml_name': 'ceasedToExist',
            'element_class': POICeasedToExist
        },
    }


class ConceptIdType(QCodeURIMixin, CommonPowerAttributes):
    """
    The type for a preferred unambiguous identifier for the concept.
    """
    attributes = {
        # The date (and, optionally, the time) when the concept identifier was
        # created.
        'created': 'created',  # type="DateOptTimeType" use="optional">
        # The date (and, optionally, the time) after which the concept
        # identifier should not be applied as the value of a property anymore.
        'retired': 'retired'  # type="DateOptTimeType" use="optional">
    }


class ConceptId(ConceptIdType):
    """
    The preferred unambiguous identifier for the concept.
    """


class QualPropType(QCodePropType, I18NAttributes):
    """
    Type type for a property with a  QCode value in a qcode attribute, a URI in a
    uri attribute and optional names
    """

    elements = {
        'name': { 'type': 'array', 'xml_name': 'name', 'element_class': Name },
        'hierarchyinfo': {
            'type': 'array', 'xml_name': 'hierarchyInfo',
            'element_class': HierarchyInfo
        }
    }


class Type(QualPropType):
    """
    The nature of the concept.
    """


class EntityDetailsGroup(BaseObject):
    """
    A group of properties to define the details of specific entities
    """

    elements = {
        'persondetails': {
            'type': 'single', 'xml_name': 'personDetails',
            'element_class': 'entities.PersonDetails'
        },
        'organisationDetails': {
            'type': 'single', 'xml_name': 'organisationDetails',
            'element_class': 'entities.OrganisationDetails'
        },
        'geoareadetails': {
            'type': 'single', 'xml_name': 'geoAreaDetails',
            'element_class': GeoAreaDetails
         },
        'poidetails': {
            'type': 'single', 'xml_name': 'POIDetails',
            'element_class': POIDetails
        },
        'objectdetails': {
            'type': 'single', 'xml_name': 'objectDetails',
            'element_class': 'entities.ObjectDetails'
        }
        # TODO
        # 'eventdetails': {
        #     'type': 'single', 'xml_name': 'eventDetails',
        #     'element_class': EventDetails
        # }
    }


class ConceptElement(ConceptRelationshipsGroup, EntityDetailsGroup,
    CommonPowerAttributes, I18NAttributes):
    """
    A set of properties defining a concept
    """

    elements = {
        'conceptid': {
            'type': 'single', 'xml_name': 'conceptId',
            'element_class': ConceptId
        },
        'type': { 'type': 'single', 'xml_name': 'type', 'element_class': Type },
        'name': { 'type': 'array', 'xml_name': 'name', 'element_class': Name },
        'definition': {
            'type': 'array', 'xml_name': 'definition',
            'element_class': Definition
        },
        'note': { 'type': 'array', 'xml_name': 'note', 'element_class': Note },
        'facet': { 'type': 'array', 'xml_name': 'facet', 'element_class': Facet },
        'remoteinfo': {
            'type': 'array', 'xml_name': 'remoteInfo',
            'element_class': 'link.RemoteInfo'
        },
        'hierarchyinfo': {
            'type': 'array', 'xml_name': 'hierarchyInfo',
            'element_class': HierarchyInfo
        },
        'conceptextproperty': {
            'type': 'single', 'xml_name': 'conceptExtProperty',
            'element_class': 'extensionproperties.ConceptExtProperty'
        }
    }

class Concept(GenericArray):
    """
    An array of ConceptElement objects.
    """
    element_class = ConceptElement
