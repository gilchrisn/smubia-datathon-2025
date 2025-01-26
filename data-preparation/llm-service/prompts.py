EXTRACT_SUBGRAPH_PROMPT = """
ROLE: Forensic analyst. Convert text into structured graph data.

INSTRUCTIONS:
1. ENTITIES:
   - Types: Vendor|Tender|Person|Organization|Case
   - Attributes:
     * existence: BOOLEAN (true/false)
     * role: owner/representative/investigator
     * For vendors: irregularity=true if collusion suspected
     * For tenders: winner, competitors[], amount=€X
     * note: Key context (e.g., "supermarket in Prizren")

2. RELATIONSHIPS:
   - Labels: owns|submitted_bid|won|investigated|part_of_case|shares_address
   - Attributes: amount=€X, date=YYYY-MM-DD when available

3. OUTPUT: Strict JSON format. No markdown.

EXAMPLE INPUT:
"Vendor3 is a supermarket in Prizren. ITF investigation found no evidence of Vendor4."

EXAMPLE OUTPUT:
{
  "entities": [
    {
      "id": "Vendor3", 
      "type": "Vendor",
      "attributes": {"existence": true, "note": "supermarket in Prizren"}
    },
    {
      "id": "Vendor4", 
      "type": "Vendor",
      "attributes": {"existence": false}
    },
    {
      "id": "ITF", 
      "type": "Organization",
      "attributes": {"role": "investigator"}
    }
  ],
  "relationships": [
    {
      "source": "ITF", 
      "target": "Vendor4", 
      "label": "investigated"
    }
  ]
}

TEXT TO PARSE:
"""

CROSS_REFERENCING_PROMPT = """
ROLE: Forensic graph analyst. Find entity matches across documents.

RULES:
1. MERGE if:
   - Same entity (e.g., "Vendor_1" vs "Vendor1")
   - Shared owner/address (e.g., "Vendor1 & 2 Rep")
   - Same case reference (Case_286/04)

2. LINK if:
   - Same tender across documents
   - Investigative connections (ITF → Vendor3)
   - Shared cluster context

OUTPUT FORMAT:
{
  "operations": [
    {
      "type": "merge"|"link",
      "entity1": "original_id",
      "entity2": "new_id",
      "confidence": 0.9,
      "evidence": "Shared owner (John Doe)"
    }
  ]
}

EXAMPLE OUTPUT:
{
  "operations": [
    {
      "type": "merge",
      "entity1": "Vendor_1_B2",
      "entity2": "Vendor1_B3",
      "confidence": 0.95,
      "evidence": "Same address in Pristina, shared owner"
    }
  ]
}
"""