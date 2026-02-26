""" Import necessary modules """
from enum import Enum

# Define the Enum
class LookupMaster(Enum):
    """
    LookupMaster is an enumeration that defines the different types of lookup masters.
    Each member of the enumeration represents a specific type of lookup master.
    """
    DATA_TYPE = "data_type"
    ENTITY_TYPE = "entity_type"
    ORGANIZATION_TYPE = "organization_type"
    USER_TYPE = "user_type"
    USER_DETAIL_TYPE = "user_detail_type"
    USER_DETAIL_SUB_TYPE = "user_detail_sub_type"
    USER_STATUS = "user_status"
