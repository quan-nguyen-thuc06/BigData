from elasticsearch import Elasticsearch, helpers
import json

# Kết nối tới Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

# Định nghĩa ánh xạ chỉ mục
mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "brand": {"type": "keyword"},
            "categories": {"type": "keyword"},
            "reviews_text": {"type": "text"},
            "reviews_rating": {"type": "integer"},
            "prices_amountMax": {"type": "float"},
            "review_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            },
            "suggest": {"type": "completion"}
        }
    }
}

# Xóa chỉ mục cũ nếu tồn tại và tạo chỉ mục mới
if es.indices.exists(index="amazon_products"):
    es.indices.delete(index="amazon_products")
es.indices.create(index="amazon_products", body=mapping)

# Đọc dữ liệu đã xử lý
with open('data/processed/amazon_products.json', 'r') as f:
    documents = json.load(f)

# Chuẩn bị dữ liệu cho bulk indexing
actions = [
    {
        "_index": "amazon_products",
        "_source": doc
    }
    for doc in documents
]

# Thực hiện bulk indexing
helpers.bulk(es, actions)

print("Dữ liệu đã được lập chỉ mục vào Elasticsearch")