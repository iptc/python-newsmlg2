# flextypes.py

from .conceptgroups import (
    Flex1PropType
)
from .attributegroups import (
    CommonPowerAttributes, I18NAttributes, QuantifyAttributes
)

class AudienceType(Flex1PropType, QuantifyAttributes):
    """
    The type to cover all qualifers for an audience property
    """
    attributes = {
        # A qualifier which indicates the expected significance of the content for this specific audience.
        'significance': 'significance' # type="Int1to9Type" use="optional">
    }
