#!/usr/bin/env python

import importlib
from lxml import etree

NEWSMLG2_NS = '{http://iptc.org/std/nar/2006-10-01/}'
NITF_NS = '{http://iptc.org/std/NITF/2006-10-18/}'
XML_NS = '{http://www.w3.org/XML/1998/namespace}'

VERSION = 0.1

class BaseObject(object):
    attr_values = {}
    attribute_types = {}
    dict = {}

    # Load all 'attributes' from any class in the MRO inheritance chain
    @classmethod
    def get_attributes(cls):
        all_attrs = {}
        for otherclass in reversed(cls.__mro__):
            attrs = vars(otherclass).get('attributes', {})
            all_attrs.update(attrs)
        return all_attrs

    # Load all 'attribute_types' from any class in the MRO inheritance chain
    @classmethod
    def get_attribute_types(cls):
        all_attr_types = {}
        for otherclass in reversed(cls.__mro__):
            attr_types = vars(otherclass).get('attribute_types', {})
            all_attr_types.update(attr_types)
        return all_attr_types

    def get_attr(self, attr):
        return self.attr_values.get(attr, None)

    def __init__(self, **kwargs):
        # this is our base object, we don't call super() from here
        self.dict = {}
        self.attr_values = {}
        xmlelement = kwargs.get('xmlelement')
        if type(xmlelement) == etree._Element:
            attrs = self.get_attributes()
            if attrs:
                for xml_attribute, json_attribute in attrs.items():
                    #if xml_attribute == 'xml:lang':
                    #    import pdb; pdb.set_trace()
                    self.attr_values[xml_attribute] = xmlelement.get(xml_attribute)

    def as_dict(self):
        # this is our base object, we don't call super() from here
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
        dict = self.as_dict()
        if dict != {}:
            return True
        else:
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
        super(GenericArray, self).__init__(**kwargs)
        self.array_contents = []
        xmlarray = kwargs.get('xmlarray')
        if type(xmlarray) == list or type(xmlarray) == etree._Element:
            if not self.element_class:
                self.element_class = getattr(
                    importlib.import_module(self.element_module_name),
                    self.element_class_name
                )
            for xmlelement in xmlarray:
                array_elem = self.element_class(xmlelement = xmlelement)
                self.array_contents.append(array_elem)

    def __getitem__(self, item):
        return self.array_contents[item]

    def __str__(self):
        # Hack / "syntactic sugar": if an array has only one element,
        # then requesting str() on the array returns the str() of the
        # first element.
        if len(self.array_contents) == 1:
            return str(self.array_contents[0])
        else:
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
        return json.dumps(self.as_dict(), indent=4)
