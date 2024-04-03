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


 
dm_uuid = str(uuid.uuid5(namespace, str(random.random())))
dm_gtin = '01234567890123'
dm_recieved_serial = '121212121212'
dm_data_serial = '232323232323'
dm_expiry = '01012027'
dm_lot = 'A1234'


report_message_uuid = str(uuid.uuid5(namespace, str(random.random())))
po_number = 'ABD1234'

response_message_uuid = str(uuid.uuid5(namespace, str(random.random())))

report_2_message_uuid = str(uuid.uuid5(namespace, str(random.random())))


# Create an example of every class with fictional data
wholesaler_contact_info = ContactInformation(email="contact@wholesaler.com", vp="jwt...", gln="1234567890123", phone="123-456-7890")
manufacturer_contact_info = ContactInformation(email="contact@manufacturer.com", vp="jwt...", gln="1234567890124", phone="123-456-7891")

data_misalignment = DataMisalignmentDescription(
    exception_item_uuid=dm_uuid,
    received_product_gtin=dm_gtin,
    received_product_lot=dm_lot,
    received_product_expiry=dm_expiry,
    received_product_serial=dm_recieved_serial,
    product_data_gtin=dm_gtin,
    product_data_lot=dm_lot,
    product_data_expiry=dm_expiry,
    product_data_serial=dm_data_serial,
    resolution_request=Resolution.SEND_DATA
)



exceptions = Exceptions(
    data_misalignment=[data_misalignment]
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



dm_response_item = ResponseItem(
    exception_item_uuid=dm_uuid,
    resolution_response=ResolutionResponse.ACCEPT,
    comments="Sent updated EPCIS",
)



exception_response = ExceptionResponse(
    message_uuid=response_message_uuid,
    exception_case_uuid=case_uuid,
    timestamp=response_time,
    sender_information=manufacturer_contact_info,
    po_number=po_number,
    response_items=[dm_response_item],
    additional_notes="All issues have been reviewed."
)

exception_report_2 = ExceptionReport(
    message_uuid=report_2_message_uuid,
    exception_case_uuid=case_uuid,
    timestamp=report_2_time,
    sender_information=wholesaler_contact_info,
    po_number=po_number,
    case_resolved=True
)

with open(os.path.join('examples', 'hda_1_4A_incorrect_serial_report.json'), 'w') as f:
    f.write(exception_report.model_dump_json())

with open(os.path.join('examples', 'hda_1_4A_incorrect_serial_response.json'), 'w') as f:
    f.write(exception_response.model_dump_json())

with open(os.path.join('examples', 'hda_1_4A_incorrect_serial_report_2.json'), 'w') as f:
    f.write(exception_report_2.model_dump_json())

