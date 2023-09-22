#!/usr/bin/env python

"""
Singleton for storing catalogs that will be processed in NewsMLG2 files.

Needs to be in a separate file to avoid import loops.
"""

class AliasNotFoundInCatalogs(Exception):
    """Alias prefix not found in any catalogs"""


class URINotFoundInCatalogs(Exception):
    """Catalog URI not found in any catalogs"""


class CatalogStore():
    """
    Singleton class to handle all catalogs used
    in this NewsMLG2 processor.
    """
    _list = []
    def __init__(self, val = []):
        self._list = val

    def append(self, rhs):
        self._list.append(rhs)
        return self

    def __getitem__(self, item):
        """
        Return a given catalog in our list.
        """
        return self._list.__getitem__(item)

    def __len__(self):
        return len(self._list)

    def get_scheme_for_alias(self, alias):
        """
        Return the catalog scheme matching a given alias.
        e.g. 'nrol' would return the Scheme for 'name role'.
        """
        for catalog in self._list:
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
        for catalog in self._list:
            scheme = catalog.get_scheme_for_uri(uri)
            if scheme is not None:
                return scheme
        raise URINotFoundInCatalogs()


CATALOG_STORE = CatalogStore([])
