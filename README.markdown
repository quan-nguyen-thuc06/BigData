# Hệ thống Tìm kiếm Sản phẩm Thông minh

Dự án này triển khai một hệ thống tìm kiếm sản phẩm thông minh sử dụng Elasticsearch với các tính năng như tìm kiếm cơ bản, tìm kiếm mờ, gợi ý tự động, tìm kiếm có bộ lọc, và tìm kiếm ngữ nghĩa.

## Yêu cầu
- Python 3.8+
- Elasticsearch 8.x chạy trên `localhost:9200`
- Tập dữ liệu: "Consumer Reviews of Amazon Products" từ Kaggle

## Cài đặt
1. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Khởi động Elasticsearch:**
   - Tải và chạy Elasticsearch theo hướng dẫn tại [elasticsearch.co](https://www.elastic.co/downloads/elasticsearch).
   - Đảm bảo Elasticsearch chạy trên `http://localhost:9200`.

## Sử dụng
1. **Tiền xử lý dữ liệu:**
   - Đặt file `amazon_reviews.csv` vào thư mục `data/raw/`.
   - Chạy:
     ```bash
     python src/preprocessing.py
     ```
   - Kết quả được lưu tại `data/processed/amazon_products.json`.

2. **Lập chỉ mục dữ liệu:**
   - Chạy:
     ```bash
     python src/indexing.py
     ```

3. **Chạy API:**
   - Chạy:
     ```bash
     uvicorn src.api:app --reload
     ```
   - API sẽ chạy tại `http://localhost:8000`.

4. **Thử nghiệm các điểm cuối API:**
   - Tìm kiếm cơ bản: `GET /search?query=phone`
   - Tìm kiếm mờ: `GET /fuzzy-search?query=phon`
   - Gợi ý tự động: `GET /suggest?prefix=pho`
   - Tìm kiếm có bộ lọc: `GET /filtered-search?query=phone&price_max=500&rating_min=4&category=Electronics`
   - Tìm kiếm ngữ nghĩa: `GET /semantic-search?query=good quality phone`

5. **Đánh giá hiệu suất:**
   - Mở `notebooks/evaluation.ipynb` trong Jupyter Notebook để chạy các truy vấn thử nghiệm và tính toán các chỉ số (precision, recall, F1-score, độ trễ).

## Ghi chú
- Đảm bảo điều chỉnh tên cột trong `preprocessing.py` nếu tập dữ liệu có cấu trúc khác.
- Tìm kiếm ngữ nghĩa sử dụng mô hình `all-MiniLM-L6-v2` để tạo vector nhúng.