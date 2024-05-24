#!/usr/bin/env python

"""
Core functions for NewsMLG2 library: base objects for most
of our XML-based elements. Use magic methods to handle
property accessors to make processing easier.
"""

import re
from lxml import etree

from .catalogstore import CATALOG_STORE
from .utils import import_string

NEWSMLG2_VERSION = '2.34'
NEWSMLG2_NS = 'http://iptc.org/std/nar/2006-10-01/'
NEWSMLG2NSPREFIX = '{%s}' % NEWSMLG2_NS
NITF_NS = 'http://iptc.org/std/NITF/2006-10-18/'
NITFNSPREFIX= '{%s}' % NITF_NS
XML_NS = 'http://www.w3.org/XML/1998/namespace'
XMLNSPREFIX = '{%s}' % XML_NS
NSMAP = {None : NEWSMLG2_NS, 'xml': XML_NS, 'nitf': NITF_NS}


class BaseObject():
    """
    Implements `attributes` and `elements` handlers.
    """
    _attribute_definitions = None
    _attribute_values = {}
    _element_values = {}

    def get_attribute_definitions(self):
        """
        Load all 'attributes' from any class in the MRO inheritance chain
        """
        if self._attribute_definitions:
            return self._attribute_definitions
        self._attribute_definitions = {}
        for otherclass in reversed(self.__class__.__mro__):
            attrs = vars(otherclass).get('attributes', {})
            self._attribute_definitions.update(attrs)
        return self._attribute_definitions

    def get_element_definitions(self):
        """
        Load all element definitions declared in any class in the MRO
        inheritance chain
        """
        self._element_definitions = []
        for otherclass in reversed(self.__class__.__mro__):
            elements = vars(otherclass).get('elements', ())
            self._element_definitions += elements
        return self._element_definitions

    def get_element_class(self, element_class):
        """
        Get a class as defined here - with the special case that a class
        defined as a string is loaded using importlib.
        """
        if isinstance(element_class, str):
            # This will raise an exception if the class doesn't exist
            element_class = import_string(element_class)
        return element_class

    def __init__(self, **kwargs):
        """
        This is our base object, we don't call super() from here
        """
        self._attribute_values = {}
        self._element_values = {}
        xmlelement = kwargs.get('xmlelement')
        attr_defns = self.get_attribute_definitions()
        element_defns = self.get_element_definitions()
        if 'text' in kwargs:
            self._text = kwargs.get('text')
        if xmlelement is None:
            return
        if not isinstance(xmlelement, etree._Element):
            raise AttributeError("xmlelement should be an instance of _Element. Currently it is a "+str(type(xmlelement)))
        for attribute_id, attribute_definition in attr_defns.items():
            attribute_xmlname = attribute_definition['xml_name']
            xmlattr_value = xmlelement.get(attribute_xmlname)
            if xmlattr_value is not None:
                self._attribute_values[attribute_id] = xmlattr_value
        for (element_id, element_definition) in element_defns:
            element_class = self.get_element_class(element_definition['element_class'])
            if element_definition['type'] == 'array':
                self._element_values[element_id] = GenericArray(
                    xmlarray = xmlelement.findall(
                                    NEWSMLG2NSPREFIX+element_definition['xml_name']
                               ),
                    element_class = element_definition['element_class']
                )
            else:
                self._element_values[element_id] = element_class(
                    xmlelement = xmlelement.find(
                                    NEWSMLG2NSPREFIX+element_definition['xml_name']
                                 )
                )
        if xmlelement.text:
            self._text = re.sub(r"\s+", " ", xmlelement.text).strip()

    def get_element_value(self, item):
        """
        Return value of the element as read from the XML.
        """
        return self._element_values[item]

    def __getattr__(self, name):
        """
        Default getter for all property access operations that don't have a defined method
        """
        if name in self._element_values:
            return self.get_element_value(name)
        # convert our list of tuples to a dict so we can look up keys
        elemdefndict = dict(self._element_definitions)
        if name in elemdefndict:
            # no value, but the element definition exists - so create an empty object on the fly
            element_definition = elemdefndict[name]
            element_class = self.get_element_class(element_definition['element_class'])
            self._element_values[name] = element_class()
            return self._element_values[name]

        if name in self._attribute_definitions:
            if name in self._attribute_values:
                return self._attribute_values[name]
            if 'default' in self._attribute_definitions[name]:
                return self._attribute_definitions[name]['default']
            # <name> is a defined attribute of the class but
            # has no defined value or default: return None
            return None
        raise AttributeError(
            "'" + self.__class__.__name__ +
            "' has no element or attribute '" + name + "'"
        )

    def __setattr__(self, name, value):
        """
        Object setter: this should let us set all NewsML-G2 properties (elements
        and attributes) using Python dot syntax, e.g. "newsitem.version" or
        "newsitem.contentmeta".
        The type of "value" could be anything so we can't validate it unless we
        have defined it in the attribute definition.
        Note that __setattr__ is called for *all* property sets, not just
        when there is no other method, so we need to look for our own properties
        before handling other property names.
        """
        if name.startswith('_'):
            # it's a property internal to this module, handle it normally
            super().__setattr__(name, value)
            return
        # convert our list of tuples to a dict so we can look up keys
        elemdefndict = dict(self._element_definitions)
        if name in elemdefndict:
            element_class_name = elemdefndict[name]['element_class']
            element_class = self.get_element_class(element_class_name)
            if isinstance(value, str):
                self._element_values[name] = element_class(text = value)
            elif isinstance(value, list):
                if elemdefndict[name]['type'] == 'array':
                    self._element_values[name] = GenericArray(
                        xmlarray = value,
                        element_class = element_class
                    )
                else:
                    raise AttributeError(
                            "Trying to assign a list to a non-array element"
                          )
            else:
                self._element_values[name] = value
        elif name in self._attribute_definitions:
            self._attribute_values[name] = value
        else:
            raise AttributeError(
                "'" + self.__class__.__name__ +
                "' has no element or attribute '" + name + "'"
                  )

    def __bool__(self):
        if any(self._attribute_values.values()):
            return True
        if [bool(elem) for elem in self._element_values.values()]:
            return True
        if getattr(self, '_text', None):
            return True
        return False

    def __str__(self):
        if hasattr(self, '_text') and self._text != '':
            return self._text
        elif hasattr(self, 'qcode') and self.qcode:
            return '<'+self.__class__.__name__+' qcode="'+str(self.qcode)+'">'
        elif hasattr(self, 'uri') and self.uri:
            return '<'+self.__class__.__name__+' uri="'+str(self.uri)+'">'
        return '<'+self.__class__.__name__+'>'

    def to_xml(self):
        """
        Convert the current object to XML representation.
        Any XML generated should conform to the NewsML-G2 schema.
        """
        if hasattr(self, 'xml_element_name'):
            xml_element_name = self.xml_element_name
        else:
            xml_element_name = self.__class__.__name__
            xml_element_name = (xml_element_name[0].lower()
                + xml_element_name[1:])
        elem = etree.Element(NEWSMLG2NSPREFIX+xml_element_name, nsmap=NSMAP)
        if hasattr(self, '_text') and self._text != '':
            elem.text = self._text
        for attr_id, attr_defn in self.get_attribute_definitions().items():
            if attr_id in self._attribute_values:
                xml_attr = attr_defn['xml_name']
                elem.set(xml_attr, self._attribute_values[attr_id])
            elif not isinstance(attr_defn, str):
                if 'default' in attr_defn:
                    attr_xml_name = attr_defn['xml_name']
                    attr_default_value = attr_defn['default']
                    elem.set(attr_xml_name, attr_default_value)
                elif 'use' in attr_defn and attr_defn['use'] == 'required':
                    raise AttributeError(
                        "Attribute '" + attr_id + "' is required but has no value"
                    )
        for child_element_id, child_element_value in self._element_values.items():
            if child_element_value:
                if isinstance(child_element_value, GenericArray):
                    for arrayelem in child_element_value:
                        elem.append(arrayelem.to_xml())
                else:
                    child_elem_xml = child_element_value.to_xml()
                    elem.append(child_elem_xml)
        return elem


