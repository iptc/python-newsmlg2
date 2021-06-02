#!/usr/bin/env python

"""
Elements for handling rights management
"""

from lxml import etree
import json

from .core import NEWSMLG2, BaseObject, GenericArray
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, TimeValidityAttributes
)
from .conceptgroups import FlexPartyPropType, FlexPersonPropType, Flex2ExtPropType
from .labeltypes import BlockType
from .link import Link


class RightsBlockType(BlockType):
    """
    An expression of rights in natural language or as a reference to remote information
    """
    attributes = {
        # The locator of a remote expression of rights
        'href': 'href',  # type="IRIType"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        xmlelement = kwargs.get('xmlelement')
        if xmlelement.text:
            self.text = xmlelement.text.strip()

    def __str__(self):
        return self.text


class CopyrightHolder(FlexPartyPropType):
    """
    The person or organisation claiming the intellectual property for the content.
    """

class CopyrightNoticeElement(RightsBlockType):
    """
    Any necessary copyright notice for claiming the intellectual property for the content.
    """

class CopyrightNotice(GenericArray):
    element_class = CopyrightNoticeElement


class Accountable(FlexPersonPropType):
    """
    An individual accountable for the content in legal terms.
    """


class UsageTermsElement(RightsBlockType):
    """
    A natural-language statement about the usage terms pertaining to the content.
    """


class UsageTerms(GenericArray):
    element_class = UsageTermsElement


class RightsInfoExtPropertyElement(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by the rel attribute. The semantics of the Extension Property must have the same scope as the parent property.
    """


class RightsInfoExtProperty(GenericArray):
    """
    Array of RightsInfoExtPropertyElement objects.
    """
    element_class = RightsInfoExtPropertyElement


class RightsExpressionXMLElement(BaseObject):
    # TODO
    pass

class RightsExpressionXML(GenericArray):
    element_class = RightsExpressionXMLElement

class RightsExpressionDataElement(BaseObject):
    # TODO
    pass

class RightsExpressionData(GenericArray):
    element_class = RightsExpressionDataElement


class RightsInfoElement(CommonPowerAttributes, I18NAttributes, TimeValidityAttributes):
    """
    A set of properties representing the rights associated with the Item
    """
    attributes = {
        # Reference(s) to the part(s) of an Item to which the rightsInfo element applies. When referencing part(s) of the content of an Item, idrefs must include the partid value of a partMeta element which in turn references the part of the content.
        'idrefs': 'idrefs', # type="xs:IDREFS"
        # Indicates to which part(s) of an Item the rightsInfo element applies - expressed by a QCode. If the attribute does not exist then rightsInfo applies to all parts of the Item. Mandatory NewsCodes scheme for the values: http://cv.iptc.org/newscodes/riscope/
        'scope': 'scope', # type="QCodeListType" use="optional">
        # Indicates to which part(s) of an Item the rightsInfo element applies - expressed by a URI. If the attribute does not exist then rightsInfo applies to all parts of the Item. Mandatory NewsCodes scheme for the values: http://cv.iptc.org/newscodes/riscope/</xs:documentation>
        'scopeuri': 'scopeuri', # type="IRIListType" use="optional">
        # Indicates to which rights-related aspect(s) of an Item or part(s) of an Item the rightsInfo element applies - expressed by a QCode. If the attribute does not exist then rightsInfo applies to all aspects. Mandatory NewsCodes scheme for the values: http://cv.iptc.org/newscodes/riaspect</xs:documentation>
        'aspect': 'aspect', # type="QCodeListType" use="optional">
        # Indicates to which rights-related aspect(s) of an Item or part(s) of an Item the rightsInfo element applies - expressed by a URI. If the attribute does not exist then rightsInfo applies to all aspects. Mandatory NewsCodes scheme for the values: http://cv.iptc.org/newscodes/riaspect</xs:documentation>
        'aspecturi': 'aspecturi' # type="IRIListType" use="optional">
    }

    elements = {
        'accountable': { 'type': 'single', 'xml_name': 'accountable', 'element_class': Accountable },
        'copyrightholder': { 'type': 'single', 'xml_name': 'copyrightHolder', 'element_class': CopyrightHolder },
        'copyrightnotice': { 'type': 'array', 'xml_name': 'copyrightNotice', 'element_class': CopyrightNotice },
        'usageterms': { 'type': 'array', 'xml_name': 'usageTerms', 'element_class': UsageTerms },
        'link': { 'type': 'array', 'xml_name': 'link', 'element_class': Link },
        'rightsinfo_ext': { 'type': 'array', 'xml_name': 'rightsInfoExtProperty', 'element_class': RightsInfoExtProperty },
        'rightsexpressionxml': { 'type': 'array', 'xml_name': 'rightsExpressionXML', 'element_class': RightsExpressionXML },
        'rightsexpressiondata': { 'type': 'array', 'xml_name': 'rightsExpressionData', 'element_class': RightsExpressionData }
    }


class RightsInfo(GenericArray):
    element_class = RightsInfoElement
