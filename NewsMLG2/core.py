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
    _attribute_definitions = None
    _element_definitions = None
    _attribute_values = {}
    _attribute_types = {}
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
        return self._attribute_values.get(attr, None)

    def get_element_definitions(self):
        """
        Load all element definitions declared in any class in the MRO
        inheritance chain
        """
        if self._element_definitions:
            return self._element_definitions
        self._element_definitions = {}
        for otherclass in reversed(self.__class__.__mro__):
            elements = vars(otherclass).get('elements', {})
            self._element_definitions.update(elements)
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
            raise AttributeError("xmlelement should be an instance of _Element")
        for attribute_id, attribute_definition in attr_defns.items():
            if not isinstance(attribute_definition, str):
                # new style definition
                attribute_xmlname = attribute_definition['xml_name']
                self._attribute_values[attribute_id] = xmlelement.get(attribute_xmlname)
            else:
                # old style definition - definition is ignored
                # TODO remove this line when all attribute definitions are updated
                self._attribute_values[attribute_id] = xmlelement.get(attribute_id)
        for element_id, element_definition in element_defns.items():
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
        Default getter for all methods where we don't have a defined method
        """
        if name in self._element_values:
            return self._element_values[name]
        elif name in self._element_definitions:
            # no value, but the element exists - create it on the fly!
            element_definition = self._element_definitions[name]
            element_class = self.get_element_class(element_definition['element_class'])
            self._element_values[name] = element_class()
            return self._element_values[name]
        elif name in self._attribute_definitions:
            if name in self._attribute_values:
                return self._attribute_values[name]
            elif 'default' in self._attribute_definitions[name]:
                return self._attribute_definitions[name]['default']
            else:
                raise AttributeError(
                    "'" + name + "' is a defined attribute of " +
                    "'" + self.__class__.__name__ + "' " +
                    "but has no defined value or default"
                )
        raise AttributeError(
            "'" + self.__class__.__name__ +
            "' has no element or attribute '" + name + "'"
        )

    def __setattr__(self, name, value):
        """
        Object setter: this should let us set all NewsMLg2 properties (elements
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
        elif name in self._element_definitions:
            if isinstance(value, str):
                element_class = self.get_element_class(self._element_definitions[name]['element_class'])
                self._element_values[name] = element_class(text = value)
            else:
                self._element_values[name] = value
        elif name in self._attribute_definitions:
            self._attribute_values[name] = value
        else:
            raise AttributeError(
                "'" + self.__class__.__name__ +
                "' has no element or attribute '" + name + "'"
                  )


    """
    def as_dict(self):
        Return the full object in dictionary form
        (Could we just use __dict__ ?)
        attrs = self.get_attribute_definitions()
        attr_types = self.get_attribute_types()
        if attrs:
            for xml_attribute, json_property in attrs.items():
                if xml_attribute in self._attribute_values and self._attribute_values[xml_attribute]:
                    property_value =  self._attribute_values[xml_attribute]
                    property_type = attr_types.get(xml_attribute, None)
                    if property_type == "integer":
                        property_value = int(property_value)
                    self.dict.update({ json_property: property_value })
        return self.dict
    """

    def __bool__(self):
        if any(self._attribute_values.values()):
            return True
        if [bool(elem) for elem in self._element_values.values()]:
            return True
        if getattr(self, '_text', None):
            return True
        return False

    def __str__(self):
        if hasattr(self, '_text') and self._text is not None:
            return self._text
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
                if isinstance(attr_defn, str):
                    # old style - TODO remove after all attr defns are updated
                    xml_attr = attr_defn
                else:
                    xml_attr = attr_defn['xml_name']
                elem.set(xml_attr, self._attribute_values[attr_id])
            # only check for new-style attribute definitions
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
                child_elem_xml = child_element_value.to_xml()
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
    _array_contents = []
    _element_module_name = None
    _element_class_name = None
    _element_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._array_contents = []
        xmlarray = kwargs.get('xmlarray')
        if isinstance(xmlarray, (list, etree._Element)):
            if 'element_class' in kwargs:
                self._element_class = kwargs['element_class']
            else:
                raise AttributeError("'element_class' is required")
            for xmlelement in xmlarray:
                array_elem = self._element_class(xmlelement = xmlelement)
                self._array_contents.append(array_elem)

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
            '<' + self.__class__.__name__ + 'of ' +
            len(self._array_contents) + ' ' +
            self._element_class_name +' objects>'
        )

    def as_dict(self):
        return [ elem.as_dict() for elem in self._array_contents ]

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

    def to_xml(self):
        xml_array = []
        for elem in self._array_contents:
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
