#!/usr/bin/env python

"""
Handle catalogs (lists of controlled vocabularies with their
aliases and locations)
"""

import os
from lxml import etree

from .core import NEWSMLG2, BaseObject, GenericArray
from .attributegroups import CommonPowerAttributes
from .complextypes import Name
from .concepts import Definition, Note
from .conceptrelationships import SameAs
from .labeltypes import Label1Type
from .simpletypes import IRIType
from .catalogstore import CATALOG_STORE


# TODO: raise a warning if a qcode is used that doesn't have a matching scheme declared in a catalog
# (but warnings could be turned off with a parameter)
# - option: "strict" mode where it fails instead of just raising a warning
#   - perhaps in multiple levels: differing types of "strictness"
# - method to return whether the document is "valid" in terms of resolvable qcodes, or not - so clients
# can decide what to do

# Save some commonly used catalogs in this module's cache so we don't have
# to download catalog files from the Internet
CATALOG_CACHE = {
    'http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_34.xml':
        'catalogs/catalog.IPTC-G2-Standards_34.xml',
    'http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_35.xml':
        'catalogs/catalog.IPTC-G2-Standards_35.xml',
    'http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_36.xml':
        'catalogs/catalog.IPTC-G2-Standards_36.xml'
}

def build_catalog(xmlelement):
    """
    Load all CVs referenced in local and remote catalogs.
    TODO:
    - inline catalogs are not yet tested
    - load and cache catalog from catalogRef href
    """
    catalogs = xmlelement.findall(NEWSMLG2+'catalog')
    catalog_refs = xmlelement.findall(NEWSMLG2+'catalogRef')
    for catalog in catalogs:
        add_catalog(xmlelement=catalog)
    for catalog_ref in catalog_refs:
        href = catalog_ref.get('href')

        if href in CATALOG_CACHE:
            # IPTC standard catalogs are built in, to avoid network traffic
            # (and load on IPTC servers)
            file = CATALOG_CACHE[href]
            add_catalog(uri=href, file=file)
        else:
            print("WARNING: Remote catalog {} declared. Remote "
                  "loading of catalogs is not yet supported.".format(href))


def add_catalog(**kwargs):
    """
    Load an individual catalog from a local file.
    """
    if 'file' in kwargs:
        dirname = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dirname, kwargs['file'])
        xmltree = etree.parse(filename)
        catalog_element = xmltree.getroot()
        catalog = Catalog(xmlelement=catalog_element)
        CATALOG_STORE.append(catalog)
    elif 'xmlelement' in kwargs:
        catalog = Catalog(xmlelement=kwargs['xmlelement'])
        CATALOG_STORE.append(catalog)


def get_catalogs():
    """
    Return all currently known catalogs.
    """
    return CATALOG_STORE


