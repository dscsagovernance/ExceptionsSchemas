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
    GLNError, GTINError, MasterDataErrors, Exceptions
)

# Define the namespace (this could be one of the predefined ones or a custom UUID)
namespace = uuid.NAMESPACE_DNS

# Define the name (this is a string that you provide)



case_uuid = str(uuid.uuid5(namespace, str(random.random())))
report_time = int(time.time())
response_time = report_time + 3600
report_2_time = response_time + 3600
po_number = 'PO123456789'

gln_uuid = str(uuid.uuid5(namespace, str(random.random())))
gtin_uuid = str(uuid.uuid5(namespace, str(random.random())))
invalid_gtin = '12345678901234'
new_gtin = '12345678909876'
invalid_gln = '123456789'
new_gln = '123456780'


pnd_uuid = str(uuid.uuid5(namespace, str(random.random())))

dnp_uuid = str(uuid.uuid5(namespace, str(random.random())))
dnp_gtin = '01234567890123'
dnp_serial = '12121212121212'

overage_uuid = str(uuid.uuid5(namespace, str(random.random())))
overage_gtin = '23456789012345'

underage_uuid = str(uuid.uuid5(namespace, str(random.random())))
underage_gtin = '23456789012344'

report_message_uuid = str(uuid.uuid5(namespace, str(random.random())))
po_number = 'ABD1234'

response_message_uuid = str(uuid.uuid5(namespace, str(random.random())))

report_2_message_uuid = str(uuid.uuid5(namespace, str(random.random())))


# Create an example of every class with fictional data
wholesaler_contact_info = ContactInformation(email="contact@wholesaler.com", vp="jwt...", gln="1234567890123", phone="123-456-7890")
manufacturer_contact_info = ContactInformation(email="contact@manufacturer.com", vp="jwt...", gln="1234567890124", phone="123-456-7891")
gln_error = GLNError(exception_item_uuid=gln_uuid, invalid_gln=invalid_gln, proposed_gln=new_gln)
gtin_error = GTINError(exception_item_uuid=gtin_uuid, invalid_gtin=invalid_gtin, proposed_gtin=new_gtin)

master_data_errors = MasterDataErrors(
    gln_errors=[gln_error],
    gtin_errors=[gtin_error]
)

missing_data = ProductNoEPCISDescription(
    exception_item_uuid=pnd_uuid,
    product_gtin=invalid_gtin,
    observation_source=ObservationSource.PACKING_SLIP,
    resolution_request=Resolution.SEND_DATA
)

missing_product = EPCISNoProductDescription(
    exception_item_uuid=dnp_uuid,
    file_id="file-123.xml",
    product_gtin=dnp_gtin,
    product_serial=dnp_serial,
    resolution_request=Resolution.CREDIT_ACCOUNT
)

overages = OveragesUnderages(
    exception_item_uuid=overage_uuid,
    gtin=overage_gtin,
    quantity_ordered=100,
    quantity_received=110,
    resolution_request=Resolution.SEND_BACK_PRODUCT
)

underages = OveragesUnderages(
    exception_item_uuid=underage_uuid,
    gtin=underage_gtin,
    quantity_ordered=100,
    quantity_received=90,
    resolution_request=Resolution.SEND_PRODUCT
)

exceptions = Exceptions(
    missing_data=[missing_data],
    missing_product=[missing_product],
    overages=[overages],
    underages=[underages],
    master_data_errors = master_data_errors
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

pnd_response_item = ResponseItem(
    exception_item_uuid=pnd_uuid,
    resolution_response=ResolutionResponse.ACCEPT,
    comments="Accepted the missing data issue.",
)

dnp_response_item = ResponseItem(
    exception_item_uuid=dnp_uuid,
    resolution_response=ResolutionResponse.ACCEPT,
    comments="Shipped product already on it's way, no account credit needed.",
    alternative_resolution=AlternativeResolution(
        alternative_resolution=Resolution.SEND_PRODUCT,
        follow_up=FollowUpMethod.EMAIL,
        follow_up_details="Product is already coming"
    )
)


overage_response_item = ResponseItem(
    exception_item_uuid=overage_uuid,
    resolution_response=ResolutionResponse.ACCEPT,
    comments="Accepted the overage issue.",
)

underage_response_item = ResponseItem(
    exception_item_uuid=underage_uuid,
    resolution_response=ResolutionResponse.ACCEPT,
    comments="Accepted the underage issue.",
)

gtin_response_item = ResponseItem(
    exception_item_uuid=gtin_uuid,
    resolution_response=ResolutionResponse.ACCEPT,
    comments="Accepted the gtin issue.",
)

gln_response_item = ResponseItem(
    exception_item_uuid=underage_uuid,
    resolution_response=ResolutionResponse.ACCEPT,
    comments="Accepted the gln issue.",
)

exception_response = ExceptionResponse(
    message_uuid=response_message_uuid,
    exception_case_uuid=case_uuid,
    timestamp=response_time,
    sender_information=manufacturer_contact_info,
    po_number=po_number,
    response_items=[pnd_response_item, dnp_response_item, overage_response_item, underage_response_item, gln_response_item, gtin_response_item],
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

print(json.dumps(json.loads(exception_report.json()), indent=2))
print(json.dumps(json.loads(exception_response.json()), indent=2))
print(json.dumps(json.loads(exception_report_2.json()), indent=2))