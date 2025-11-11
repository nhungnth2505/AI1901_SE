# Giả lập một cơ sở dữ liệu media (hình ảnh, âm nhạc, văn bản)
# Minh họa cho mục 12.5: Mỗi đối tượng media đều có metadata bằng văn bản 
media_database = [
    {
        "id": "img1",
        "type": "image",
        "filename": "sunset_beach.jpg",
        "metadata": {
            "title": "Hoàng hôn tuyệt đẹp",
            "tags": ["biển", "đại dương", "hoàng hôn", "bầu trời", "cam"],
            "caption": "Cảnh hoàng hôn màu cam tuyệt đẹp trên sóng biển."
        }
    },
    {
        "id": "img2",
        "type": "image",
        "filename": "city_night.jpg",
        "metadata": {
            "title": "Thành phố về đêm",
            "tags": ["thành phố", "ánh đèn", "ban đêm", "đô thị", "bầu trời"],
            "caption": "Đường chân trời đô thị với ánh đèn thành phố rực rỡ dưới bầu trời đêm."
        }
    },
    {
        "id": "song1",
        "type": "music",
        "filename": "upbeat_track.mp3",
        "metadata": {
            "title": "Summer Vibes",
            "artist": "DJ Sunny",
            "album": "Beach Party",
            "tags": ["pop", "mùa hè", "vui vẻ", "khiêu vũ"]
        }
    },
    {
        "id": "doc1",
        "type": "text",
        "content": "Truy xuất thông tin (Information Retrieval) là quá trình lấy các tài nguyên...",
        "metadata": {
            "title": "Giới thiệu về IR",
            "author": "Dr. Smith",
            "tags": ["ir", "tìm kiếm", "văn bản", "truy xuất"]
        }
    }
]

def search_metadata(metadata, query):
    """
    Một hàm trợ giúp đơn giản để tìm kiếm query trong metadata.
    Đây là cốt lõi của khái niệm trong mục 12.5.
    """
    query = query.lower()
    for key, value in metadata.items():
        if isinstance(value, str):
            if query in value.lower():
                return True
        elif isinstance(value, list): # Dành cho danh sách tags
            if any(query in tag.lower() for tag in value):
                return True
    return False

def unified_search(database, query, media_type=None):
    """
    Hàm tìm kiếm mô phỏng:
    - 12.5: Tìm kiếm media bằng cách quét metadata văn bản.
    - 12.6: Cho phép lọc theo 'media_type', mô phỏng một dịch vụ tìm kiếm chuyên biệt.
    """
    
    print(f"\n--- Đang tìm kiếm: '{query}' ---")
    if media_type:
        # Mô phỏng khái niệm "One Search Fits All?" 
        print(f"Lọc dịch vụ chuyên biệt: '{media_type}'")
    
    results = []
    for item in database:
        # (12.6) Áp dụng bộ lọc dịch vụ nếu có
        if media_type and item['type'] != media_type:
            continue
            
        # (12.5) Thực hiện tìm kiếm dựa trên văn bản (metadata)
        found_in_metadata = search_metadata(item['metadata'], query)
        
        # Xử lý đặc biệt cho tài liệu văn bản (cũng tìm kiếm nội dung)
        found_in_content = False
        if item['type'] == 'text' and query.lower() in item['content'].lower():
            found_in_content = True
            
        if found_in_metadata or found_in_content:
            results.append(item)
            
    return results

# --- Chạy Demo ---

# Demo 1 (12.5): Tìm kiếm chung cho từ "bầu trời".
# Sẽ trả về 2 hình ảnh vì từ "bầu trời" có trong metadata của chúng 
results_1 = unified_search(media_database, "bầu trời")
for r in results_1:
    print(f"  > Tìm thấy [ID: {r['id']}, Loại: {r['type']}] - Tiêu đề: {r['metadata']['title']}")

# Demo 2 (12.5): Tìm kiếm chung cho từ "pop".
# Sẽ chỉ trả về bài hát 
results_2 = unified_search(media_database, "pop")
for r in results_2:
    print(f"  > Tìm thấy [ID: {r['id']}, Loại: {r['type']}] - Tiêu đề: {r['metadata']['title']}")

# Demo 3 (12.6): Tìm kiếm từ "bầu trời" nhưng CHỈ trong dịch vụ "music" 
# Sẽ không trả về kết quả nào.
results_3 = unified_search(media_database, "bầu trời", media_type="music")
if not results_3:
    print("  > Không tìm thấy kết quả nào.")

# Demo 4 (12.6): Tìm kiếm từ "bầu trời" nhưng CHỈ trong dịch vụ "image" 
# Sẽ trả về 2 hình ảnh.
results_4 = unified_search(media_database, "bầu trời", media_type="image")
for r in results_4:
    print(f"  > Tìm thấy [ID: {r['id']}, Loại: {r['type']}] - Tiêu đề: {r['metadata']['title']}")

# Demo 5 (12.5): Tìm kiếm nội dung văn bản
results_5 = unified_search(media_database, "truy xuất")
for r in results_5:
    print(f"  > Tìm thấy [ID: {r['id']}, Loại: {r['type']}] - Tiêu đề: {r['metadata']['title']}")