#!/usr/bin/env python

"""
"Ext" extension properties and associated types
"""

from .concepts import Flex1PropType
from .attributegroups import ArbitraryValueAttributes, TimeValidityAttributes


class Flex1ExtPropType(Flex1PropType, ArbitraryValueAttributes):
    """
    Flexible generic PCL-type for controlled, uncontrolled values and arbitrary
    values
    """

class Flex2ExtPropType(Flex1ExtPropType, TimeValidityAttributes):
    """
    Flexible generic PCL-Type for controlled, uncontrolled values and arbitrary
    values, with mandatory relationship
    """
    attributes = {
        # The identifier of a concept defining the semantics of the property
        # - expressed by a QCode
        # either the rel or the reluri attribute MUST be used
        'rel': {
            'xml_name': 'rel'
        },
        # The identifier of a concept defining the semantics of the property
        # - expressed by a URI
        # either the rel or the reluri attribute MUST be used
        'reluri': {
            'xml_name': 'reluri'
        }
    }

class ConceptExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """
