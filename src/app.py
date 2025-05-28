import streamlit as st
import requests

# Địa chỉ API (giả định)
API_URL = "http://localhost:8000"

# Hàm lấy gợi ý tự động
def get_suggestions(prefix):
    try:
        response = requests.get(f"{API_URL}/suggest", params={"prefix": prefix}, timeout=2)
        if response.status_code == 200:
            return response.json().get("suggestions", [])
    except:
        return []
    return []

# Hàm tìm kiếm thông minh
def smart_search(query):
    try:
        # Logic đơn giản: dựa trên độ dài truy vấn để chọn phương pháp
        if len(query.split()) > 2:  # Truy vấn dài -> semantic search
            response = requests.get(f"{API_URL}/semantic-search", params={"query": query}, timeout=2)
        else:  # Truy vấn ngắn -> basic hoặc fuzzy
            response = requests.get(f"{API_URL}/search", params={"query": query}, timeout=2)
        if response.status_code == 200:
            return response.json().get("results", [])
    except:
        return []
    return []

# Giao diện Streamlit
st.title("Tìm kiếm Sản phẩm Thông minh")

# Thanh tìm kiếm với gợi ý tự động
query = st.text_input("Nhập từ khóa tìm kiếm:", key="search_input")

# Hiển thị gợi ý tự động khi người dùng nhập
if query:
    suggestions = get_suggestions(query)
    if suggestions:
        selected = st.selectbox("Chọn gợi ý (hoặc tiếp tục nhập):", [""] + suggestions, index=0)
        if selected:  # Nếu người dùng chọn gợi ý
            query = selected

# Tự động tìm kiếm và hiển thị kết quả khi có truy vấn
if query:
    results = smart_search(query)
    if results:
        st.write(f"**Kết quả tìm kiếm ({len(results)} sản phẩm):**")
        for product in results:
            st.write(f"**{product.get('name', 'Tên sản phẩm')}**")
            st.write(f"Giá: {product.get('prices_amountMax', 0):.2f} USD")
            st.write(f"Mô tả: {product.get('reviews_text', 'Không có mô tả')[:100]}...")
            st.write("---")
    else:
        st.write("Không tìm thấy sản phẩm nào khớp với truy vấn.")
else:
    st.write("Vui lòng nhập từ khóa để bắt đầu tìm kiếm.")