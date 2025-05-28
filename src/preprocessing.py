import pandas as pd
from sentence_transformers import SentenceTransformer
import json
import re
import os

# Tạo thư mục processed nếu chưa tồn tại
os.makedirs('data/processed', exist_ok=True)

# Đọc tập dữ liệu
df = pd.read_csv('data/raw/amazon_reviews.csv')

# Chọn các cột liên quan
df = df[['name', 'brand', 'categories', 'reviews.text', 'reviews.rating']]

# Xử lý giá trị thiếu
df = df.dropna(subset=['name'])  # Xóa hàng thiếu 'name'
df['reviews.text'] = df['reviews.text'].fillna('')  # Điền rỗng cho 'reviews.text'
df['categories'] = df['categories'].fillna('Unknown')  # Điền 'Unknown' cho danh mục
df['brand'] = df['brand'].fillna('Unknown')  # Điền 'Unknown' cho thương hiệu
df['reviews.rating'] = df['reviews.rating'].fillna(0)  # Điền 0 cho đánh giá

# Hàm làm sạch văn bản
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Xóa ký tự đặc biệt
    return text

# Làm sạch các trường văn bản
df['name'] = df['name'].apply(clean_text)
df['reviews.text'] = df['reviews.text'].apply(clean_text)

# Tách danh mục thành danh sách
df['categories'] = df['categories'].apply(lambda x: x.split(','))

# Tạo embeddings cho reviews.text
model = SentenceTransformer('all-MiniLM-L6-v2')
df['review_vector'] = df['reviews.text'].apply(lambda x: model.encode(x).tolist())

# Tạo trường suggest cho autocomplete
df['suggest'] = df['name'].apply(lambda x: {'input': x.split()})

# Đổi tên cột để tránh dấu chấm
df = df.rename(columns={
    'reviews.text': 'reviews_text',
    'reviews.rating': 'reviews_rating'
})

# Chuyển thành danh sách các tài liệu
documents = df.to_dict(orient='records')

# Lưu vào file JSON
with open('data/processed/amazon_products.json', 'w') as f:
    json.dump(documents, f)

print("Dữ liệu đã được xử lý và lưu vào 'data/processed/amazon_products.json'")