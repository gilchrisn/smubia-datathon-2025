from supabase import create_client
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class Database:
    """
    Database class to interact with the defined schema via Supabase.
    Includes operations for documents, clusters, entities, relationships, and mappings.
    """

    def __init__(self):
        self.client = supabase

    # --- Document Operations ---

    def create_document(self, doc_id: str, doc_type: str, raw_content: str, cluster_id: Optional[int] = None):
        """Inserts a new document into the `documents` table."""
        return self.client.table('documents').insert({
            'doc_id': doc_id,
            'doc_type': doc_type,
            'raw_content': raw_content,
            'cluster_id': cluster_id
        }).execute()

    def get_all_documents(self):
        """Fetches all documents."""
        return self.client.table('documents').select('*').execute()
    
    def get_all_pdf_documents(self):    
        """Fetches all documents of type 'pdf'."""
        return self.client.table('documents').select('*').eq('doc_type', 'pdf').execute()
    
    def get_all_news_documents(self):
        """Fetches all documents of type 'news'."""
        return self.client.table('documents').select('*').eq('doc_type', 'news').execute()
    
    def get_document(self, doc_id: str):
        """Fetches a document by its unique ID."""
        return self.client.table('documents').select('*').eq('doc_id', doc_id).execute()

    def update_document(self, doc_id: str, updates: dict):
        """Updates a document with new values."""
        return self.client.table('documents').update(updates).eq('doc_id', doc_id).execute()

    def delete_document(self, doc_id: str):
        """Deletes a document by its unique ID."""
        return self.client.table('documents').delete().eq('doc_id', doc_id).execute()

    # --- Cluster Operations ---

    def create_cluster(self, name: str, description: str):
        """Inserts a new concept cluster."""
        return self.client.table('clusters').insert({
            'cluster_name': name,
            'description': description
        }).execute()

    def get_cluster(self, cluster_id: int):
        """Fetches a cluster by its unique ID."""
        return self.client.table('clusters').select('*').eq('cluster_id', cluster_id).execute()

    def update_cluster(self, cluster_id: int, updates: dict):
        """Updates a cluster with new values."""
        return self.client.table('clusters').update(updates).eq('cluster_id', cluster_id).execute()

    def delete_cluster(self, cluster_id: int):
        """Deletes a cluster by its unique ID."""
        return self.client.table('clusters').delete().eq('cluster_id', cluster_id).execute()

    # --- Entity Operations ---

    def create_entity(self, natural_id: str, title: str, entity_type: str, 
                 attributes: Dict, sources: List[str]):
        """Inserts a new entity with natural ID and title"""
        return self.client.table('entities').insert({
            'natural_id': natural_id,
            'title': title,
            'entity_type': entity_type,
            'attributes': attributes,
            'sources': sources
        }).execute()

    # --- Relationship Operations ---

    def create_relationship(self, source_id: str, target_id: str, 
                        label: str, attributes: Optional[Dict] = None, 
                        sources: Optional[List[str]] = None):
        """Helper to create relationship using natural IDs"""
        
        return self.client.table('relationships').insert({
            'source_id': source_id,
            'target_id': target_id,
            'label': label,
            'attributes': attributes or {},
            'sources': sources or []
        }).execute()

    # --- Entity-Cluster Mapping Operations ---

    def map_entity_to_cluster(self, entity_id: str, cluster_id: int):
        """Maps an entity to a cluster."""
        return self.client.table('entity_clusters').insert({
            'entity_id': entity_id,
            'cluster_id': cluster_id
        }).execute()

    def delete_entity_cluster_mapping(self, entity_id: str, cluster_id: int):
        """Deletes a mapping between an entity and a cluster."""
        return self.client.table('entity_clusters').delete()\
            .eq('entity_id', entity_id)\
            .eq('cluster_id', cluster_id)\
            .execute()

    # --- Helper Methods ---

    def search_entities_by_type(self, entity_type: str):
        """Fetches all entities of a given type."""
        return self.client.table('entities').select('*').eq('entity_type', entity_type).execute()

    def get_relationships_by_label(self, label: str):
        """Fetches all relationships with a given label."""
        return self.client.table('relationships').select('*').eq('label', label).execute()

# Main Execution for Testing
if __name__ == "__main__":
    db = Database()
    print("Database client initialized:", db.client)