class Catalog(CommonPowerAttributes):
    """
    A local or remote catalog.
    """

    _catalog = []
    catalog_titles = []

    attributes = {
        # A pointer to some additional information about
        # the Catalog, and especially its evolution and latest version.
        'additionalInfo': 'additionalInfo', # type="IRIType">
        # Defines the location of the catalog as remote resource.
        # (Should be the same as the URL which is used with the href
        # attribute of a catalogRef in an item.)
        'url': 'url', # type="IRIType">
        # Defines the authority controlling this catalog
        'authority': 'authority', # type="IRIType">
        # Globally Unique Identifier for this kind of catalog as
        # managed by a provider. A version attribute should be used with it.
        'guid': 'guid', # type="xs:anyURI">
        # Version corresponding to the guid of the catalog.
        # If a version attribute exists a guid attribute must exist too
        'version': 'version', # type="xs:nonNegativeInteger">
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._catalog = []
        self._catalog_titles = []
        self._catalog_uri_lookup = {}
        self._catalog_alias_lookup = {}
        xmlelement = kwargs.get('xmlelement')
        assert isinstance(xmlelement, etree._Element)
        assert xmlelement.tag == NEWSMLG2+'catalog'
        titles = xmlelement.findall(NEWSMLG2+'title')
        for title in titles:
            title = Title(xmlelement=title)
            self.catalog_titles.append(title)

        schemes = xmlelement.findall(NEWSMLG2+'scheme')
        for scheme in schemes:
            scheme = Scheme(xmlelement=scheme)
            self.add_scheme_to_catalog(scheme)

    def add_scheme_to_catalog(self, scheme):
        """Add a given scheme to our catalog"""
        self._catalog.append(scheme)
        if hasattr(scheme, 'uri'):
            self._catalog_uri_lookup[scheme.uri] = scheme
        if hasattr(scheme, 'alias'):
            self._catalog_alias_lookup[scheme.alias] = scheme

    def get_scheme_for_alias(self, alias):
        """Return the scheme matching a given alias string"""
        if alias in self._catalog_alias_lookup.keys():
            return self._catalog_alias_lookup[alias]
        return None

    def get_scheme_for_uri(self, uri):
        """Return the scheme matching a given URI"""
        if uri in self._catalog_uri_lookup.keys():
            return self._catalog_uri_lookup[uri]
        return None

    def __iter__(self):
        for key in self._catalog:
            yield key

    def __getitem__(self,index):
        return self._catalog[index]

    def __len__(self):
        return len(self._catalog)

    #def __dict__(self):
    #    return dict(self._catalog)

    def str(self):
        """String representation of the catalog object."""
        if self.catalog_titles:
            return '<Catalog '+self.catalog_titles[0]+'>'
        return '<Catalog>'


class CatalogRefElement(BaseObject):
    """
    A reference to a remote catalog. A hyperlink to a set of scheme alias declarations.
    """
    xml_element_name = 'catalogRef'
    attributes = {
        # A short natural language name for the catalog.
        'title': 'title',
        # A hyperlink to a remote Catalog.
        'href': 'href'
    }


class CatalogRef(GenericArray):
    """
    A reference to document(s) listing externally-supplied controlled vocabularies.
    The catalog file can be in NewsML 1.
    """
    element_class = CatalogRefElement


class TitleElement(Label1Type):
    """
    A short, natural-language name
    NOTE part of "more shared elements" section - might need to move this into newsmlg2.py
    """


class Title(GenericArray):
    """
    An array of TitleElement objects.
    """
    element_class = TitleElement


class SameAsSchemeElement(IRIType, CommonPowerAttributes):
    """
    A URI which identifies another scheme with concepts that use the
    same codes and are semantically equivalent to the concepts of this scheme
    """


class SameAsScheme(GenericArray):
    """
    An array of SameAsSchemeElement objects.
    """
    element_class = SameAsSchemeElement


class Scheme(CommonPowerAttributes):
    """
    A scheme alias-to-URI mapping.
    """

    elements = {
        'sameasscheme': {
            'type': 'array', 'xml_name': 'sameAsScheme', 'element_class': SameAsScheme
        },
        'name': {
            'type': 'array', 'xml_name': 'name', 'element_class': Name
        },
        'definition': {
            'type': 'array', 'xml_name': 'definition', 'element_class': Definition
        },
        'note': {
            'type': 'array', 'xml_name': 'note', 'element_class': Note
        },
        'sameas': {
            'type': 'array', 'xml_name': 'sameAs', 'element_class': SameAs
        }
    }

    attributes = {
        # A short string used by the provider as a replacement for a scheme URI.
        'alias': 'alias', # type="xs:NCName" use="required">
        # The URI which identifies the scheme.
        'uri': 'uri', # type="IRIType" use="required">
        # Defines the authority controlling this scheme
        'authority': 'authority', # type="IRIType">
        # The date (and, optionally, the time) when the scheme was created.
        # This must not be later than the creation timestamp of any concepts in the scheme.
        'schemecreated': 'schemecreated', # type="DateOptTimeType" use="optional">
        # The date (and, optionally, the time) when the scheme was last modified.
        # The initial value is the date (and, optionally, the time) of creation of the scheme.
        'schememodified': 'schememodified', # type="DateOptTimeType" use="optional">
        # The date (and, optionally, the time) after which the scheme should not be used anymore.
        # If a scheme is marked as retired, then all Concept Identifiers in that scheme
        # (identified by the scheme @uri) must also be retired.
        'schemeretired': 'schemeretired' # type="DateOptTimeType" use="optional">
    }

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.alias, self.uri)
