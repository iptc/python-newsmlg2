#!/usr/bin/env python

"""
NAR Property Types
"""

from lxml import etree
from .catalogstore import CATALOG_STORE
from .core import NEWSMLG2, BaseObject, QCodeURIMixin
from .complextypes import IntlStringType, Name
from .concepts import HierarchyInfo
from .attributegroups import (
    CommonPowerAttributes, FlexAttributes, I18NAttributes
)


class QCodePropType(QCodeURIMixin, CommonPowerAttributes):
    """
    The type for a property with a QCode value in a qcode attribute
    """

class QualPropType(QCodePropType, I18NAttributes):
    """
    Type type for a property with a  QCode value in a qcode attribute, a URI in a
    uri attribute and optional names
    """

    elements = {
        'name': { 'type': 'array', 'xml_name': 'name', 'element_class': Name },
        'hierarchyinfo': { 'type': 'array', 'xml_name': 'hierarchyInfo', 'element_class': HierarchyInfo }
    }


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
