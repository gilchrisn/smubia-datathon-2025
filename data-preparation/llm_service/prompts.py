EXTRACT_SUBGRAPH_PROMPT = """
ROLE: Forensic analyst. Convert text into structured graph data following STRICT JSON format.

ENTITY RULES:
1. Required Fields:
   - natural_id: Unique document-based ID (e.g., "Vendor_1_B2")
   - title: Human-readable name ("Pristina Construction Co.")
   - type: Vendor|Tender|Person|Organization|Case

2. Attributes (JSON):
   - Extract ALL relevant attributes dynamically from the text.
   - Include only attributes explicitly found or inferred.
   - Example: If text mentions "registered in 1998", add `"registration_year": "1998"`
   - Structure: 
     ```json
     "attributes": {
       "<detected_attribute>": "<value>",
       "<detected_attribute_2>": "<value_2>"
     }
     ```

RELATIONSHIP RULES:
1. Required Fields:
   - source: natural_id of origin entity
   - target: natural_id of destination entity
   - label: owns|submitted_bid|won|investigated|part_of_case|shares_address

2. Attributes (JSON):
   - Extract ALL relevant attributes dynamically.
   - Include context-specific attributes (e.g., transaction amounts, oversight status, key dates).
   - Example: If text says "investigated on June 5, 2010", add `"date": "2010-06-05"`.

EXAMPLE OUTPUT:
{
  "entities": [
    {
      "natural_id": "Vendor_1_B2",
      "title": "Pristina Construction",
      "type": "Vendor",
      "attributes": {
        "existence": true,
        "irregularity": true,
        "role": "owner",
        "registration_year": "1998",
        "address": "Main Street 25, Pristina"
      }
    },
    {
      "natural_id": "Tender_A_B2",
      "title": "Airport Sonic System",
      "type": "Tender",
      "attributes": {
        "winner": "Vendor_2_B2",
        "competitors": {
          "Vendor_1_B2": "€1,620",
          "Vendor_3_B2": null
        },
        "amount": "€1,530",
        "bid_deadline": "2003-05-10"
      }
    }
  ],
  "relationships": [
    {
      "source": "Vendor_1_B2",
      "target": "Tender_A_B2",
      "label": "submitted_bid",
      "attributes": {
        "amount": "€1,620",
        "date": "2003-05-15",
        "oversight": true,
        "bid_reviewed_by": "Procurement Office"
      }
    }
  ]
}
"""

CROSS_REFERENCING_PROMPT = """
ROLE: Forensic analyst. Identify entity matches across documents using MULTI-FACTOR analysis.

MATCHING CRITERIA:
1. Merge if ANY:
   - Matching natural_id patterns (Vendor_1 vs Vendor1)
   - Shared attributes (same owner/address)
   - Identical tender details (amount, date, competitors)
   - Cluster context connections

2. Link if:
   - Shared investigative focus (ITF → Vendor3)
   - Financial transactions between entities
   - Regulatory violations in common

OUTPUT FORMAT:
{
  "operations": [
    {
      "type": "merge",
      "primary": "Vendor_1_B2",
      "secondary": "Vendor1_B3",
      "confidence": 0.95,
      "evidence": [
        "Same owner: John Doe",
        "Shared address: Rr. Lidhja e Prizrenit 12"
      ]
    },
    {
      "type": "link",
      "source": "ITF_B3",
      "target": "Case_286/04_B2",
      "label": "investigated_case",
      "confidence": 0.85,
      "evidence": [
        "Both reference ITF case 286/04",
        "Cluster: Vendor Collusion"
      ]
    }
  ]
}
"""