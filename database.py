from supabase import create_client
from typing import Dict, List, Optional, Union
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
    def __init__(self):
        self.client = supabase

    # Document Operations
    def create_document(self, doc_id: str, doc_type: str, raw_content: str, cluster_id: Optional[int] = None):
        return self.client.table('documents').insert({
            'doc_id': doc_id,
            'doc_type': doc_type,
            'raw_content': raw_content,
            'cluster_id': cluster_id
        }).execute()

    def get_document(self, doc_id: str):
        return  self.client.table('documents').select('*').eq('doc_id', doc_id).execute()

    def update_document(self, doc_id: str, updates: dict):
        return self.client.table('documents').update(updates).eq('doc_id', doc_id).execute()

    def delete_document(self, doc_id: str):
        return self.client.table('documents').delete().eq('doc_id', doc_id).execute()

    # Cluster Operations
    def create_cluster(self, name: str, description: str):
        return self.client.table('clusters').insert({
            'cluster_name': name,
            'description': description
        }).execute()

    def get_cluster(self, cluster_id: int):
        return self.client.table('clusters').select('*').eq('cluster_id', cluster_id).execute()

    def update_cluster(self, cluster_id: int, updates: dict):
        return self.client.table('clusters').update(updates).eq('cluster_id', cluster_id).execute()

    def delete_cluster(self, cluster_id: int):
        return self.client.table('clusters').delete().eq('cluster_id', cluster_id).execute()
    
    # Entity Operations
    def create_entity(self, entity_id: str, entity_type: str, attributes: Dict, sources: List[str]):
        return self.client.table('entities').insert({
            'entity_id': entity_id,
            'entity_type': entity_type,
            'attributes': attributes,
            'sources': sources
        }).execute()
    
    def get_entity(self, entity_id: int):
        return self.client.table('entities').select('*').eq('entity_id', entity_id).execute()
    
    def update_entity(self, entity_id: str, updates: dict):
        return self.client.table('entities').update(updates).eq('entity_id', entity_id).execute()

    def delete_entity(self, entity_id: str):
        return self.client.table('entities').delete().eq('entity_id', entity_id).execute()
    
    # Relationship Operations
    def create_relationship(self, source_id: str, target_id: str, label: str, 
                             attributes: Optional[Dict] = None, sources: Optional[List[str]] = None):
        return  self.client.table('relationships').insert({
            'source_id': source_id,
            'target_id': target_id,
            'label': label,
            'attributes': attributes or {},
            'sources': sources or []
        }).execute()
    
    def get_relationship(self, relationship_id: int):
        return self.client.table('relationships').select('*').eq('relationship_id', relationship_id).execute()
    
    def update_relationship(self, relationship_id: int, updates: dict):
        return self.client.table('relationships').update(updates).eq('relationship_id', relationship_id).execute()
    
    def delete_relationship(self, relationship_id: int):
        return self.client.table('relationships').delete().eq('relationship_id', relationship_id).execute()

    # Entity-Cluster Mapping Operations
    def map_entity_to_cluster(self, entity_id: str, cluster_id: int):
        return self.client.table('entity_clusters').insert({
            'entity_id': entity_id,
            'cluster_id': cluster_id
        }).execute()
    
    def delete_entity_cluster_mapping(self, entity_id: str, cluster_id: int):
        return self.client.table('entity_clusters').delete()\
            .eq('entity_id', entity_id)\
            .eq('cluster_id', cluster_id)\
            .execute()

    # Helper Methods
    def search_entities_by_type(self, entity_type: str):
        return  self.client.table('entities').select('*').eq('entity_type', entity_type).execute()

    def get_relationships_by_label(self, label: str):
        return self.client.table('relationships').select('*').eq('label', label).execute()

def main():
    db = Database()
    print(db.client)
    

if __name__ == "__main__":
    main()