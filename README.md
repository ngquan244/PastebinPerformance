# Pastebin

## Giới thiệu
Đây là một hệ thống Pastebin Monolith đơn giản với mục tiêu đánh giá hiệu suất sử dụng công cụ Locust. Hệ thống được thiết kế nhằm cung cấp một nền tảng pastebin Monolith đơn giản, cho phép người dùng tạo, lưu trữ, và quản lý các đoạn văn bản (paste). Để đảm bảo hiệu suất tối ưu và khả năng mở rộng, em đã thực hiện kiểm thử tải bằng Locust nhằm đo lường các chỉ số quan trọng như thời gian phản hồi, thông lượng, mức sử dụng tài nguyên và khả năng mở rộng khi số lượng người dùng tăng lên.

## Tính năng chính
- Cho phép người dùng tạo, lưu trữ và truy xuất văn bản.
- Cung cấp API để truy cập dữ liệu.
- Đánh giá hiệu suất hệ thống với Locust.
- Theo dõi các chỉ số quan trọng như:
  - **Độ trễ (Latency):**
  - **Thông lượng (Throughput):** 
  - **Tài nguyên sử dụng (Resource Utilization):** 
  - **Khả năng mở rộng (Scalability):**.
##  Giao diện và hướng dẫn sử dụng
Giao diện tạo Paste:

![image](https://github.com/user-attachments/assets/cc04c4bd-df75-4bed-ad24-50b1a25b4096)

Giao diện danh sách Pastes:

![image](https://github.com/user-attachments/assets/dd790514-63e2-4dfa-b451-3a60fe763a82)

Giao diện một Paste Detail:

![image](https://github.com/user-attachments/assets/2bdb8f99-632a-4658-a579-6d8ae7f63066)

Giao diện Paste hết hạn hoặc không tồn tại:

![image](https://github.com/user-attachments/assets/094b574f-da0f-49cb-8cf0-1be5d0bd6ca5)


##  Cài đặt

### 1. Yêu cầu hệ thống
- Python 3.x
- Git
- Locust
- Django

### 2. Clone repository
```bash
git clone https://github.com/ngquan244/PastebinPerformance.git
cd PastebinPerformance
```

### 3. Tạo virtual environment (khuyến nghị)
```bash
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate    # Trên Windows
```

### 4. Cài đặt các thư viện yêu cầu
```bash
pip install -r requirements.txt
```

##  Cách chạy dự án

### 1. Khởi chạy server
```bash
cd pastebin_project
python manage.py runserver   
```

### 2. Chạy kiểm thử hiệu suất với Locust
```bash
locust
```
Sau đó, truy cập `http://localhost:8089` để theo dõi kết quả.

##  Kết quả đo lường
Các chỉ số hiệu suất sẽ được hiển thị trên giao diện Locust, giúp đánh giá khả năng xử lý của hệ thống.

## 📌 Liên hệ
Nếu bạn có bất kỳ câu hỏi hoặc góp ý nào, hãy liên hệ qua GitHub Issues hoặc email của tôi.

 Email: smisumikus@gmail.com

