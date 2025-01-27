from database import Database

def test_crud():
    try:
        db = Database()
        print("\n=== Testing Database Operations ===\n")

        # Test Document CRUD
        print("=== Document Operations ===")
        doc = db.create_document('test.pdf', 'pdf', 'initial content')
        print("Created document:", doc.data)
        
        doc_get = db.get_document('test.pdf')
        print("Retrieved document:", doc_get.data)
        
        doc_update = db.update_document('test.pdf', {'raw_content': 'updated content'})
        print("Updated document:", doc_update.data)
        
        # Test Cluster CRUD
        print("\n=== Cluster Operations ===")
        cluster = db.create_cluster('Test Cluster', 'Test Description')
        print("Created cluster:", cluster.data)
        
        cluster_get = db.get_cluster(cluster.data[0]['cluster_id'])
        print("Retrieved cluster:", cluster_get.data)
        
        cluster_update = db.update_cluster(cluster.data[0]['cluster_id'], {'description': 'Updated Description'})
        print("Updated cluster:", cluster_update.data)

        # Test Entity CRUD
        print("\n=== Entity Operations ===")
        entity = db.create_entity('test_entity', 'person', {'name': 'Test Person'}, ['test.pdf'])
        print("Created entity:", entity.data)
        
        entity_get = db.get_entity('test_entity')
        print("Retrieved entity:", entity_get.data)
        
        entity_update = db.update_entity('test_entity', {'attributes': {'name': 'Updated Person'}})
        print("Updated entity:", entity_update.data)
        
        # Test Entity Search
        entities_by_type = db.search_entities_by_type('person')
        print("Entities by type 'person':", entities_by_type.data)

        # Test Relationship CRUD
        print("\n=== Relationship Operations ===")
        # Create second entity for relationship
        entity2 = db.create_entity('test_entity2', 'person', {'name': 'Test Person 2'}, ['test.pdf'])
        
        rel = db.create_relationship('test_entity', 'test_entity2', 'knows', {'since': '2023'}, ['test.pdf'])
        print("Created relationship:", rel.data)
        
        rel_get = db.get_relationship(rel.data[0]['relationship_id'])
        print("Retrieved relationship:", rel_get.data)
        
        rel_update = db.update_relationship(rel.data[0]['relationship_id'], {'attributes': {'since': '2024'}})
        print("Updated relationship:", rel_update.data)
        
        # Test relationships by label
        rels_by_label = db.get_relationships_by_label('knows')
        print("Relationships with label 'knows':", rels_by_label.data)

        # Test Entity-Cluster Mapping
        print("\n=== Entity-Cluster Mapping Operations ===")
        mapping = db.map_entity_to_cluster('test_entity', cluster.data[0]['cluster_id'])
        print("Created entity-cluster mapping:", mapping.data)

        # Cleanup (Delete operations)
        print("\n=== Cleanup Operations ===")
        
        # 1. First delete entity-cluster mappings
        db.delete_entity_cluster_mapping('test_entity', cluster.data[0]['cluster_id'])
        print("Deleted entity-cluster mapping")
        
        # 2. Then delete relationships
        db.delete_relationship(rel.data[0]['relationship_id'])
        print("Deleted relationship")
        
        # 3. Then delete entities
        db.delete_entity('test_entity2')
        db.delete_entity('test_entity')
        print("Deleted entities")
        
        # 4. Then delete cluster
        db.delete_cluster(cluster.data[0]['cluster_id'])
        print("Deleted cluster")
        
        # 5. Finally delete document
        db.delete_document('test.pdf')
        print("Deleted document")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_crud()