class GenericArray():
    """
    Handle arrays of objects.
    Subclass defines object class either as a reference in 'element_class',
    or by module and class name in strings as 'element_module_name' and
    'element_class_name'
    """
    _array_contents = []
    _element_module_name = None
    _element_class_name = None
    _element_class = None

    def __init__(self, **kwargs):
        self._array_contents = []
        self._iterindex = -1

        # Populate array based on initial args
        xmlarray = kwargs.get('xmlarray')
        if isinstance(xmlarray, (list, etree._Element)):
            if 'element_class' in kwargs:
                self._element_class = kwargs['element_class']
            else:
                raise AttributeError("'element_class' is required")
            if isinstance(xmlarray, list):
                for element in xmlarray:
                    if isinstance(element, etree._Element):
                        array_elem = self._element_class(xmlelement = element)
                        self._array_contents.append(array_elem)
                    else:
                        self._array_contents.append(element)
        else:
            raise AttributeError("'xmlarray' must be an etree _Element "
                                 "or a list of objects")

    def __iter__(self):
        return self

    def __next__(self):
        self._iterindex += 1
        if (self._iterindex >= len(self._array_contents)):
            self._iterindex = -1
            raise StopIteration
        return self._array_contents[self._iterindex]

    def __len__(self):
        return len(self._array_contents)

    def __getitem__(self, item):
        return self._array_contents[item]

    def __setitem__(self, item, value):
        self._array_contents[item] = value

    def __delitem__(self, item):
        del self._array_contents[item]

    def __str__(self):
        """
        Hack / "syntactic sugar": if an array has only one element,
        then requesting str() on the array returns the str() of the
        first element.
        """
        if len(self._array_contents) == 1:
            return str(self._array_contents[0])
        return (
            '<' + self.__class__.__name__ + ' of ' +
            str(len(self._array_contents)) + ' ' +
            self._element_class.__name__ +' objects>'
        )

    def __getattr__(self, name):
        """
        More "syntactic sugar": If a user tries to get a property or call a
        method on the array, and the array only contains one element, then pass
        the call on to the first element in the array.
        """
        if len(self._array_contents) == 1:
            return getattr(self._array_contents[0], name)
        raise AttributeError(
            "'" + self.__class__.__name__ + "'" +
            " has more than one element, shortcut property accessor failed"
        )

    def __bool__(self):
        if self._array_contents != []:
            return any(bool(item) for item in self._array_contents)
        return False

    def get_languages(self):
        """
        For repeating elements with xml:lang attributes,
        this helper function returns all available language codes.
        """
        return [elem.xml_lang for elem in self._array_contents]

    def get_for_language(self, language):
        """
        For repeating elements with xml:lang attributes,
        this helper function finds the correct language version.
        """
        for elem in self._array_contents:
            if elem.xml_lang == language:
                return elem
        # If language is not found, returns None - should we
        # raise an exception?
        return None


class QCodeURIMixin(BaseObject):
    """
    Used for any class that has "qcode" and "uri" attributes.
    Up to version 0.2, provided helper methods. Now users should
    use `uri_to_qcode()` and `qcode_to_uri()` functions instead.
    """
    attributes = {
        # A qualified code which identifies a concept - either the qcode or the
        # uri attribute MUST be used
        'qcode': {
            'xml_name': 'qcode'
        },
        # A URI which identifies a concept - either the qcode or the uri
        # attribute MUST be used
        'uri': {
            'xml_name': 'uri'
        }
    }
