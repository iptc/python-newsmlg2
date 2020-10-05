#!/usr/bin/env python

import json
import os

from lxml import etree

DEBUG = False
# DEBUG = True

from .core import NEWSMLG2_NS, BaseObject

CATALOGS = {
    'http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_35.xml':
        'catalogs/catalog.IPTC-G2-Standards_35.xml'
}

class CatalogMixin(object):
    def buildCatalog(self, xmlelement, **kwargs):
        catalogs = xmlelement.findall(NEWSMLG2_NS+'catalog')
        catalogRefs = xmlelement.findall(NEWSMLG2_NS+'catalogRef')
        for catalog in catalogs:
            # NOTE inline catalogs not yet tested
            self.addCatalog(xmlelement=catalog)
        for catalogRef in catalogRefs:
            href = catalogRef.get('href')

            if href in CATALOGS:
                # IPTC standard catalogs are built in, to avoid network traffic
                file = CATALOGS[href]
                if DEBUG:
                    print("Loading built-in catalog {}".format(file))
                self.addCatalog(file=file)
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
            self.catalog = Catalog(xmlelement=catalog_element)
        elif 'xmlelement' in kwargs:
            self.catalog = Catalog(xmlelement=xmlelement)

    def getCatalog(self):
        return self.catalog

class Catalog(BaseObject):
    """
    A local or remote catalog.
    """

    def __init__(self, **kwargs):
        super(Catalog, self).__init__(**kwargs)
        self._catalog = []
        self._catalog_uri_lookup = {}
        self._catalog_alias_lookup = {}
        xmlelement = kwargs.get('xmlelement')
        assert type(xmlelement) == etree._Element
        assert xmlelement.tag == NEWSMLG2_NS+'catalog'
        schemes = xmlelement.findall(NEWSMLG2_NS+'scheme')
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
        return self._catalog_alias_lookup[alias]

    def __iter__(self):
        for key in self._catalog.keys():
            yield key

    def __getitem__(self,index):
        return self._catalog[index]

    def __len__(self):
        return len(self._catalog)

    def __dict__(self):
        return dict(self._catalog)


class Scheme(object):
    """
    A scheme alias-to-URI mapping.
    """
    def __init__(self, xmlelement=None, **kwargs):
        if xmlelement is not None:
            self.alias = xmlelement.get('alias', '')
            self.uri = xmlelement.get('uri', '')
            self.authority = xmlelement.get('authority', '')
            self.modified = xmlelement.get('modified', '')
            self.name = xmlelement.findtext(NEWSMLG2_NS+'name', default='') # TODO: handle xml:lang
            self.definition = xmlelement.findtext(NEWSMLG2_NS+'definition', default='') # TODO: handle xml:lang
    def __str__(self):
        return "{} ({}, {})".format(self.name, self.alias, self.uri)
