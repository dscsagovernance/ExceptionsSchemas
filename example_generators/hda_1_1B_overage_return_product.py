import os
import json
import sys
from pathlib import Path
import uuid
import time
import random

current_file_path = Path(__file__).resolve()  
project_root = current_file_path.parent.parent  
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import all classes from exception_data_models.py
from data_models.exception_data_model import (
    ExceptionReport, ExceptionResponse, ContactInformation, ProductNoEPCISDescription,
    EPCISNoProductDescription, OveragesUnderages, Resolution, ObservationSource,
    ResolutionResponse, ResponseItem, AlternativeResolution, FollowUpMethod,
    GLNError, GTINError, MasterDataErrors, Exceptions, DataMisalignmentDescription
)

# Define the namespace (this could be one of the predefined ones or a custom UUID)
namespace = uuid.NAMESPACE_DNS

# Define the name (this is a string that you provide)



case_uuid = str(uuid.uuid5(namespace, str(random.random())))
report_time = int(time.time())
response_time = report_time + 3600
report_2_time = response_time + 3600
po_number = 'PO123456789'

overage_uuid = str(uuid.uuid5(namespace, str(random.random())))
overage_gtin = '23456789012345'

report_message_uuid = str(uuid.uuid5(namespace, str(random.random())))
po_number = 'ABD1234'

response_message_uuid = str(uuid.uuid5(namespace, str(random.random())))

report_2_message_uuid = str(uuid.uuid5(namespace, str(random.random())))


# Create an example of every class with fictional data
wholesaler_contact_info = ContactInformation(email="contact@wholesaler.com", vp="jwt...", gln="1234567890123", phone="123-456-7890")
manufacturer_contact_info = ContactInformation(email="contact@manufacturer.com", vp="jwt...", gln="1234567890124", phone="123-456-7891")


overages = OveragesUnderages(
    exception_item_uuid=overage_uuid,
    gtin=overage_gtin,
    quantity_ordered=100,
    quantity_received=110,
    resolution_request=Resolution.RETURN_PRODUCT
)



exceptions = Exceptions(
    overages=[overages],
)

exception_report = ExceptionReport(
    message_uuid=report_message_uuid,
    exception_case_uuid=case_uuid,
    timestamp=report_time,
    po_number=po_number,
    sender_information=wholesaler_contact_info,
    exceptions=exceptions,
    other_errors=["Other unspecified error."],
    case_resolved=False
)


overage_response_item = ResponseItem(
    exception_item_uuid=overage_uuid,
    resolution_response=ResolutionResponse.ACCEPT,
    comments="Accepted the overage issue.",
)



exception_response = ExceptionResponse(
    message_uuid=response_message_uuid,
    exception_case_uuid=case_uuid,
    timestamp=response_time,
    sender_information=manufacturer_contact_info,
    po_number=po_number,
    response_items=[overage_response_item],
    additional_notes="All issues have been reviewed. Did not accept the data no product issue"
)

exception_report_2 = ExceptionReport(
    message_uuid=report_2_message_uuid,
    exception_case_uuid=case_uuid,
    timestamp=report_2_time,
    sender_information=wholesaler_contact_info,
    po_number=po_number,
    case_resolved=True
)

with open(os.path.join('examples', 'hda_1_1B_overage_return_product_report.json'), 'w') as f:
    f.write(exception_report.model_dump_json())

with open(os.path.join('examples', 'hda_1_1B_overage_return_product_response.json'), 'w') as f:
    f.write(exception_response.model_dump_json())

with open(os.path.join('examples', 'hda_1_1B_overage_return_product_report_2.json'), 'w') as f:
    f.write(exception_report_2.model_dump_json())
