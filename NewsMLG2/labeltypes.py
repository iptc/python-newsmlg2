#!/usr/bin/env python

"""
NAR Label Types
"""

from .core import BaseObject
from .attributegroups import (
    CommonPowerAttributes, FlexAttributes, I18NAttributes, QuantifyAttributes
)


class BR(CommonPowerAttributes):
    """
    A line break
    """

class RB(BaseObject):
    """Ruby base"""

class RP(BaseObject):
    """Ruby parenthesis"""

class RT(BaseObject):
    """Ruby text"""

class Ruby(CommonPowerAttributes, I18NAttributes):
    """
    Simple W3C Ruby Annotation - see http://www.w3.org/TR/ruby/#simple-ruby1
    """
    elements = [
        ('rb', { 'type': 'single', 'xml_name': 'rb', 'element_class': RB }),
        ('rt', { 'type': 'single', 'xml_name': 'rt', 'element_class': RT }),
        ('rp', { 'type': 'single', 'xml_name': 'rp', 'element_class': RP })
    ]


class Span(CommonPowerAttributes, I18NAttributes):
    """
    A generic mechanism for adding inline information to parts of the textual
    content
    """
    elements = [
        ('ruby', { 'type': 'array', 'xml_name': 'ruby', 'element_class': Ruby })
    ]
    attributes = {
        # An equivalent of the html class attribute
        'class': {
            'xml_name': 'class',
            'xml_type': 'xs:string',
            'use': 'optional'
        }
    }


class Inline(CommonPowerAttributes, FlexAttributes, I18NAttributes,
    QuantifyAttributes):
    """
    An inline markup tag to be used with any concept
    Note that this is a mixed element i.e. text can be mixed with child
    elements. TODO handle this type of content properly.
    """
    elements = [
        ('span', { 'type': 'array', 'xml_name': 'span', 'element_class': Span }),
        ('ruby', { 'type': 'array', 'xml_name': 'ruby', 'element_class': Ruby })
    ]
    attributes = {
        # An equivalent of the html class attribute
        'class': {
            'xml_name': 'class',
            'xml_type': 'xs:string',
            'use': 'optional'
        }
    }


class A(CommonPowerAttributes, I18NAttributes):
    """
    An anchor for inline linking like in HTML
    Note that this is a mixed element i.e. text can be mixed with child
    elements. TODO handle this type of content properly.
    """
    elements = [
        ('inline', { 'type': 'array', 'xml_name': 'inline', 'element_class': Inline }),
        ('span', { 'type': 'array', 'xml_name': 'span', 'element_class': Span }),
        ('ruby', { 'type': 'array', 'xml_name': 'ruby', 'element_class': Ruby })
    ]
    attributes = {
        # An equivalent of the html class attribute
        'class': {
            'xml_name': 'class',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # An equivalent of the html href attribute
        'href': {
            'xml_name': 'href',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # An equivalent of the html hreflang attribute
        'hreflang': {
            'xml_name': 'hreflang',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # An equivalent of the html rel attribute
        'rel': {
            'xml_name': 'rel',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # An equivalent of the html rev attribute
        'rev': {
            'xml_name': 'rev',
            'xml_type': 'xs:string',
            'use': 'optional'
        }
    }


class Label1Type(CommonPowerAttributes, I18NAttributes):
    """
    The PCL-type for information about the content as natural language string
    with minimal markup
    """
    elements = [
        ('a', { 'type': 'array', 'xml_name': 'a', 'element_class': A }),
        ('span', { 'type': 'array', 'xml_name': 'span', 'element_class': Span }),
        ('ruby', { 'type': 'array', 'xml_name': 'ruby', 'element_class': Ruby }),
        ('inline', { 'type': 'array', 'xml_name': 'inline', 'element_class': Inline })
    ]
    attributes = {
        # A refinement of the semantics of the label - expressed by a QCode
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeListType',
            'use': 'optional'
        },
        # A refinement of the semantics of the label - expressed by a URI
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIListType',
            'use': 'optional'
        },
        # An indication of the target media type(s), values as defined by the
        # Cascading Style Sheets specification [CSS].
        'media': {
            'xml_name': 'media',
            'xml_type': 'xs:NMTOKENS',
            'use': 'optional'
        }
    }


class BlockType(CommonPowerAttributes, I18NAttributes):
    """
    The type for nformation about the content as natural language
    string with minimal markup and line breaks
    """
    elements = [
        ('a', { 'type': 'array', 'xml_name': 'a', 'element_class': A }),
        ('span', { 'type': 'array', 'xml_name': 'span', 'element_class': Span }),
        ('ruby', { 'type': 'array', 'xml_name': 'ruby', 'element_class': Ruby }),
        ('br', { 'type': 'array', 'xml_name': 'br', 'element_class': BR }),
        ('inline', { 'type': 'array', 'xml_name': 'inline', 'element_class': Inline })
    ]
    attributes = {
        # An indication of the target media type(s) values as
        # defined by the Cascading Style Sheets (CSS) specification.
        'media': {
            'xml_name': 'media',
        },
        # A refinement of the semantics of the block.
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeListType'
        },
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIType'
        }
    }
