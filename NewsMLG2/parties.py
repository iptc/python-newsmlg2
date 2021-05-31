#!/usr/bin/env python

"""
Party details - Person and Organisation
"""

from .core import GenericArray
from .attributegroups import CommonPowerAttributes, TimeValidityAttributes
from .complextypes import TruncatedDateTimePropType
# from .conceptgroups import ConceptDefinitionGroup
from .conceptrelationships import ConceptRelationshipsGroup

class Born(TruncatedDateTimePropType):
    """
    The date the person was born.
    """

class Died(TruncatedDateTimePropType):
    """
    The date the person died.
    """


#class FlexOrganisationPropType(ConceptDefinitionGroup, ConceptRelationshipsGroup, commonPowerAttributes, qualifyingAttributes, I18NAttributes):
#    """
#    Flexible organisation data type for both controlled and uncontrolled values
#    """
#    elements = {
#        'born': { 'type': 'single', 'xml_name': 'born', 'element_class': Born },
#        'organisation_details': { 'type': 'single', 'xml_name': 'organisationDetails', 'element_class': OrganisationDetails }
#    }


#class PersonAffiliationType(FlexOrganisationPropType, TimeValidityAttributes):
#    """
#    The type for an affliation of a person to an organisation (Type defined in this XML Schema only)
#    """


#class PersonAffiliationElement(PersonAffiliationType):
#    """
#    An affiliation of the person with an organisation.
#    """


#class PersonAffiliation(GenericArray):
#    """
#    An array of PersonAffiliationElement objects.
#    """
#    element_class = PersonAffiliationElement


#class ContactInfoElement(ContactInfoType):
#    """
#    Information how to contact the person.
#    """
#
#
#class ContactInfo(GenericArray):
#    """
#    An array of ContactInfoElement objects.
#    """
#    element_class = ContactInfoElement


class PersonDetails(CommonPowerAttributes):
    """
    A set of properties specific to a person
    """
    elements = {
        'born': { 'type': 'single', 'xml_name': 'born', 'element_class': Born },
        'died': { 'type': 'single', 'xml_name': 'died', 'element_class': Died },
# TODO        'affiliation': { 'type': 'array', 'xml_name': 'affiliation', 'element_class': PersonAffiliation },
# TODO       'contact_info': { 'type': 'array', 'xml_name': 'contactInfo', 'element_class': ContactInfo },
    }

class OrganisationDetails(CommonPowerAttributes):
    """
    TODO
    """
