import numpy as np

def run_hits_demo():
    """
    Thực hiện demo thuật toán HITS dựa trên đồ thị tại 
    và mô phỏng các bước lặp tại .
    """
    
    # 1. ĐỊNH NGHĨA ĐỒ THỊ (GRAPH)
    # Chúng ta có 7 nút (nodes), được đánh số từ 1 đến 7.
    # Ta sẽ dùng 0-indexing (0-6) để biểu diễn trong mảng.
    # A[i][j] = 1 nếu có liên kết từ nút (i+1) đến nút (j+1).
    
    # Dựa trên đồ thị :
    # 3 -> 1, 3 -> 5, 3 -> 6
    # 5 -> 1
    # 2 -> 6
    # 4 -> 6
    # Nút 1, 6, 7 không trỏ đi đâu cả.
    
    # Adjacency Matrix (Ma trận kề) L:
    #    1  2  3  4  5  6  7  (Tới)
    L = np.array([
        [0, 0, 0, 0, 0, 0, 0], # 1 (Từ)
        [0, 0, 0, 0, 0, 1, 0], # 2
        [1, 0, 0, 0, 1, 1, 0], # 3
        [0, 0, 0, 0, 0, 1, 0], # 4
        [1, 0, 0, 0, 0, 0, 0], # 5
        [0, 0, 0, 0, 0, 0, 0], # 6
        [0, 0, 0, 0, 0, 0, 0]  # 7
    ], dtype=float)
    
    # Ma trận chuyển vị (Transpose) L.T
    # L_T[i][j] = 1 nếu có liên kết từ (j+1) đến (i+1)
    # Đây là ma trận thể hiện các liên kết "đi vào" (in-links)
    L_T = L.T

    # 2. KHỞI TẠO ĐIỂM SỐ
    # Slide bắt đầu với (1, 1) cho mỗi nút.
    # auth: Điểm Authority
    # hub: Điểm Hub
    num_nodes = 7
    auth = np.full(num_nodes, 1.0)
    hub = np.full(num_nodes, 1.0)
    
    # Số vòng lặp như trong slide
    iterations = 3
    
    print(f"--- BẮT ĐẦU THUẬT TOÁN HITS (Mô phỏng ) ---")
    print(f"Đồ thị L (từ ):\n{L}\n")
    
    # 3. THỰC HIỆN CÁC VÒNG LẶP
    for i in range(iterations):
        print(f"============= VÒNG LẶP {i + 1} =============")
        
        # In điểm số đầu vào của vòng lặp
        # (Đây là điểm đã chuẩn hóa từ vòng trước, hoặc điểm khởi tạo)
        if i == 0:
            print(f"Input (Auth, Hub) :")
            for n in range(num_nodes):
                print(f"  Node {n+1}: ({auth[n]:.2f}, {hub[n]:.2f})")
        else:
            # In điểm đã chuẩn hóa từ bước trước
            print(f"Input (Auth, Hub) :")
            for n in range(num_nodes):
                print(f"  Node {n+1}: ({auth[n]:.2f}, {hub[n]:.2f})")
                
        
        # a. Cập nhật điểm Authority
        # Điểm Authority mới = tổng các điểm Hub của các nút trỏ đến nó
        # auth_new = L.T @ hub
        auth_new = L_T.dot(hub)
        
        # b. Cập nhật điểm Hub
        # Điểm Hub mới = tổng các điểm Authority của các nút mà nó trỏ đến
        # hub_new = L @ auth
        # (LƯU Ý: HITS chuẩn dùng auth_new, nhưng slide 
        # cho thấy cả hai cập nhật đều dựa trên điểm (auth, hub) CŨ từ đầu vòng lặp)
        hub_new = L.dot(auth)
        
        print("\nUpdate Scores (Chưa chuẩn hóa) :")
        for n in range(num_nodes):
            print(f"  Node {n+1}: ({auth_new[n]:.2f}, {hub_new[n]:.2f})")

        # c. Chuẩn hóa điểm số (Normalize Scores)
        # Chia mỗi điểm cho tổng L1 (tổng của tất cả các điểm)
        # để giữ cho điểm số không tăng vô hạn
        sum_auth = np.sum(auth_new)
        sum_hub = np.sum(hub_new)
        
        if sum_auth > 0:
            auth = auth_new / sum_auth
        else:
            auth = auth_new # Giữ nguyên nếu tổng là 0
            
        if sum_hub > 0:
            hub = hub_new / sum_hub
        else:
            hub = hub_new # Giữ nguyên nếu tổng là 0

        print("\nNormalize Scores :")
        for n in range(num_nodes):
            print(f"  Node {n+1}: ({auth[n]:.2f}, {hub[n]:.2f})")
        print("-" * 20)

    # 4. IN KẾT QUẢ CUỐI CÙNG
    print("\n========= KẾT QUẢ CUỐI CÙNG (Sau 3 vòng lặp) =========")
    print("Điểm Authority (Chuyên gia) cuối cùng:")
    for n in range(num_nodes):
        print(f"  Node {n+1}: {auth[n]:.3f}")

    print("\nĐiểm Hub (Điều phối) cuối cùng:")
    for n in range(num_nodes):
        print(f"  Node {n+1}: {hub[n]:.3f}")

# Chạy demo
if __name__ == "__main__":
    run_hits_demo()