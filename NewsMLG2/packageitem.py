"""
packageitem classes
"""

from .anyitem import (
    AnyItem, Assert, DerivedFrom, DerivedFromValue, InlineRef
)
from .attributegroups import CommonPowerAttributes, I18NAttributes
from .conceptrelationships import FlexPropType
from .contentmeta import ContentMetadataAfDType
from .extensionproperties import Flex2ExtPropType
from .itemmanagement import EdNote, Signal, Title
from .link import Link1Type
from .partmeta import PartMeta


class PackageItemContentMeta(ContentMetadataAfDType):
    """
    A set of properties about the content
    """
    xml_element_name = 'contentMeta'


class GroupRef(CommonPowerAttributes):
    """
    A reference to a group local to the package
    """
    attributes = {
        # The reference to the id of a local group
        'idref': {
            'xml_name': 'idref',
            'xml_type': 'xs:IDREF',
            'use': 'required'
        }
    }


class ItemRef(Link1Type):
    """
    A reference to a target item or Web resource
    """


class ConceptRef(FlexPropType):
    """
    A reference to a target concept
    """


class GroupExtProperty(Flex2ExtPropType):
    """
    Extension Property; the semantics are defined by the concept referenced by
    the rel attribute. The semantics of the Extension Property must have the
    same scope as the parent property.
    """


class Group(CommonPowerAttributes, I18NAttributes):
    """
    A mixed set of group references and references to items or Web resources
    """
    elements = [
        ('groupref', {
            'type': 'array',
            'xml_name': 'groupRef',
            'element_class': GroupRef
        }),
        ('itemref', {
            'type': 'array',
            'xml_name': 'itemRef',
            'element_class': ItemRef
        }),
        ('conceptref', {
            'type': 'array',
            'xml_name': 'conceptRef',
            'element_class': ConceptRef
        }),
        ('title', {
            'type': 'array',
            'xml_name': 'title',
            'element_class': Title
        }),
        ('signal', {
            'type': 'array',
            'xml_name': 'signal',
            'element_class': Signal
        }),
        ('ednote', {
            'type': 'array',
            'xml_name': 'edNote',
            'element_class': EdNote
        }),
        ('groupextproperty', {
            'type': 'array',
            'xml_name': 'groupExtProperty',
            'element_class': GroupExtProperty
        })
    ]
    attributes = {
        # The part this group plays within its container -
        # expressed by a QCode
        # Either the role or the roleuri attribute MUST be used
        'role': {
            'xml_name': 'role',
            'xml_type': 'QCodeType',
        },
        # The part this group plays within its container -
        # expressed by a URI
        # Either the role or the roleuri attribute MUST be used
        'roleuri': {
            'xml_name': 'roleuri',
            'xml_type': 'IRIType'
        },
        # An indication whether the elements in the group are complementary
        # and unordered, complementary and ordered or a set of alternative
        # elements - expressed by a QCode
        'mode': {
            'xml_name': 'mode',
            'xml_type': 'QCodeType',
            'use': 'optional'
        },
        # An indication whether the elements in the group are complementary
        # and unordered, complementary and ordered or a set of alternative
        # elements - expressed by a URI
        'modeuri': {
            'xml_name': 'modeuri',
            'xml_type': 'IRIType',
            'use': 'optional'
        }
    }


class GroupSet(CommonPowerAttributes):
    """
    A hierarchical set of groups
    """
    elements = [
        ('group', {
            'type': 'array',
            'xml_name': 'group',
            'element_class': Group
        })
    ]
    attributes = {
        # The reference to a local group acting as the root of the hierarchy
        # of groups
        'root': {
            'xml_name': 'root',
            'xml_type': 'xs:IDREF',
            'use': 'required'
        }
    }


class PackageItem(AnyItem):
    """
    An Item used for packaging references to other Items and Web resources.
    """
    elements = [
        ('contentmeta', {
            'type': 'single',
            'xml_name': 'contentMeta',
            'element_class': PackageItemContentMeta
        }),
        ('partmeta', {
            'type': 'array',
            'xml_name': 'partMeta',
            'element_class': PartMeta
        }),
        ('assert', {
            'type': 'array',
            'xml_name': 'assert',
            'element_class': Assert
        }),
        ('inlineRef', {
            'type': 'array',
            'xml_name': 'inlineRef',
            'element_class': InlineRef
        }),
        ('derivedfrom', {
            'type': 'array',
            'xml_name': 'derivedFrom',
            'element_class': DerivedFrom
        }),
        ('derivedfromvalue', {
            'type': 'array',
            'xml_name': 'derivedFromValue',
            'element_class': DerivedFromValue
        }),
        ('groupset', {
            'type': 'single',
            'xml_name': 'groupSet',
            'element_class': GroupSet
        })
    ]
