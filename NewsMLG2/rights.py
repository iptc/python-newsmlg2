#!/usr/bin/env python

"""
Elements for handling rights management
"""

from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, TimeValidityAttributes
)
from .concepts import FlexPartyPropType, FlexPersonPropType
from .conceptrelationships import FlexPropType
from .extensionproperties import Flex2ExtPropType
from .labeltypes import BlockType
from .link import Link


class RightsBlockType(BlockType):
    """
    An expression of rights in natural language or as a reference to remote information
    """
    attributes = {
        # The locator of a remote expression of rights
        'href': {
            'xml_name': 'href',
            'xml_type': 'IRIType'
        }
    }


class CopyrightHolder(FlexPartyPropType):
    """
    The person or organisation claiming the intellectual property for the content.
    """


class CopyrightNotice(RightsBlockType):
    """
    Any necessary copyright notice for claiming the intellectual property for the content.
    """


class Accountable(FlexPersonPropType):
    """
    An individual accountable for the content in legal terms.
    """


class UsageTerms(RightsBlockType):
    """
    A natural-language statement about the usage terms pertaining to the content.
    """


class RightsInfoExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """


class RightsExpressionXML(CommonPowerAttributes):
    """
    Contains a rights expression as defined by a Rights Expression Language and
    seralized using XML encoding.
    """
    attributes = {
        # Identifier for the used Rights Expression language
        'langid': {
            'xml_name': 'langid',
            'xml_type': 'xs:anyURI',
            'use': 'required'
        }
    }


class RightsExpressionData(CommonPowerAttributes):
    """
    Contains a rights expression as defined by a Rights Expression Language and
    seralized using any specific encoding except XML.
    """
    attributes = {
        # Identifier for the used Rights Expression language
        'langid': {
            'xml_name': 'langid',
            'xml_type': 'xs:anyURI',
            'use': 'required'
        },
        # Identifier of the used type of encoding, prefered are IANA Media Type identifiers.
        'enctype': {
            'xml_name': 'enctype',
            'xml_type': 'xs:string',
            'use': 'required'
        }
    }


class DataMining(FlexPropType):
    """
    Data mining prohibition or permission, optionally with constraints
    """


class RightsInfo(CommonPowerAttributes, I18NAttributes, TimeValidityAttributes):
    """
    A set of properties representing the rights associated with the Item
    """
    attributes = {
        # Reference(s) to the part(s) of an Item to which the rightsInfo element
        # applies. When referencing part(s) of the content of an Item, idrefs
        # must include the partid value of a partMeta element which in turn
        # references the part of the content.
        'idrefs': {
            'xml_name': 'idrefs',
            'xml_type': 'xs:IDREFS'
        },
        # Indicates to which part(s) of an Item the rightsInfo element applies -
        # expressed by a QCode. If the attribute does not exist then rightsInfo
        # applies to all parts of the Item.
        # Mandatory NewsCodes scheme for the values:
        # http://cv.iptc.org/newscodes/riscope/
        'scope': {
            'xml_name': 'scope',
            'xml_type': 'QCodeListType',
            'use': 'optional'
        },
        # Indicates to which part(s) of an Item the rightsInfo element applies -
        # expressed by a URI. If the attribute does not exist then rightsInfo
        # applies to all parts of the Item.
        # Mandatory NewsCodes scheme for the values:
        # http://cv.iptc.org/newscodes/riscope/
        'scopeuri': {
            'xml_name': 'scopeuri',
            'xml_type': 'IRIListType',
            'use': 'optional'
        },
        # Indicates to which rights-related aspect(s) of an Item or part(s) of
        # an Item the rightsInfo element applies - expressed by a QCode. If the
        # attribute does not exist then rightsInfo applies to all aspects.
        # Mandatory NewsCodes scheme for the values:
        # http://cv.iptc.org/newscodes/riaspect
        'aspect': {
            'xml_name': 'aspect',
            'xml_type': 'QCodeListType',
            'use': 'optional'
        },
        # Indicates to which rights-related aspect(s) of an Item or part(s) of
        # an Item the rightsInfo element applies - expressed by a URI. If the
        # attribute does not exist then rightsInfo applies to all aspects.
        # Mandatory NewsCodes scheme for the values:
        # http://cv.iptc.org/newscodes/riaspect
        'aspecturi': {
            'xml_name': 'aspecturi',
            'xml_type': 'IRIListType',
            'use': 'optional'
        }
    }

    elements = [
        ('accountable', {
            'type': 'single', 'xml_name': 'accountable',
            'element_class': Accountable
        }),
        ('copyrightholder', {
            'type': 'single', 'xml_name': 'copyrightHolder',
            'element_class': CopyrightHolder
        }),
        ('copyrightnotice', {
            'type': 'array', 'xml_name': 'copyrightNotice',
            'element_class': CopyrightNotice
        }),
        ('usageterms', {
            'type': 'array', 'xml_name': 'usageTerms',
            'element_class': UsageTerms
        }),
        ('link', {
            'type': 'array', 'xml_name': 'link', 'element_class': Link
        }),
        ('rightsinfo_ext', {
            'type': 'array', 'xml_name': 'rightsInfoExtProperty',
            'element_class': RightsInfoExtProperty
        }),
        ('rightsexpressionxml', {
            'type': 'array', 'xml_name': 'rightsExpressionXML',
            'element_class': RightsExpressionXML
        }),
        ('rightsexpressiondata', {
            'type': 'array', 'xml_name': 'rightsExpressionData',
            'element_class': RightsExpressionData
        }),
        ('datamining', {
            'type': 'single', 'xml_name': 'dataMining',
            'element_class': DataMining
        })
    ]
