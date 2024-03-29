# PDG Exceptions Schema

Uses Pydantic to build a JSON schema from a data model for exceptions https://docs.pydantic.dev/latest/concepts/json_schema/

## Example flow

### Wholesaler reports an exception
```
{
  "message_uuid": "36424d90-ae99-5d7f-a244-ffccee08dabf",
  "exception_case_uuid": "2dbf3d13-e539-5e86-a43f-3ef49bc08c5d",
  "timestamp": 1711495403,
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
        "exception_item_uuid": "909df5e2-fb8a-5330-bd1a-dcd6efd658fa",
        "product_gtin": "12345678901234",
        "observation_source": "Packing Slip",
        "resolution_request": "Send new data",
        "product_serial": null
      }
    ],
    "missing_product": [
      {
        "exception_item_uuid": "3af38480-4fd4-50a2-bade-1df2d4e88601",
        "file_id": "file-123.xml",
        "product_gtin": "01234567890123",
        "product_serial": "12121212121212",
        "resolution_request": "Credit account"
      }
    ],
    "overages": [
      {
        "exception_item_uuid": "e90ae12e-9fc7-5bf4-b686-657660af9918",
        "gtin": "23456789012345",
        "quantity_ordered": 100,
        "quantity_received": 110,
        "resolution_request": "Send back product"
      }
    ],
    "underages": [
      {
        "exception_item_uuid": "53a7fbda-f1ab-5679-8195-0c057a050434",
        "gtin": "23456789012344",
        "quantity_ordered": 100,
        "quantity_received": 90,
        "resolution_request": "Send product"
      }
    ],
    "master_data_errors": {
      "gln_errors": [
        {
          "exception_item_uuid": "959fe743-ed76-5b28-87ff-c58ac36e5eb2",
          "invalid_gln": "123456789",
          "proposed_gln": "123456780",
          "resolution_request": null
        }
      ],
      "gtin_errors": [
        {
          "exception_item_uuid": "f3febc18-3a11-58c4-99e4-4e6631c864f3",
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
  "message_uuid": "ca5ce291-fad2-5e78-ba45-ee3d310d7d3b",
  "exception_case_uuid": "2dbf3d13-e539-5e86-a43f-3ef49bc08c5d",
  "timestamp": 1711499003,
  "sender_information": {
    "vp": "jwt...",
    "gln": "1234567890124",
    "email": "contact@manufacturer.com",
    "phone": "123-456-7891"
  },
  "po_number": "ABD1234",
  "response_items": [
    {
      "exception_item_uuid": "909df5e2-fb8a-5330-bd1a-dcd6efd658fa",
      "resolution_response": "Accept",
      "comments": "Accepted the missing data issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "3af38480-4fd4-50a2-bade-1df2d4e88601",
      "resolution_response": "Accept",
      "comments": "Shipped product already on it's way, no account credit needed.",
      "alternative_resolution": {
        "alternative_resolution": "Send product",
        "follow_up": "Email",
        "follow_up_details": "Product is already coming"
      }
    },
    {
      "exception_item_uuid": "e90ae12e-9fc7-5bf4-b686-657660af9918",
      "resolution_response": "Accept",
      "comments": "Accepted the overage issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "53a7fbda-f1ab-5679-8195-0c057a050434",
      "resolution_response": "Accept",
      "comments": "Accepted the underage issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "53a7fbda-f1ab-5679-8195-0c057a050434",
      "resolution_response": "Accept",
      "comments": "Accepted the gln issue.",
      "alternative_resolution": null
    },
    {
      "exception_item_uuid": "f3febc18-3a11-58c4-99e4-4e6631c864f3",
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
  "message_uuid": "61c72ff1-8b9b-504f-b460-cbaf4c83020a",
  "exception_case_uuid": "2dbf3d13-e539-5e86-a43f-3ef49bc08c5d",
  "timestamp": 1711502603,
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