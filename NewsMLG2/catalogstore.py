#!/usr/bin/env python

"""
Singleton for storing catalogs that will be processed in NewsMLG2 files.

Needs to be in a separate file to avoid import loops.
"""

class AliasNotFoundInCatalogs(Exception):
    """Alias prefix not found in any catalogs"""


class URINotFoundInCatalogs(Exception):
    """Catalog URI not found in any catalogs"""


class CatalogStore(list):
    """
    Singleton class to handle all catalogs used
    in this NewsMLG2 processor.
    """
    def __add__(self, rhs):
        return CatalogStore(list.__add__(self, rhs))

    def __getitem__(self, item):
        """
        Return a given catalog in our list.
        """
        result = list.__getitem__(self, item)
        try:
            return CatalogStore(result)
        except TypeError:
            return result

    def get_scheme_for_alias(self, alias):
        """
        Return the catalog scheme matching a given alias.
        e.g. 'nrol' would return the Scheme for 'name role'.
        """
        for catalog in self:
            scheme = catalog.get_scheme_for_alias(alias)
            if scheme is not None:
                return scheme
        raise AliasNotFoundInCatalogs()

    def get_scheme_for_uri(self, uri):
        """
        Return the catalog scheme matching a given URI.
        e.g. 'https://cv.iptc.org/newscodes/scene' would return the Scheme for
        'scene'.
        """
        for catalog in self:
            scheme = catalog.get_scheme_for_uri(uri)
            if scheme is not None:
                return scheme
        raise URINotFoundInCatalogs()


CATALOG_STORE = CatalogStore([])
