import json
from enum import Enum
from typing import Union, Dict, Optional

from typing_extensions import Annotated

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import List, Dict

# Enum definitions
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

class ResolutionRequest(Enum):
    SEND_DATA = "Send data"
    SEND_PRODUCT = "Send product"
    RETURN_PRODUCT = "Return product"
    SEND_BACK_PRODUCT = "Send back product"

# Basic model definitions
class ProductNoEPCISDescription(BaseModel):
    product_gtin: str
    observation_source: ObservationSource
    resolution_request: ResolutionRequest

class EPCISNoProductDescription(BaseModel):
    file_id: str
    product_gtin: str
    product_serial: str
    resolution_request: ResolutionRequest

class GLNErrors(BaseModel):
    invalid_gln: str
    proposed_gln: Optional[str] = None

class GTINErrors(BaseModel):
    invalid_gtin: str
    proposed_gtin: Optional[str] = None

class OtherErrors(BaseModel):
    error_messages: List[str]

class SenderInformation(BaseModel):
    sender_vp: str
    sender_gln: Optional[str] = None
    sender_email: Optional[str] = None
    sender_phone: Optional[str] = None

# Renamed composite model with specified fields, incorporating requested changes
class ExceptionReport(BaseModel):
    po_number: str
    data_status: EPCISStatus
    product_no_data: List[ProductNoEPCISDescription]
    data_no_product: List[EPCISNoProductDescription]
    master_data_errors: Dict[str, BaseModel] = Field(default_factory=lambda: {
        "gln_errors": GLNErrors(),
        "gtin_errors": GTINErrors(),
        "other_errors": OtherErrors() # Making it optional can be done by not including it in the dictionary if not needed.
    })
    sender_information: SenderInformation



main_model_schema = ExceptionReport.model_json_schema()  # (1)!
print(json.dumps(main_model_schema, indent=2))  # (2)!