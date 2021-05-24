#!/usr/bin/env python

# Link type

from .core import BaseObject
from .conceptgroups import Flex2ExtPropType
from .attributegroups import TimeValidityAttributes, I18NAttributes, CommonPowerAttributes

class TargetResourceAttributes(BaseObject):
    """
    A group of attributes pertaining to any kind of link
    """
    attributes = {
        # The locator of the target resource.
        'href': 'href',  # type="IRIType" use="optional">
        # The  provider’s identifier of the target resource.
        'residref': 'residref',  # type="xs:string" use="optional">
        # The version of the target resource. By default, the latest revision is retrieved when the link is activated.
        'version': 'version',  # type="xs:positiveInteger" use="optional">
        # Points to an element inside the target resource which must be identified by an ID attribute having a value which is persistent for all versions of the target resource, i.e. for its entire lifecycle. (added NAR 1.8)
        'persistidref': 'persistidref',  # type="xs:string" use="optional">
        # he IANA (Internet Assigned Numbers Authority) MIME type of the target resource.
        'contenttype': 'contenttype',  # type="xs:string" use="optional">
        # Version of the standard identified by contenttype.
        # type="xs:string" use="optional">
        'contenttypestandardversion': 'contenttypestandardversion',
        # A refinement of a generic content type (i.e. IANA MIME type) by a literal string value.
        'contenttypevariant': 'contenttypevariant',  # type="xs:string" use="optional">
        # Version of the standard identified by contenttypevariant.
        # type="xs:string" use="optional">
        'contenttypevariantstandardversion': 'contenttypevariantstandardversion',
        # A refinement of a generic content type (i.e. IANA MIME type) by a value from a controlled vocabulary - expressed by a QCode
        'format': 'format',  # type="QCodeType" use="optional">
        # A refinement of a generic content type (i.e. IANA MIME type) by a value from a controlled vocabulary - expressed by a URI
        'formaturi': 'formaturi',  # type="IRIType" use="optional">
        # Version of the standard identified by the format.
        # type="xs:string" use="optional">
        'formatstandardversion': 'formatstandardversion',
        # The size in bytes of the target resource.
        'size': 'size',  # type="xs:nonNegativeInteger" use="optional">
        # A short natural language name for the target resource.
        'title': 'title',  # " type="xs: string" use="optional">
    }


class DeprecatedLinkAttributes(BaseObject):
    attributes = {
        # The use of this attribute is DEPRECATED, use @residref instead.
        # (was: The globally unique Identifier of the target Item.)
        'guidref': 'guidref',  # " type="xs:string" use="optional">
        # The use of this attribute is DEPRECATED, use @contenttype instead.
        # (was: An IANA MIME type.)
        'hreftype': 'hreftype',  # " type="xs:string" use="optional">
    }

class Link1Type(TargetResourceAttributes, TimeValidityAttributes, I18NAttributes, CommonPowerAttributes, DeprecatedLinkAttributes):
    """
    The PCL-type of a link from the current Item to a target Item or Web resource
    """
    attributes = {
        # The identifier of the relationship between the current Item and the target resource - expressed by a QCode
        'rel': 'rel',  # type="QCodeType" use="optional">
        # The identifier of the relationship between the current Item and the target resource - expressed by a URI
        'reluri': 'reluri',  # type="IRIType" use="optional">
        'rank': 'rank',  # type="xs:nonNegativeInteger" use="optional">
    }

class ItemMetaExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by the rel attribute.
    The semantics of the Extension Property must have the same scope as the parent property.
    """
    pass
