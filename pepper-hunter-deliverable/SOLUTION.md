<!-- Ban thao do Gemini lam qua Pepper Hunter Doer - CHUA NOP, can duyet truoc khi gui. -->

Chào bạn, dưới đây là file `SOLUTION.md` được phân tích và soạn thảo dựa hoàn toàn trên nội dung issue được cung cấp, tuân thủ đúng vai trò kỹ sư phần mềm.

```markdown
# SOLUTION.md - BOUNTY-02: One-file Python CLI client for the 12-service x402 fleet

## 1. Tóm tắt yêu cầu & Tiêu chí nghiệm thu (Acceptance Criteria)
Trích xuất trực tiếp từ issue #2:

- **Mục tiêu:** Xây dựng một ứng dụng dòng lệnh (CLI) bằng Python nằm trong một file duy nhất (`raen-cli.py`).
- **Thư viện sử dụng:** Sử dụng Python Standard Library và tối đa 1 dependency cho việc ký (signer dep).
- **Chức năng cốt lõi:**
  1. Đọc danh sách các dịch vụ RAEN x402 từ file `agents.json`.
  2. Liệt kê (lists) tất cả các dịch vụ x402 có trong `agents.json`.
  3. Gửi một request trả phí (paid call) tới bất kỳ dịch vụ nào được chọn thông qua cú pháp lệnh.
  4. Xử lý thành công vòng lặp xác thực thanh toán: Nhận mã lỗi `402` -> Thực hiện thanh toán -> Nhận lại phản hồi đã thanh toán (`settled-response`).
  5. In ra biên lai thanh toán x402 (`settlement receipt`).

- **Tiêu chí nghiệm thu (Acceptance Criteria):**
  - Chạy thành công lệnh end-to-end: `python raen-cli.py <service> <prompt>`
  - Xử lý trọn vẹn luồng: `402 -> payment -> settled-response loop`
  - Hình thức nộp bài: Public repository hoặc Pull Request trực tiếp vào repo của bounty.

---

## 2. Cách tiếp cận kỹ thuật từng bước (Step-by-step Technical Approach)

1. **Khởi tạo file chương trình duy nhất (`raen-cli.py`):**
   - Sử dụng các module tiêu chuẩn của Python (ví dụ: `sys`, `json`, `urllib` hoặc `requests` nếu cần, nhưng ưu tiên `urllib` của stdlib để giữ nguyên tắc "one-file/stdlib").
   - Import thư viện signer bên thứ nhất (được chỉ định hoặc ngầm định trong hệ sinh thái x402, dựa trên yêu cầu "one signer dep").

2. **Xử lý nguồn dữ liệu (`agents.json`):**
   - Viết hàm đọc và parse file `agents.json` để lấy danh sách endpoint, thông tin định danh của 12 dịch vụ x402 fleet.
   - Thêm logic hiển thị danh sách (liệt kê) khi chạy CLI mà không có tham số hoặc ở chế độ list.

3. **Xây dựng CLI Parser:**
   - Sử dụng `sys.argv` hoặc thư viện `argparse` (thuộc Python Standard Library) để nhận cú pháp: `python raen-cli.py <service> <prompt>`.

4. **Xử lý Vòng lặp Giao dịch x402 (The 402 Loop):**
   - **Bước A (Request ban đầu):** Gửi HTTP POST/GET request chứa `<prompt>` tới endpoint của `<service>`.
   - **Bước B (Bắt lỗi 402):** Kiểm tra mã trạng thái HTTP trả về. Nếu nhận được mã `402 Payment Required`, tiến hành đọc thông tin yêu cầu thanh toán từ header hoặc body phản hồi.
   - **Bước C (Thanh toán / Ký giao dịch):** Sử dụng `signer dep` để thực hiện việc ký và thanh toán theo chuẩn x402.
   - **Bước D (Gửi lại request kèm bằng chứng thanh toán):** Gửi lại request ban đầu kèm theo thông tin/chứng nhận thanh toán (settlement proof).
   - **Bước E (Nhận kết quả & In biên lai):** Nhận phản hồi thành công (`settled-response`) và in ra biên lai thanh toán x402 cùng nội dung phản hồi từ service.

---

## 3. File / Đường dẫn dự kiến sửa
*(Lưu ý: Do cấu trúc repo cụ thể chưa được mô tả chi tiết trong issue, đây là cấu trúc file dự kiến)*

- `raen-cli.py` (File mã nguồn chính đặt tại thư mục gốc của repository)
- `agents.json` (File dữ liệu nguồn chứa danh sách 12 dịch vụ x402 - đọc để lấy thông tin endpoint)

---

## 4. Kế hoạch tự test (Self-Test Plan)

1. **Test liệt kê dịch vụ:**
   - Chạy lệnh kiểm tra việc đọc file `agents.json` và in ra danh sách 12 dịch vụ x402.
2. **Test luồng gọi API thông thường (nếu có dịch vụ không yêu cầu trả phí hoặc test mock):**
   - Đảm bảo CLI phân giải đúng tên `<service>` thành URL endpoint từ `agents.json`.
3. **Test vòng lặp x402 (End-to-End):**
   - Chạy lệnh thực tế: `python raen-cli.py <test-service> "Hello RAEN"`
   - Xác thực rằng ứng dụng bắt được mã `402`, gọi module signer thực hiện thanh toán, đính kèm biên lai vào request tiếp theo và nhận về `settled-response`.
4. **Test hiển thị biên lai:**
   - Kiểm tra định dạng đầu ra trên màn hình console để đảm bảo biên lai thanh toán x402 được in ra rõ ràng, đầy đủ thông tin theo yêu cầu của issue.
```
