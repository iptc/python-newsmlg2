"""
Generic utils used by other classes
"""

from importlib import import_module
from .catalogstore import CATALOG_STORE


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.

    Copied from Django source code:
    https://github.com/django/django/blob/main/django/utils/module_loading.py
    """
    dotted_path = "NewsMLG2." + dotted_path
    module_path, class_name = dotted_path.rsplit('.', 1)
    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err

def qcode_to_uri(qcode):
    """
    Return the value of this property as a URI by looking up the
    qcode's prefix in the catalog
    """
    alias, code = qcode.split(':')
    # get catalog
    scheme = CATALOG_STORE.get_scheme_for_alias(alias)
    # look up catalog for alias, get URI
    uri = scheme.uri
    return uri + code

def uri_to_qcode(uri):
    """
    Return the value of this property as a qcode by looking up the
    URI's prefix in the catalog
    """
    # convert URI to qcode:
    urimainpart, code = uri.rsplit('/', 1)
    # get catalog - we need to put the slash back
    scheme = CATALOG_STORE.get_scheme_for_uri(urimainpart+'/')
    # look up catalog for URI, get prefix
    alias = scheme.alias
    return alias + ':' + code
