#!/usr/bin/env python

"""
Link is used by many other classes
so it needs to live in its own file
to avoid import loops.
"""

from .core import BaseObject
from .catalogstore import CATALOG_STORE
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes,
    TimeValidityAttributes
)


class TargetResourceAttributes(BaseObject):
    """
    A group of attributes pertaining to any kind of link
    """
    attributes = {
        # The locator of the target resource.
        'href': {
            'xml_name': 'href',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # The  provider’s identifier of the target resource.
        'residref': {
            'xml_name': 'residref',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # The version of the target resource. By default, the latest revision is
        # retrieved when the link is activated.
        'version': {
            'xml_name': 'version',
            'xml_type': 'xs:positiveInteger',
            'use': 'optional'
        },
        # Points to an element inside the target resource which must be
        # identified by an ID attribute having a value which is persistent for
        # all versions of the target resource, i.e. for its entire lifecycle.
        # (added NAR 1.8)
        'persistidref': {
            'xml_name': 'persistidref',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # he IANA (Internet Assigned Numbers Authority) MIME type of the target
        # resource.
        'contenttype': {
            'xml_name': 'contenttype',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # Version of the standard identified by contenttype.
        'contenttypestandardversion': {
            'xml_name': 'contenttypestandardversion',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # A refinement of a generic content type (i.e. IANA MIME type) by a
        # literal string value.
        'contenttypevariant': {
            'xml_name': 'contenttypevariant',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # Version of the standard identified by contenttypevariant.
        'contenttypevariantstandardversion': {
            'xml_name': 'contenttypevariantstandardversion',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # A refinement of a generic content type (i.e. IANA MIME type) by a
        # value from a controlled vocabulary - expressed by a QCode
        'format': {
            'xml_name': 'format',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # A refinement of a generic content type (i.e. IANA MIME type) by a
        # value from a controlled vocabulary - expressed by a URI
        'formaturi': {
            'xml_name': 'formaturi',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        # Version of the standard identified by the format.
        'formatstandardversion': {
            'xml_name': 'formatstandardversion',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # The size in bytes of the target resource.
        'size': {
            'xml_name': 'size',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        },
        # A short natural language name for the target resource.
        'title': {
            'xml_name': 'title',
            'xml_type': 'xs: string',
            'use': 'optional'
        }
    }


class DeprecatedLinkAttributes(BaseObject):
    """
    Deprecated attributes once used for target identifiers.
    """
    attributes = {
        # The use of this attribute is DEPRECATED, use @residref instead.
        # (was: The globally unique Identifier of the target Item.)
        'guidref': {
            'xml_name': 'guidref',
            'xml_type': 'xs:string',
            'use': 'optional'
        },
        # The use of this attribute is DEPRECATED, use @contenttype instead.
        # (was: An IANA MIME type.)
        'hreftype': {
            'xml_name': 'hreftype',
            'xml_type': 'xs:string',
            'use': 'optional'
        }
    }


class Link1Type(TargetResourceAttributes, TimeValidityAttributes,
    I18NAttributes, CommonPowerAttributes, DeprecatedLinkAttributes):
    """
    The PCL-type of a link from the current Item to a target Item or Web resource
    """
    attributes = {
        # The identifier of the relationship between the current Item and the
        # target resource - expressed by a QCode
        'rel': {
            'xml_name': 'rel',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # The identifier of the relationship between the current Item and the
        # target resource - expressed by a URI
        'reluri': {
            'xml_name': 'reluri',
            'xml_type': 'IRIType',
            'use': 'optional'
        },
        'rank': {
            'xml_name': 'rank',
            'xml_type': 'xs:nonNegativeInteger',
            'use': 'optional'
        }
    }


class Link(Link1Type):
    """
    A link from the current Item to a target Item or Web resource
    """


class RemoteInfo(Link1Type):
    """
    A link to an item or a web resource which provides information about the
    concept
    """
