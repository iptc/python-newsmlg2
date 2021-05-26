#!/usr/bin/env python

"""
Core functions for NewsMLG2 library.
"""

import importlib
import json
from lxml import etree

from .catalogstore import CATALOG_STORE

NEWSMLG2_NS = 'http://iptc.org/std/nar/2006-10-01/'
NEWSMLG2 = '{%s}' % NEWSMLG2_NS
NITF_NS = 'http://iptc.org/std/NITF/2006-10-18/'
NITF = '{%s}' % NITF_NS
XML_NS = 'http://www.w3.org/XML/1998/namespace'
XML = '{%s}' % XML_NS
NSMAP = {None : NEWSMLG2_NS, 'xml': XML_NS, 'nitf': NITF_NS}

class BaseObject():
    """
    Implements `attributes`, `single_elements` and `array_elements`.
    """
    attr_values = {}
    attribute_types = {}
    single_elements = {}
    array_elements = {}
    dict = {}

    @classmethod
    def get_attributes(cls):
        """
        Load all 'attributes' from any class in the MRO inheritance chain
        """
        all_attrs = {}
        for otherclass in reversed(cls.__mro__):
            attrs = vars(otherclass).get('attributes', {})
            all_attrs.update(attrs)
        return all_attrs

    @classmethod
    def get_attribute_types(cls):
        """
        Load all 'attribute_types' declared in  any class in the MRO
        inheritance chain
        """
        all_attr_types = {}
        for otherclass in reversed(cls.__mro__):
            attr_types = vars(otherclass).get('attribute_types', {})
            all_attr_types.update(attr_types)
        return all_attr_types

    def get_attr(self, attr):
        """
        Get value of the given XML attribute.
        """
        return self.attr_values.get(attr, None)

    @classmethod
    def get_single_elements(cls):
        """
        Load all single-valued elements declared in any class in the MRO
        inheritance chain
        """
        all_single_elements = {}
        for otherclass in reversed(cls.__mro__):
            single_elements = vars(otherclass).get('single_elements', {})
            all_single_elements.update(single_elements)
        return all_single_elements

    @classmethod
    def get_array_elements(cls):
        """
        Load all arrays (multi-valued elements) declared in any class in
        the MRO inheritance chain
        """
        all_array_elements = {}
        for otherclass in reversed(cls.__mro__):
            array_elements = vars(otherclass).get('array_elements', {})
            all_array_elements.update(array_elements)
        return all_array_elements

    def __init__(self, **kwargs):
        """
        This is our base object, we don't call super() from here
        """
        self.dict = {}
        self.attr_values = {}
        self.single_element_values = {}
        self.array_element_values = {}
        xmlelement = kwargs.get('xmlelement')
        if isinstance(xmlelement, etree._Element):
            attrs = self.get_attributes()
            if attrs:
                for xml_attribute, json_attribute in attrs.items():
                    self.attr_values[xml_attribute] = xmlelement.get(xml_attribute)
            single_elements = self.get_single_elements()
            if single_elements:
                for element_name, element_class in single_elements.items():
                    self.single_element_values[element_name] = element_class(
                        xmlelement = xmlelement.find(NEWSMLG2+element_name)
                    )
            array_elements = self.get_array_elements()
            if array_elements:
                for element_name, element_class in array_elements.items():
                    self.array_element_values[element_name] = element_class(
                        xmlarray = xmlelement.findall(NEWSMLG2+element_name)
                    )

    def get_single_element_value(self, item):
        return self.single_element_values[item]

    def get_array_element_value(self, item):
        return self.array_element_values[item]

    def as_dict(self):
        """
        Return the full object in dictionary form
        (Could we just use __dict__ ?)
        """
        attrs = self.get_attributes()
        attr_types = self.get_attribute_types()
        if attrs:
            for xml_attribute, json_property in attrs.items():
                if xml_attribute in self.attr_values and self.attr_values[xml_attribute]:
                    property_value =  self.attr_values[xml_attribute]
                    property_type = attr_types.get(xml_attribute, None)
                    if property_type == "integer":
                        property_value = int(property_value)
                    self.dict.update({ json_property: property_value })
        return self.dict

    def __bool__(self):
        asdict = self.as_dict()
        if asdict != {}:
            return True
        return False

    def __str__(self):
        return '<'+self.__class__.__name__+'>'


class GenericArray(BaseObject):
    """
    Helper class to handle arrays of objects.
    To be subclassed by every array class.
    Subclass defines object class either as a reference in 'element_class',
    or by module and class name in strings as 'element_module_name' and
    'element_class_name'
    """
    array_contents = []
    element_module_name = None
    element_class_name = None
    element_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.array_contents = []
        xmlarray = kwargs.get('xmlarray')
        if isinstance(xmlarray, (list, etree._Element)):
            if not self.element_class:
                self.element_class = getattr(
                    importlib.import_module(self.element_module_name),
                    self.element_class_name
                )
            for xmlelement in xmlarray:
                array_elem = self.element_class(xmlelement = xmlelement)
                self.array_contents.append(array_elem)

    def __len__(self):
        return len(self.array_contents)

    def __getitem__(self, item):
        return self.array_contents[item]

    def __setitem__(self, item, value):
        self.array_contents[item] = value

    def __delitem__(self, item):
        del self.array_contents[item]

    def __str__(self):
        # Hack / "syntactic sugar": if an array has only one element,
        # then requesting str() on the array returns the str() of the
        # first element.
        if len(self.array_contents) == 1:
            return str(self.array_contents[0])
        return (
            '<' + self.__class__.__name__ + 'of ' +
            len(self.array_contents) + ' ' +
            self.element_class_name +' objects>'
        )

    def __bool__(self):
        return len(self.array_contents) != 0

    def as_dict(self):
        return [ elem.as_dict() for elem in self.array_contents ]

    def to_json(self):
        """
        Return this class as a JSON object.
        """
        return json.dumps(self.as_dict(), indent=4)


class QCodeURIMixin(BaseObject):
    """
    Used for any class that has "qcode" and "uri" attributes.
    Provides getter and setter methods.
    """
    attributes = {
        # A qualified code which identifies a concept - either the qcode or the
        # uri attribute MUST be used
        'qcode': 'qcode',
        # A URI which identifies a concept - either the qcode or the uri
        # attribute MUST be used
        'uri': 'uri'
    }

    def get_qcode(self):
        """
        Return the value of this property as a qcode
        """
        qcode = self.get_attr('qcode')
        if qcode is not None:
            return qcode
        # convert URI to qcode:
        uri = self.get_attr('uri')
        urimainpart, code = uri.rsplit('/', 1)
        # get catalog
        scheme = CATALOG_STORE.get_scheme_for_uri(urimainpart)
        # look up catalog for URI, get prefix
        alias = scheme.alias
        return alias + ':' + code 

    def get_uri(self):
        """
        Return the value of this property as a URI
        """
        uri = self.get_attr('uri')
        if uri:
            return uri
        # convert qcode to URI:
        qcode = self.get_attr('qcode')
        alias, code = qcode.split(':')
        # get catalog
        scheme = CATALOG_STORE.get_scheme_for_alias(alias)
        # look up catalog for alias, get URI
        uri = scheme.uri
        return uri + code
