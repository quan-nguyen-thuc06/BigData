from fastapi import FastAPI
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

# Khởi tạo ứng dụng FastAPI, Elasticsearch và mô hình Sentence-BERT
app = FastAPI()
es = Elasticsearch(['http://localhost:9200'])
model = SentenceTransformer('all-MiniLM-L6-v2')

# Tìm kiếm cơ bản
@app.get("/search")
def basic_search(query: str):
    body = {
        "query": {
            "match": {
                "name": query
            }
        }
    }
    res = es.search(index="amazon_products", body=body)
    return {"results": [hit["_source"] for hit in res["hits"]["hits"]]}

# Tìm kiếm mờ (fuzzy search)
@app.get("/fuzzy-search")
def fuzzy_search(query: str):
    body = {
        "query": {
            "match": {
                "name": {
                    "query": query,
                    "fuzziness": "AUTO"
                }
            }
        }
    }
    res = es.search(index="amazon_products", body=body)
    return {"results": [hit["_source"] for hit in res["hits"]["hits"]]}

# Gợi ý tự động (autocomplete)
@app.get("/suggest")
def autocomplete(prefix: str):
    body = {
        "suggest": {
            "product-suggest": {
                "prefix": prefix,
                "completion": {
                    "field": "suggest"
                }
            }
        }
    }
    res = es.search(index="amazon_products", body=body)
    suggestions = [opt["text"] for opt in res["suggest"]["product-suggest"][0]["options"]]
    return {"suggestions": suggestions}

# Tìm kiếm có bộ lọc (filtered search)
@app.get("/filtered-search")
def filtered_search(query: str, price_max: float = None, rating_min: int = None, category: str = None):
    body = {
        "query": {
            "bool": {
                "must": [{"match": {"name": query}}],
                "filter": []
            }
        }
    }
    if price_max:
        body["query"]["bool"]["filter"].append({"range": {"prices_amountMax": {"lte": price_max}}})
    if rating_min:
        body["query"]["bool"]["filter"].append({"range": {"reviews_rating": {"gte": rating_min}}})
    if category:
        body["query"]["bool"]["filter"].append({"term": {"categories": category}})
    res = es.search(index="amazon_products", body=body)
    return {"results": [hit["_source"] for hit in res["hits"]["hits"]]}

# Tìm kiếm ngữ nghĩa (semantic search)
@app.get("/semantic-search")
def semantic_search(query: str):
    query_vector = model.encode(query).tolist()
    body = {
        "knn": {
            "field": "review_vector",
            "query_vector": query_vector,
            "k": 10,
            "num_candidates": 100
        }
    }
    res = es.search(index="amazon_products", body=body)
    return {"results": [hit["_source"] for hit in res["hits"]["hits"]]}