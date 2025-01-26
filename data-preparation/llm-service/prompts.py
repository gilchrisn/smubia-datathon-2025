EXTRACT_SUBGRAPH_PROMPT = """
Role: You are a forensic analyst. Parse the text below into a directed graph of entities and relationships.

Rules:
1. **Nodes**:
   - Types: Vendor, Person, Tender, Official, Transaction, Law.
   - Attributes: Add `irregularity=True` if involved in fraud (e.g., fake bids, undocumented cash).
   - Assign unique IDs (e.g., "Vendor_1", "John_Doe").

2. **Edges**:
   - Directed relationships with labels like "submitted_bid", "owns", "approved_by".
   - Attributes: Include amounts (€), dates, or regulatory violations.

3. **Output**: JSON with `{"nodes": [...], "edges": [...]}`. No explanations.

Examples:

Text: "Vendor_1 (owned by John Doe) won Tender_A despite fake bids from Vendor_3."
Output:
{
  "nodes": [
    {"id": "Vendor_1", "type": "Vendor", "attributes": {"irregularity": true}},
    {"id": "John_Doe", "type": "Person", "attributes": {"role": "owner"}},
    {"id": "Tender_A", "type": "Tender"}
  ],
  "edges": [
    {"source": "John_Doe", "target": "Vendor_1", "label": "owns"},
    {"source": "Vendor_1", "target": "Tender_A", "label": "won"},
    {"source": "Vendor_3", "target": "Tender_A", "label": "submitted_fake_bid"}
  ]
}

Now parse this text:
"""

CROSS_REFERENCING_PROMPT = """
Role: You are a forensic graph analyst. Determine if nodes from two documents refer to the same entity or have a meaningful relationship.

Rules:
1. **Merge**: Same entity but different IDs (e.g., "Vendor_1" vs "Vendor1").
2. **Link**: Related entities (e.g., "Official_A (PDF1) approved Tender_X (PDF2)").
3. **Output**: JSON list of actions with evidence.

Format:
[
  {
    "type": "merge" | "link",
    "node1": "id_from_pdf1",
    "node2": "id_from_pdf2",
    "confidence": 0.0-1.0,
    "evidence": "Brief reason (e.g., same owner, shared tender ID)"
  }
]

Examples:

Nodes from PDF1: [{"id": "Vendor_1", "type": "Vendor", "attributes": {"owner": "John_Doe"}}]
Nodes from PDF2: [{"id": "Vendor1", "type": "Vendor", "attributes": {"owner": "John_Doe"}}]
Output:
[
  {
    "type": "merge",
    "node1": "Vendor_1",
    "node2": "Vendor1",
    "confidence": 0.95,
    "evidence": "Same owner (John_Doe)"
  }
]

Nodes from PDF1: [{"id": "Official_A", "type": "Official"}]
Nodes from PDF2: [{"id": "Tender_X", "type": "Tender"}]
Output:
[
  {
    "type": "link",
    "node1": "Official_A",
    "node2": "Tender_X",
    "confidence": 0.8,
    "evidence": "News reports state Official_A approved Tender_X"
  }
]

Now analyze:
Nodes from PDF1: {nodes_pdf1}
Nodes from PDF2: {nodes_pdf2}
"""