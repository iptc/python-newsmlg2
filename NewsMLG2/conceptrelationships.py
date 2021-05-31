#!/usr/bin/env python
  
from lxml import etree
import json

from .core import NEWSMLG2, BaseObject, GenericArray
from .attributegroups import (
    ArbitraryValueAttributes, CommonPowerAttributes, FlexAttributes,
    I18NAttributes, QuantifyAttributes, TimeValidityAttributes
)
from .complextypes import Name
from .concepts import HierarchyInfo, Definition
from .propertytypes import QCodePropType


class FlexPropType(CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible generic type for both controlled and uncontrolled values
    """

    elements = {
        'name': { 'type': 'array', 'xml_name': 'name', 'element_class': Name },
        'hierarchyinfo': { 'type': 'array', 'xml_name': 'hierarchyInfo', 'element_class': HierarchyInfo }
    }

    # TODO move this to a generic method in BaseObject
    def as_dict(self, **kwargs):
        super().as_dict()
        if self.names:
            self.dict.update({'names': self.names.as_dict()})
        return self.dict


class RelatedConceptType(BaseObject):
    """
    The type for an identifier of a related concept
    """

    """
    TODO
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

class MainConcept(RelatedConceptType):
    """
    The concept which is faceted by other concept(s) asserted by facetConcept
    """


class FacetConcept(RelatedConceptType):
    """
    The concept which is faceting another concept asserted by mainConcept
    """


class SameAsType(FlexPropType, TimeValidityAttributes):
    """
    The type for an identifier of an equivalent concept (Type defined in this XML Schema only)
    """
    pass


class SameAs(SameAsType):
    """
    An identifier of a concept with equivalent semantics
    """


class Broader(RelatedConceptType):
    """
    An identifier of a more generic concept.
    """


class Narrower(RelatedConceptType):
    """
    An identifier of a more specific concept.
    """


class Bag(QCodePropType, QuantifyAttributes):
    """
    A group of existing concepts which express a new concept.
    """

    attributes = {
        # The type of the concept assigned as controlled property value - expressed by a QCode</xs:documentation>
        'type': 'type',  # " type="QCodeType">
        # The type of the concept assigned as controlled property value - expressed by a URI</xs:documentation>
        'typeuri': 'typeuri',  # " type="IRIType">
        # Indicates how significant the event expressed by a bit of event concept type is to the concept expressed by this bit The scope of this relationship is limited to the bits of a single bag. See also the note below the table.</xs:documentation>
        'significance': 'significance'  # " type="Int100Type">
    }


class FacetElement(FlexPropType, TimeValidityAttributes):
    """
    In NAR 1.8 and later, facet is deprecated and SHOULD NOT (see RFC 2119) be
    used, the "related" property should be used instead.
    (was: An intrinsic property of the concept.)
    """
    attributes = {
        # The identifier of the relationship between the current concept (containing the facet) and the concept identified by the facet value - expressed by a QCode</xs:documentation>
        'rel': 'rel',  #  type="QCodeType" use="optional">
        # The identifier of the relationship between the current concept (containing the facet) and the concept identified by the facet value - expressed by a URI</xs:documentation>
        'reluri': 'reluri',  #  type="IRIType" use="optional">
        # DO NOT USE this attribute, for G2 internal maintenance purposes only.</xs:documentation>
        'g2flag': 'g2flag'  #  type="xs:string" use="optional" fixed="DEPR">
    }


class Facet(GenericArray):
    """
    Array of FacetElement objects.
    """
    element_class = FacetElement


class FlexRelatedConceptType(RelatedConceptType, ArbitraryValueAttributes):
    """
    The type for identifying a related concept
    """
    elements = {
        'bag': { 'type': 'single', 'xml_name': 'bag', 'element_class': Bag }
    }


class Related(FlexRelatedConceptType):
    """
    A related concept, where the relationship is different from 'sameAs',
    'broader' or 'narrower'.
    """


class QualRelPropType(QCodePropType, I18NAttributes):
    """
    Type for a property with a  QCode value in a qcode attribute, a URI in
    a uri attribute and optional names and related concepts
    """

    elements = {
        'name': { 'type': 'array', 'xml_name': 'name', 'element_class': Name },
        'hierarchyinfo': { 'type': 'array', 'xml_name': 'hierarchyInfo', 'element_class': HierarchyInfo },
        'related': { 'type': 'array', 'xml_name': 'related', 'element_class': Related },
    }


class FlexProp2Type(CommonPowerAttributes, FlexAttributes, I18NAttributes):
    """
    Flexible type for related concepts for both controlled and uncontrolled values
    """

    elements = {
        'name': { 'type': 'array', 'xml_name': 'name', 'element_class': Name },
        'hierarchyinfo': { 'type': 'array', 'xml_name': 'hierarchyInfo', 'element_class': HierarchyInfo },
        'sameAs': { 'type': 'array', 'xml_name': 'sameAs', 'element_class': SameAs },
    }

    # TODO move this to a generic method in BaseObject
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


class ConceptRelationshipsGroup(BaseObject):
    """
    A group of properites required to indicate relationships of the concept
    to other concepts
    """

    elements = {
        'same_as': { 'type': 'array', 'xml_name': 'sameAs', 'element_class': SameAs },
        'broader': { 'type': 'array', 'xml_name': 'broader', 'element_class': Broader },
        'narrower': { 'type': 'array', 'xml_name': 'broader', 'element_class': Narrower },
        'related': { 'type': 'array', 'xml_name': 'related', 'element_class': Related }
    }
