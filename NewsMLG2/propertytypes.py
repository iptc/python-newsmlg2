#!/usr/bin/env python

"""
NAR Property Types
"""

from lxml import etree
from .catalogstore import CATALOG_STORE
from .core import NEWSMLG2, BaseObject, QCodeURIMixin
from .complextypes import (
    IntlStringType
)
from .concepts import Names
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

    def __init__(self, **kwargs):
        super(QualPropType, self).__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            self.names = Names(
                xmlarray=xmlelement.findall(NEWSMLG2+'name')
            )
            # TODO hierarchyInfo

    def as_dict(self, **kwargs):
        super(QualPropType, self).as_dict()
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
