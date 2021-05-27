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
from .conceptgroups import FlexPartyPropType
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

class Accountable(BaseObject):
    # TODO
    pass

class UsageTermsElement(RightsBlockType):
    """
    A natural-language statement about the usage terms pertaining to the content.
    """

class UsageTerms(GenericArray):
    element_class = UsageTermsElement

class RightsInfoExtProperty(BaseObject):
    # TODO
    pass

class RightsInfoExtPropertyArray(GenericArray):
    element_class = RightsInfoExtProperty

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
        'copyright_holder': { 'type': 'single', 'xml_name': 'copyrightHolder', 'element_class': CopyrightHolder },
        'copyright_notice': { 'type': 'array', 'xml_name': 'copyrightNotice', 'element_class': CopyrightNotice },
        'usage_terms': { 'type': 'array', 'xml_name': 'usageTerms', 'element_class': UsageTerms },
        'link': { 'type': 'array', 'xml_name': 'link', 'element_class': Link },
        'rights_info_ext': { 'type': 'array', 'xml_name': 'rightsInfoExtProperty', 'element_class': RightsInfoExtProperty },
        'rights_expression_xml': { 'type': 'array', 'xml_name': 'rightsExpressionXML', 'element_class': RightsExpressionXML },
        'rights_expression_data': { 'type': 'array', 'xml_name': 'rightsExpressionData', 'element_class': RightsExpressionData }
    }

    def get_copyrightholder(self):
        return self.get_element_value('copyright_holder')

    def get_copyrightnotice(self):
        return self.get_element_value('copyright_notice')

    def get_usageterms(self):
        return self.get_element_value('usage_terms')


class RightsInfo(GenericArray):
    element_class = RightsInfoElement
