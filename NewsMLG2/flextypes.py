#!/usr/bin/env python

"""
Handle flex types. Should we merge this with something else?
"""

from .concepts import (
    Flex1PropType
)
from .attributegroups import (
    QuantifyAttributes
)

class AudienceType(Flex1PropType, QuantifyAttributes):
    """
    The type to cover all qualifers for an audience property
    """
    attributes = {
        # A qualifier which indicates the expected significance of the content
        # for this specific audience.
        'significance': 'significance' # type="Int1to9Type" use="optional">
    }
