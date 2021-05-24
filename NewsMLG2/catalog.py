#!/usr/bin/env python

# Catalog information

import json
import os

from lxml import etree

DEBUG = True

from .core import NEWSMLG2, BaseObject, GenericArray
from .attributegroups import CommonPowerAttributes
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

class CatalogMixin(object):
    def buildCatalog(self, xmlelement, **kwargs):
        catalogs = xmlelement.findall(NEWSMLG2+'catalog')
        catalogRefs = xmlelement.findall(NEWSMLG2+'catalogRef')
        for catalog in catalogs:
            # TODO inline catalogs are not yet tested
            self.addCatalog(xmlelement=catalog)
        for catalogRef in catalogRefs:
            href = catalogRef.get('href')

            if href in CATALOG_CACHE:
                # IPTC standard catalogs are built in, to avoid network traffic
                # (and load on IPTC servers)
                file = CATALOG_CACHE[href]
                if DEBUG:
                    print("Loading built-in catalog {}".format(file))
                self.addCatalog(uri=href, file=file)
            else:
                ## TODO: load and cache catalog from href
                if DEBUG:
                    print("WARNING: Remote catalog {} declared. Remote "
                          "loading of catalogs is not yet supported.".format(href))

    def addCatalog(self, **kwargs):
        if 'file' in kwargs:
            dirname = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(dirname, kwargs['file'])
            if DEBUG:
                print("Loading catalog from file {}".format(filename))
            xmltree = etree.parse(filename)
            catalog_element = xmltree.getroot()
            catalog = Catalog(xmlelement=catalog_element)
            CATALOG_STORE.append(catalog)
        elif 'xmlelement' in kwargs:
            catalog = Catalog(xmlelement=xmlelement)
            CATALOG_STORE.append(catalog)

    def getCatalogs(self):
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
        super(Catalog, self).__init__(**kwargs)
        self._catalog = []
        self._catalog_titles = []
        self._catalog_uri_lookup = {}
        self._catalog_alias_lookup = {}
        xmlelement = kwargs.get('xmlelement')
        assert type(xmlelement) == etree._Element
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
        self._catalog.append(scheme)
        if hasattr(scheme, 'uri'):
            self._catalog_uri_lookup[scheme.uri] = scheme
        if hasattr(scheme, 'alias'):
            self._catalog_alias_lookup[scheme.alias] = scheme
        if DEBUG:
            print("Loaded scheme {} from catalog".format(scheme))

    def getSchemeForAlias(self, alias):
        if alias in self._catalog_alias_lookup.keys():
            return self._catalog_alias_lookup[alias]

    def __iter__(self):
        for key in self._catalog.keys():
            yield key

    def __getitem__(self,index):
        return self._catalog[index]

    def __len__(self):
        return len(self._catalog)

    #def __dict__(self):
    #    return dict(self._catalog)

    def str(self):
        if self.catalog_titles:
            return '<Catalog '+self.catalog_titles[0]+'>'
        else:
            return '<Catalog>'


class CatalogRef(CommonPowerAttributes):
    """
    A reference to a remote catalog. A hyperlink to a set of scheme alias declarations.
    """
    attributes = {
        # A hyperlink to a remote Catalog.
        'href': 'href', # type="IRIType" use="required">
    }
    """
            <xs:element ref="title" minOccurs="0" maxOccurs="unbounded">
               <xs:annotation>
                  <xs:documentation>A short natural language name for the catalog.</xs:documentation>
               </xs:annotation>
            </xs:element>
    """

class Scheme(CommonPowerAttributes):
    """
    A scheme alias-to-URI mapping.

                <xs:choice minOccurs="0" maxOccurs="unbounded">
                     <xs:element ref="sameAsScheme"/>
                     <xs:element ref="name">
                        <xs:annotation>
                           <xs:documentation>A natural language name for the scheme.</xs:documentation>
                        </xs:annotation>
                     </xs:element>
                     <xs:element ref="definition">
                        <xs:annotation>
                           <xs:documentation>A natural language definition of the semantics of the scheme. This definition is normative only for the scope of the use of this scheme.</xs:documentation>
                        </xs:annotation>
                     </xs:element>
                     <xs:element ref="note">
                        <xs:annotation>
                           <xs:documentation>Additional natural language information about the scheme.</xs:documentation>
                        </xs:annotation>
                     </xs:element>
                     <xs:element name="sameAs">
                        <xs:annotation>
                           <xs:documentation>Use is DEPRECATED - use sameAsScheme instead. (A URI which identifies another scheme with concepts that use the same codes and are semantically equivalent to the concepts of this scheme)</xs:documentation>
                        </xs:annotation>
                        <xs:complexType>
                           <xs:simpleContent>
                              <xs:extension base="IRIType">
                                 <xs:attributeGroup ref="commonPowerAttributes"/>
                                 <xs:attribute name="g2flag" type="xs:string" use="optional" fixed="DEPR-SCH">
                                    <xs:annotation>
                                       <xs:documentation>DO NOT USE this attribute, for G2 internal maintenance purposes only.</xs:documentation>
                                    </xs:annotation>
                                 </xs:attribute>
                              </xs:extension>
                           </xs:simpleContent>
                        </xs:complexType>
                     </xs:element>

    """
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
    def __init__(self, xmlelement=None, **kwargs):
        if xmlelement is not None:
            self.alias = xmlelement.get('alias', '')
            self.uri = xmlelement.get('uri', '')
            self.authority = xmlelement.get('authority', '')
            self.modified = xmlelement.get('modified', '')
            self.name = xmlelement.findtext(NEWSMLG2+'name', default='') # TODO: handle xml:lang
            self.definition = xmlelement.findtext(NEWSMLG2+'definition', default='') # TODO: handle xml:lang
    def __str__(self):
        return "{} ({}, {})".format(self.name, self.alias, self.uri)

class TitleElement(Label1Type):
    """
    A short, natural-language name
    NOTE part of "more shared elements" section - might need to move this into newsmlg2.py
    """
    pass

class TItle(GenericArray):
    element_class = TitleElement

class SameAsScheme(IRIType, CommonPowerAttributes):
    """
    A URI which identifies another scheme with concepts that use the
    same codes and are semantically equivalent to the concepts of this scheme
    """
    pass
