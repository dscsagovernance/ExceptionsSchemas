# PDG Exceptions Schema

Uses Pydantic to build a JSON schema from a data model for exceptions https://docs.pydantic.dev/latest/concepts/json_schema/

## Example flow

### Wholesaler reports an exception
```
{
  "message_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
  "exception_case_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
  "timestamp": 1711488776,
  "po_number": "ABD1234",
  "sender_information": {
    "vp": "jwt...",
    "gln": "1234567890123",
    "email": "contact@wholesaler.com",
    "phone": "123-456-7890"
  },
  "exceptions": {
    "missing_data": [
      {
        "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
        "product_gtin": "12345678901234",
        "observation_source": "Packing Slip",
        "resolution_request": "Send new data",
        "product_serial": null
      }
    ],
    "missing_product": [
      {
        "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
        "file_id": "file-123.xml",
        "product_gtin": "01234567890123",
        "product_serial": "12121212121212",
        "resolution_request": "Credit account"
      }
    ],
    "overages": [
      {
        "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
        "gtin": "23456789012345",
        "quantity_ordered": 100,
        "quantity_received": 110,
        "resolution_request": "Send back product"
      }
    ],
    "underages": [
      {
        "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
        "gtin": "23456789012344",
        "quantity_ordered": 100,
        "quantity_received": 90,
        "resolution_request": "Send product"
      }
    ],
    "master_data_errors": {
      "gln_errors": [
        {
          "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
          "invalid_gln": "123456789",
          "proposed_gln": "123456780",
          "resolution_request": null
        }
      ],
      "gtin_errors": [
        {
          "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
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
  "message_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
  "exception_case_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
  "timestamp": 1711492376,
  "sender_information": {
    "vp": "jwt...",
    "gln": "1234567890124",
    "email": "contact@manufacturer.com",
    "phone": "123-456-7891"
  },
  "po_number": "ABD1234",
  "response_items": [
    {
      "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
      "resolution_response": "Accept",
      "comments": "Accepted the missing data issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
      "resolution_response": "Accept",
      "comments": "Shipped product already on it's way, no account credit needed.",
      "alternative_resolution": {
        "alternative_resolution": "Send product",
        "follow_up": "Email",
        "follow_up_details": "Product is already coming"
      }
    },
    {
      "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
      "resolution_response": "Accept",
      "comments": "Accepted the overage issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
      "resolution_response": "Accept",
      "comments": "Accepted the underage issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
      "resolution_response": "Accept",
      "comments": "Accepted the gln issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
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
  "message_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
  "exception_case_uuid": "cfbff0d1-9375-5685-968c-48ce8b15ae17",
  "timestamp": 1711495976,
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