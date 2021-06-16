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
    attribute_definitions = None
    element_definitions = None
    attribute_values = {}
    attribute_types = {}
    element_values = {}
    dict = {}

    def get_attributes(self):
        """
        Load all 'attributes' from any class in the MRO inheritance chain
        """
        if self.attribute_definitions:
            return self.attribute_definitions
        self.attribute_definitions = {}
        for otherclass in reversed(self.__class__.__mro__):
            attrs = vars(otherclass).get('attributes', {})
            self.attribute_definitions.update(attrs)
        return self.attribute_definitions

    def get_attribute_types(self):
        """
        Load all 'attribute_types' declared in  any class in the MRO
        inheritance chain
        """
        all_attr_types = {}
        for otherclass in reversed(self.__class__.__mro__):
            attr_types = vars(otherclass).get('attribute_types', {})
            all_attr_types.update(attr_types)
        return all_attr_types

    def get_attr(self, attr):
        """
        Get value of the given XML attribute.
        """
        return self.attribute_values.get(attr, None)

    def get_elements(self):
        """
        Load all element definitions declared in any class in the MRO
        inheritance chain
        """
        if self.element_definitions:
            return self.element_definitions
        self.element_definitions = {}
        for otherclass in reversed(self.__class__.__mro__):
            elements = vars(otherclass).get('elements', {})
            self.element_definitions.update(elements)
        return self.element_definitions

    def __init__(self, **kwargs):
        """
        This is our base object, we don't call super() from here
        """
        self.dict = {}
        self.attribute_values = {}
        self.element_values = {}
        xmlelement = kwargs.get('xmlelement')
        if xmlelement is None:
            return
        if not isinstance(xmlelement, etree._Element):
            raise Exception("xmlelement should be an instance of _Element")
        attrs = self.get_attributes()
        for xml_attribute, attribute_id in attrs.items():
            self.attribute_values[xml_attribute] = xmlelement.get(xml_attribute)

        elements = self.get_elements()
        for element_id, element_definition in elements.items():
            element_class = element_definition['element_class']
            if isinstance(element_class, str):
                # This will raise an exception if the class doesn't exist
                element_class = import_string(element_class)
            if element_definition['type'] == 'array':
                self.element_values[element_id] = GenericArray(
                    xmlarray = xmlelement.findall(
                                    NEWSMLG2NSPREFIX+element_definition['xml_name']
                               ),
                    element_class = element_definition['element_class']
                )
            else:
                self.element_values[element_id] = element_class(
                    xmlelement = xmlelement.find(
                                    NEWSMLG2NSPREFIX+element_definition['xml_name']
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
        if name in self.attribute_values:
            return self.attribute_values[name]
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
                if xml_attribute in self.attribute_values and self.attribute_values[xml_attribute]:
                    property_value =  self.attribute_values[xml_attribute]
                    property_type = attr_types.get(xml_attribute, None)
                    if property_type == "integer":
                        property_value = int(property_value)
                    self.dict.update({ json_property: property_value })
        return self.dict

    def __bool__(self):
        if any(self.attribute_values.values()):
            return True
        if [bool(elem) for elem in self.element_values.values()]:
            return True
        if getattr(self, 'text', None):
            return True
        return False

    def __str__(self):
        if self.text:
            return self.text
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
        if hasattr(self, 'text') and self.text != '':
            elem.text = self.text
        for attr_name, attr_value in self.attribute_values.items():
            if attr_value is not None:
                elem.set(attr_name, attr_value)
        for child_element_id, child_element in self.element_values.items():
            if child_element:
                child_elem_xml = child_element.to_xml()
                if isinstance(child_elem_xml, list):
                    for child in child_elem_xml:
                        elem.append(child)
                else:
                    elem.append(child_elem_xml)
        return elem


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
            if 'element_class' in kwargs:
                self.element_class = kwargs['element_class']
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

    def __bool__(self):
        if self.array_contents != []:
            return any(bool(item) for item in self.array_contents)
        return False

    def to_xml(self):
        xml_array = []
        for elem in self.array_contents:
            xml_array.append(elem.to_xml())
        return xml_array


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
