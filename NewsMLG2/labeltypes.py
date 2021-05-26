#!/usr/bin/env python

"""
NAR Label Types
"""

from .attributegroups import (
    CommonPowerAttributes, I18NAttributes
)


class Label1Type(CommonPowerAttributes, I18NAttributes):
    """
    The PCL-type for information about the content as natural language string
    with minimal markup
    """
    # TODO:
    #elements = {
    #    'a': 'a',
    #    'span': 'span',
    #    'ruby': 'ruby',
    #    'inline': 'inline'
    #}
    attributes = {
        # A refinement of the semantics of the label - expressed by a QCode
        'role': 'role',  # type="QCodeListType" use="optional">
        # A refinement of the semantics of the label - expressed by a URI
        'roleuri': 'roleuri',  # type="IRIListType" use="optional">
        # An indication of the target media type(s), values as defined by the
        # Cascading Style Sheets specification [CSS].
        'media': 'media'  # " type="xs:NMTOKENS" use="optional">
    }


class BlockType(CommonPowerAttributes, I18NAttributes):
    """
    The type for nformation about the content as natural language
    string with minimal markup and line breaks
    """
    # TODO:
    """
          <xs:choice minOccurs="0" maxOccurs="unbounded">
         <xs:element ref="a"/>
         <xs:element ref="span"/>
         <xs:element ref="ruby"/>
         <xs:element ref="br"/>
         <xs:element ref="inline"/>
         <xs:any namespace="##other" processContents="lax">
            <xs:annotation>
               <xs:documentation>Extension point for provider-defined properties from other namespaces</xs:documentation>
            </xs:annotation>
         </xs:any>
      </xs:choice>
    """
    attributes = {
        # An indication of the target media type(s) values as
        # defined by the Cascading Style Sheets (CSS) specification.
        'media': 'media',
        # A refinement of the semantics of the block.
        'role': 'role',  # type="QCodeListType"
        'roleuri': 'roleuri'  # type="IRIType">
    }
