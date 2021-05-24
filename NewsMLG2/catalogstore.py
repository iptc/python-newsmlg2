#!/usr/bin/env python

# Singleton for storing catalogs being processed
# needs to be in a separate file to avoid import loops

class AliasNotFoundInCatalogs(Exception):
    """Alias prefix not found in any catalogs"""
    pass

class CatalogStore(list):
    def __add__(self, rhs):
        return CatalogStore(list.__add__(self, rhs))

    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        try:
            return CatalogStore(result)
        except TypeError:
            return result

    def getSchemeForAlias(self, alias):
        for catalog in self:
            scheme = catalog.getSchemeForAlias(alias)
            if scheme is not None:
                return scheme
        raise AliasNotFoundInCatalogs()

CATALOG_STORE = CatalogStore([])
