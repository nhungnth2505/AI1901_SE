from collections import defaultdict, Counter
import time
# --- PHẦN 1: DỮ LIỆU GỐC VÀ XÂY DỰNG CHỈ MỤC ---

# Dữ liệu văn bản gốc
documents = {
    1: "Tropical tropical salt water.",
    2: "A tropical island with tropical water.",
    3: "A tropical fruit.",
    4: "The salt water is calm."
}

# Hàm xây dựng chỉ mục (đã định nghĩa ở trên)
def build_inverted_index(documents):
    inverted_index = defaultdict(list)
    for doc_id, text in documents.items():
        tokens = text.lower().replace('.', '').split()
        word_counts = Counter(tokens)
        for word, count in word_counts.items():
            inverted_index[word].append((doc_id, count))
    for word in inverted_index:
        inverted_index[word].sort()
    return dict(inverted_index)

# Tự động tạo chỉ mục thay vì gán cứng
my_inverted_index = build_inverted_index(documents)


# --- PHẦN 2: THỰC THI TRUY VẤN ---

# Câu truy vấn và danh sách tài liệu vẫn như cũ
query = ['salt', 'water', 'tropical']
all_doc_ids = [1, 2, 3, 4]

print("--- Dữ liệu đầu vào cho việc truy vấn ---")
print("Văn bản gốc:")
print(documents)
print("\nChỉ mục ngược được tạo ra:")
for key, value in my_inverted_index.items():
    print(f'{key}: {value}')
print("\nCâu truy vấn:", query)
print("-" * 50)


def document_at_a_time_evaluation(query, index, doc_ids):
    """
    Thực hiện đánh giá theo phương pháp Document-at-a-time.
    Lặp qua từng tài liệu và tính tổng điểm cho nó.
    """
    # Dictionary để lưu điểm cuối cùng của mỗi tài liệu
    final_scores = {}

    print("\n--- Bắt đầu Document-at-a-time ---")
    
    # Vòng lặp ngoài: lặp qua tất cả các tài liệu có thể có
    for doc_id in doc_ids:
        # Khởi tạo điểm cho tài liệu hiện tại
        current_doc_score = 0
        print(f"\n>> Đang xử lý Tài liệu ID: {doc_id}")

        # Vòng lặp trong: lặp qua tất cả các thuật ngữ trong câu truy vấn
        for term in query:
            # Lấy danh sách postings cho thuật ngữ
            postings = index.get(term, [])
            
            # Kiểm tra xem tài liệu hiện tại có chứa thuật ngữ này không
            for post_doc_id, count in postings:
                if post_doc_id == doc_id:
                    # Nếu có, cộng dồn điểm (ở đây ta dùng word_count làm điểm)
                    current_doc_score += count
                    print(f"   - Tìm thấy '{term}' trong tài liệu {doc_id}. Cộng điểm: {count}. Điểm tạm thời: {current_doc_score}")
                    break # Chuyển sang thuật ngữ tiếp theo cho tài liệu này

        # Chỉ lưu điểm nếu tài liệu có chứa ít nhất một thuật ngữ trong truy vấn
        if current_doc_score > 0:
            final_scores[doc_id] = current_doc_score
            print(f">> Điểm cuối cùng cho Tài liệu {doc_id} là: {current_doc_score}")
            
    return final_scores




def term_at_a_time_evaluation(query, index):
    """
    Thực hiện đánh giá theo phương pháp Term-at-a-time.
    Lặp qua từng thuật ngữ và cập nhật điểm cho các tài liệu liên quan.
    """
    # Dùng defaultdict để tự động khởi tạo điểm bằng 0 cho tài liệu mới
    # Đây chính là các 'accumulators' (bộ tích lũy) trong slide
    accumulators = defaultdict(int)

    print("\n--- Bắt đầu Term-at-a-time ---")

    # Vòng lặp ngoài: lặp qua tất cả các thuật ngữ trong câu truy vấn
    for term in query:
        print(f"\n>> Đang xử lý Thuật ngữ: '{term}'")
        
        # Lấy danh sách postings cho thuật ngữ
        postings = index.get(term, [])
        
        # Vòng lặp trong: lặp qua các tài liệu chứa thuật ngữ này
        for doc_id, count in postings:
            # Lấy điểm cũ
            old_score = accumulators[doc_id]
            
            # Cập nhật điểm cho tài liệu tương ứng
            accumulators[doc_id] += count
            
            print(f"   - Cập nhật tài liệu {doc_id}: điểm cũ {old_score} + {count} = {accumulators[doc_id]}")

    return dict(accumulators) # Chuyển về dict thường để hiển thị đẹp hơn

# Chạy và xem kết quả
start = time.time()
doc_scores = document_at_a_time_evaluation(query, my_inverted_index, all_doc_ids)
print(f"Thời gian thực thi: {time.time() - start:.10f}")
print("\n--- Kết quả Document-at-a-time ---")
print("Điểm số cuối cùng:", doc_scores)

start = time.time()
term_scores = term_at_a_time_evaluation(query, my_inverted_index)
print(f"Thời gian thực thi: {time.time() - start:.10f}")
print("\n--- Kết quả Term-at-a-time ---")
print("Điểm số cuối cùng:", term_scores)