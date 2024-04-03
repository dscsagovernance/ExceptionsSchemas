# PDG Exceptions Schema

Uses Pydantic to build a JSON schema from a data model for exceptions https://docs.pydantic.dev/latest/concepts/json_schema/

## Example flow

### Wholesaler reports an exception
```
{
  "message_uuid": "4121981f-8752-5dc1-b234-61fb7f687acd",
  "exception_case_uuid": "106da6e9-68a0-569f-b550-53290c97132c",
  "timestamp": 1712180064,
  "po_number": "ABD1234",
  "sender_information": {
    "vp": "jwt...",
    "gln": "1234567890123",
    "email": "contact@wholesaler.com",
    "phone": "123-456-7890"
  },
  "exceptions": {
    "missing_product_data": [
      {
        "exception_item_uuid": "40974a8d-6fe3-549b-bec9-0b28d8121ead",
        "product_gtin": "12345678901234",
        "observation_source": "Packing Slip",
        "resolution_request": "Send new data",
        "product_serial": null
      }
    ],
    "missing_product": [
      {
        "exception_item_uuid": "502b4cef-1281-53fe-a958-988d7bc389bc",
        "file_id": "file-123.xml",
        "product_gtin": "01234567890123",
        "product_serial": "12121212121212",
        "resolution_request": "Credit account"
      }
    ],
    "data_misalignment": [
      {
        "exception_item_uuid": "1552962d-7d1e-546a-a67c-bd83e280a2cd",
        "received_product_gtin": "01234567890123",
        "received_product_lot": "A1234",
        "received_product_expiry": "01012027",
        "received_product_serial": "121212121212",
        "product_data_gtin": "01234567890123",
        "product_data_lot": "A1234",
        "product_data_expiry": "01012027",
        "product_data_serial": "232323232323",
        "resolution_request": "Send new data"
      }
    ],
    "overages": [
      {
        "exception_item_uuid": "eff0f6e6-23ff-533a-a68c-f4cb82b4a323",
        "gtin": "23456789012345",
        "quantity_ordered": 100,
        "quantity_received": 110,
        "resolution_request": "Send back product"
      }
    ],
    "underages": [
      {
        "exception_item_uuid": "5fecec1d-3231-545e-90d2-ab97e49d10c2",
        "gtin": "23456789012344",
        "quantity_ordered": 100,
        "quantity_received": 90,
        "resolution_request": "Send product"
      }
    ],
    "master_data_errors": {
      "gln_errors": [
        {
          "exception_item_uuid": "2dc6e4f4-2a5c-5130-9b75-501029fd6d17",
          "invalid_gln": "123456789",
          "proposed_gln": "123456780",
          "resolution_request": null
        }
      ],
      "gtin_errors": [
        {
          "exception_item_uuid": "9e5fd2e8-9eb4-58cb-8624-7549bf9eaf76",
          "invalid_gtin": "12345678901234",
          "proposed_gtin": "12345678909876",
          "resolution_request": null
        }
      ]
    }
  },
  "other_errors": [
    "Other unspecified error."
  ],
  "case_resolved": false
}
```
### Manufacturer reponds to the exceptions
```
{
  "message_uuid": "fbb0fdf6-a90d-5aea-9cfc-38f65e91b990",
  "exception_case_uuid": "106da6e9-68a0-569f-b550-53290c97132c",
  "timestamp": 1712183664,
  "sender_information": {
    "vp": "jwt...",
    "gln": "1234567890124",
    "email": "contact@manufacturer.com",
    "phone": "123-456-7891"
  },
  "po_number": "ABD1234",
  "response_items": [
    {
      "exception_item_uuid": "40974a8d-6fe3-549b-bec9-0b28d8121ead",
      "resolution_response": "Accept",
      "comments": "Accepted the missing data issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "502b4cef-1281-53fe-a958-988d7bc389bc",
      "resolution_response": "Accept",
      "comments": "Shipped product already on it's way, no account credit needed.",
      "alternative_resolution": {
        "alternative_resolution": "Send product",
        "follow_up": "Email",
        "follow_up_details": "Product is already coming"
      }
    },
    {
      "exception_item_uuid": "1552962d-7d1e-546a-a67c-bd83e280a2cd",
      "resolution_response": "Accept",
      "comments": "Sent updated EPCIS",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "eff0f6e6-23ff-533a-a68c-f4cb82b4a323",
      "resolution_response": "Accept",
      "comments": "Accepted the overage issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "5fecec1d-3231-545e-90d2-ab97e49d10c2",
      "resolution_response": "Accept",
      "comments": "Accepted the underage issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "5fecec1d-3231-545e-90d2-ab97e49d10c2",
      "resolution_response": "Accept",
      "comments": "Accepted the gln issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "9e5fd2e8-9eb4-58cb-8624-7549bf9eaf76",
      "resolution_response": "Accept",
      "comments": "Accepted the gtin issue.",
      "alternative_resolution": null
    }
  ],
  "additional_notes": "All issues have been reviewed. Did not accept the data no product issue"
}
```
### Wholesaler responds saying all is ok
```
{
  "message_uuid": "59342403-fd81-523e-a2f6-7e2177037968",
  "exception_case_uuid": "106da6e9-68a0-569f-b550-53290c97132c",
  "timestamp": 1712187264,
  "po_number": "ABD1234",
  "sender_information": {
    "vp": "jwt...",
    "gln": "1234567890123",
    "email": "contact@wholesaler.com",
    "phone": "123-456-7890"
  },
  "exceptions": {},
  "other_errors": null,
  "case_resolved": true
}
```