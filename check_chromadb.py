import chromadb
from chromadb.utils import embedding_functions

# Đường dẫn đến thư mục chứa database
db_path = "./chroma_db"

# Kết nối đến ChromaDB
chroma_client = chromadb.PersistentClient(path=db_path)

# Lấy danh sách các collection trong database
collections = chroma_client.list_collections()

# Hiển thị thông tin các collection
print("Danh sách collections:")
for collection in collections:
    print(f"- Name: {collection.name}, Metadata: {collection.metadata}")

# Chọn một collection (thay "product_knowledge_base" bằng tên collection của bạn)
collection = chroma_client.get_collection(name="product_knowledge_base")

# Lấy toàn bộ dữ liệu từ collection
results = collection.get()

# Hiển thị các tài liệu
print("\nNội dung collection:")
for doc_id, doc, meta in zip(results['ids'], results['documents'], results['metadatas']):
    print(f"- ID: {doc_id}")
    print(f"  Document: {doc}")
    print(f"  Metadata: {meta}")
    print()
