#!/usr/bin/env python

"""
id related elements
"""

from .complextypes import IntlStringType2
from .attributegroups import CommonPowerAttributes

class AltId(IntlStringType2):
    """
    An alternative identifier assigned to the content.
    """

    attributes = {
        # A qualifier which indicates the context within which the alternative
        # identifier has been allocated - expressed by a QCode
        'type': 'type',  # type="QCodeType" use="optional">
        # A qualifier which indicates the context within which the alternative
        # identifier has been allocated - expressed by a URI
        'typeuri': 'typeuri',  # type="IRIType" use="optional">
        # A qualifier which indicates the business environment in which the
        # identifier can be used to access the content - expressed by a QCode
        'environment': 'environment',  # type="QCodeListType" use="optional">
        # A qualifier which indicates the business environment in which the
        # identifier can be used to access the content - expressed by a URI
        'environmenturi': 'environmenturi',  # type="IRIListType" use="optional">
        # Indicates the format of the value of the element
        # - expressed by a QCode
        'idformat': 'idformat',  #  type="QCodeType">
        # Indicates the format of the value of the element - expressed by a URI
        'idformaturi': 'idformaturi',  # type="IRIType">
        # A refinement of what kind of alternative is provided by this identifier
        # - expressed by a QCode
        'role': 'role',  # type="QCodeType">
        # A refinement of what kind of alternative is provided by this identifier
        # - expressed by an URI
        'roleuri': 'roleuri',  # type="IRIType">
        # The version of the object identified by the alternative id.
        'version': 'version'  #  type="xs:string">
    }


class Hash(CommonPowerAttributes):
    """
    Hash value of parts of an item as defined by the hashscope attribute
    """
    attributes = {
        # The hash algorithm used for creating the hash value - expressed by a
        # QCode
        #  either the hashtype or the hashtypeuri attribute MUST be used
        'hashtype': 'hashtype',  # type="QCodeType">
        # The hash algorithm used for creating the hash value - expressed by a
        # URI
        # either the hashtype or the hashtypeuri attribute MUST be used
        'hashtypeuri': 'hashtypeuri',  # type="IRIType">
        # The scope of a G2 item's content which is the reference for creating
        # the hash value - expressed by a QCode. If the attribute is omitted,
        # http://cv.iptc.org/newscodes/hashscope/content is the default value.
        'scope': 'scope',  # type="QCodeType">
        # The scope of a G2 item's content which is the reference for creating
        # the hash value - expressed by a URI. If the attribute is omitted,
        # http://cv.iptc.org/newscodes/hashscope/content is the default value.
        'scopeuri': 'scopeuri'  # type="IRIType">
    }
