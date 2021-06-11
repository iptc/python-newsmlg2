#!/usr/bin/env python

"""
Core functions for NewsMLG2 library.
"""

import importlib
import json
import re
from lxml import etree

from .catalogstore import CATALOG_STORE
from .utils import import_string

NEWSMLG2_NS = 'http://iptc.org/std/nar/2006-10-01/'
NEWSMLG2 = '{%s}' % NEWSMLG2_NS
NITF_NS = 'http://iptc.org/std/NITF/2006-10-18/'
NITF = '{%s}' % NITF_NS
XML_NS = 'http://www.w3.org/XML/1998/namespace'
XML = '{%s}' % XML_NS
NSMAP = {None : NEWSMLG2_NS, 'xml': XML_NS, 'nitf': NITF_NS}


class BaseObject():
    """
    Implements `attributes` and `elements` handlers.
    """
    attr_values = {}
    attribute_types = {}
    element_values = {}
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
    def get_elements(cls):
        """
        Load all element definitions declared in any class in the MRO
        inheritance chain
        """
        all_elements = {}
        for otherclass in reversed(cls.__mro__):
            elements = vars(otherclass).get('elements', {})
            all_elements.update(elements)
        return all_elements

    def __init__(self, **kwargs):
        """
        This is our base object, we don't call super() from here
        """
        self.dict = {}
        self.attr_values = {}
        self.element_values = {}
        xmlelement = kwargs.get('xmlelement')
        if xmlelement is None:
            return
        if not isinstance(xmlelement, etree._Element):
            raise Exception("xmlelement should be an instance of _Element")
        attrs = self.get_attributes()
        for xml_attribute, attribute_id in attrs.items():
            self.attr_values[attribute_id] = xmlelement.get(xml_attribute)

        elements = self.get_elements()
        for element_id, element_definition in elements.items():
            element_class = element_definition['element_class']
            if isinstance(element_class, str):
                # This will raise an exception if the class doesn't exist
                element_class = import_string(element_class)
            if element_definition['type'] == 'array':
                assert hasattr(element_class, 'element_class'), (
                    str(element_class) +
                    " has no property 'element_class'. Defined in " +
                    str(self.__class__)
                )
                self.element_values[element_id] = element_class(
                    xmlarray = xmlelement.findall(
                                    NEWSMLG2+element_definition['xml_name']
                               )
                )
            else:
                self.element_values[element_id] = element_class(
                    xmlelement = xmlelement.find(
                                    NEWSMLG2+element_definition['xml_name']
                                 )
                )
        if xmlelement.text:
            self.text = re.sub(r"\s+", " ", xmlelement.text).strip()

    def get_element_value(self, item):
        """
        Return value of the element as read from the XML.
        """
        return self.element_values[item]

    def __getattr__(self, name):
        """
        Default getter for all methods where we don't have a defined method
        """
        if name in self.element_values:
            return self.element_values[name]
        if name in self.attr_values:
            return self.attr_values[name]
        raise AttributeError(
            "'" + self.__class__.__name__ +
            "' has no element or attribute '" + name + "'"
              )

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
        if self.text:
            return self.text
        return '<'+self.__class__.__name__+'>'

    def to_xml(self):
        root = etree.Element("p")
        root.text = "to_xml() placeholder"
        return root


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
                assert getattr(self, 'element_class_name'), (
                    str(self.__class__)+" has no element 'element_class_name'"
                )
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
        """
        Hack / "syntactic sugar": if an array has only one element,
        then requesting str() on the array returns the str() of the
        first element.
        """
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

    def __getattr__(self, name):
        """
        More "syntactic sugar": If a user tries to get a property or call a
        method on the array, and the array only contains one element, then pass
        the call on to the first element in the array.
        """
        if len(self.array_contents) == 1:
            return getattr(self.array_contents[0], name)
        raise AttributeError(
            "'" + self.__class__.__name__ + "'" +
            " has more than one element, shortcut property accessor failed"
        )


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
        # get catalog - we need to put the slash back!
        scheme = CATALOG_STORE.get_scheme_for_uri(urimainpart+'/')
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
