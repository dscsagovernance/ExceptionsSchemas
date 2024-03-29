import json
from enum import Enum
from typing import Union, Dict, Optional

from typing_extensions import Annotated, TypedDict

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.config import ConfigDict
from typing import List, Dict
from pathlib import Path



################################
# General Purpose Data Models
################################

class ContactInformation(BaseModel):
    vp: Optional[str] = None
    gln: Optional[str] = None
    email: str
    phone: Optional[str] = None

    @model_validator(mode='before')
    def check_email_or_phone(cls, values):
        if not (values.get('email') or values.get('phone')):
            raise ValueError('Either email or phone must be provided.')
        return values


class Resolution(Enum):
    SEND_DATA = "Send new data"
    SEND_PRODUCT = "Send product"
    RETURN_PRODUCT = "Return product"
    SEND_BACK_PRODUCT = "Send back product"
    CREDIT_ACCOUNT = "Credit account"
    DEBIT_ACCOUNT = "Debit account"


##############################
# Report Specific Data Models
##############################

class EPCISStatus(Enum):
    OK = "Ok"
    SYNTAX_ERROR = "Syntax error"
    NOT_RECEIVED = "Not received"
    OTHER_ERRORS = "Other errors"

class ObservationSource(Enum):
    SCAN = "Scan"
    PACKING_SLIP = "Packing Slip"
    ASN = "ASN"
    OTHER = "Other"


class ProductNoEPCISDescription(BaseModel):
    exception_item_uuid: str
    product_gtin: str
    observation_source: ObservationSource
    resolution_request: Resolution
    product_serial: Optional[str] = None

class EPCISNoProductDescription(BaseModel):
    exception_item_uuid: str
    file_id: str
    product_gtin: str
    product_serial: str
    resolution_request: Resolution

class OveragesUnderages(BaseModel):
    exception_item_uuid: str
    gtin: str
    quantity_ordered: int
    quantity_received: int
    resolution_request: Resolution

class GLNError(BaseModel):
    exception_item_uuid: str
    invalid_gln: str
    proposed_gln: Optional[str] = None
    resolution_request: Optional[Resolution] = None 

class GTINError(BaseModel):
    exception_item_uuid: str
    invalid_gtin: str
    proposed_gtin: Optional[str] = None
    resolution_request: Optional[Resolution] = None


class MasterDataErrors(TypedDict, total=False):
    gln_errors: Optional[List[GLNError]] = None
    gtin_errors: Optional[List[GTINError]] = None

class Exceptions(TypedDict, total=False):
    missing_product_data: Optional[List[ProductNoEPCISDescription]] = []
    missing_product: Optional[List[EPCISNoProductDescription]] = []
    overages: Optional[List[OveragesUnderages]] = []
    underages: Optional[List[OveragesUnderages]] = []
    master_data_errors: Optional[MasterDataErrors] = {}

class ExceptionReport(BaseModel):
    message_uuid: str
    exception_case_uuid: str
    timestamp: int
    po_number: str
    sender_information: ContactInformation
    exceptions: Optional[Exceptions] = {}
    other_errors: Optional[List[str]] = None
    case_resolved: bool



#################################
# Response Specific Data Models
#################################    

class ResolutionResponse(Enum):
    ACCEPT = "Accept"
    REJECT = "Reject"

class FollowUpMethod(Enum):
    EMAIL = "Email"
    PHONE = "Phone"

class AlternativeResolution(BaseModel):
    alternative_resolution: Optional[Resolution]
    follow_up: Optional[FollowUpMethod]
    follow_up_details: Optional[str] = None

    @model_validator(mode='before')
    def check_follow_up(cls, values):
        if values.get("alternative_resolution") is None and not (values.get("follow_up") and values.get("follow_up_details")):
            raise ValueError('If alternative_resolution is not provided, follow_up and follow_up_details are required.')
        return values

class ResponseItem(BaseModel):
    exception_item_uuid: str # Ties back to origical exception report item
    resolution_response: ResolutionResponse
    comments: Optional[str] = None
    alternative_resolution: Optional[AlternativeResolution] = None
    '''
    @field_validator('alternative_resolution')
    def ensure_alternative_or_followup(cls, v, values):
        if values.get('resolution_response') == ResolutionResponse.REJECT and not v:
            raise ValueError('If resolution is rejected, an alternative resolution or follow-up method and details must be provided.')
        return v
    '''
class ExceptionResponse(BaseModel):
    message_uuid: str
    exception_case_uuid: str  # Ties back to the original exception report
    timestamp: int
    sender_information: ContactInformation
    po_number: str  # Purchase order number for cross-reference
    response_items: Optional[List[ResponseItem]] = []
    additional_notes: Optional[str] = None



report_schema = ExceptionReport.model_json_schema()
with open(Path('../schemas/report_schema.json'), 'w') as f:
    f.write(json.dumps(report_schema, indent=2))


response_schema = ExceptionResponse.model_json_schema()
with open(Path('../schemas/response_schema.json'), 'w') as f:
    f.write(json.dumps(response_schema, indent=2))
