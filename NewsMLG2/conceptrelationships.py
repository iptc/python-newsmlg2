#!/usr/bin/env python
  
from lxml import etree
import json

from .core import NEWSMLG2, BaseObject, GenericArray
from .attributegroups import TimeValidityAttributes
from .propertytypes import FlexPropType

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
