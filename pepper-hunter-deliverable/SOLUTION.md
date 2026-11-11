<!-- Ban thao do Gemini lam qua Pepper Hunter Doer - CHUA NOP, can duyet truoc khi gui. -->

Chào bạn, dưới đây là file `SOLUTION.md` được phân tích và tổng hợp dựa trực tiếp trên nội dung issue `BOUNTY-03: CrewAI tool wrappers for dispute_letter + contract_analyze`.

---

# SOLUTION.md

## 1. Tóm tắt yêu cầu & Tiêu chí nghiệm thu (Acceptance Criteria)
Trích xuất từ nội dung issue `BOUNTY-03`:

*   **Mục tiêu chính:** Xây dựng các CrewAI `@tool` wrappers gọi đến RAEN MCP gateway để tích hợp vào CrewAI flow, cho phép agent thực hiện các tác vụ:
    *   Soạn thảo thư tranh chấp (`dispute_letter`).
    *   Phân tích hợp đồng (`contract_analyze`).
*   **Tiêu chí nghiệm thu (Acceptance Criteria):**
    *   Repository ở chế độ public, có thể cài đặt qua `pip` hoặc import dạng file đơn (`single-file importable`).
    *   Có script ví dụ (example crew script) minh họa ít nhất một lời gọi thực tế (`one real call`).
    *   Có file `README` hướng dẫn sử dụng.

---

## 2. Cách tiếp cận kỹ thuật từng bước (Step-by-step Technical Approach)

1.  **Khởi tạo cấu trúc dự án & Quản lý phụ thuộc:**
    *   Thiết lập file cấu hình gói (ví dụ: `pyproject.toml` hoặc `setup.py`) để hỗ trợ cài đặt qua `pip`.
    *   Khai báo các thư viện phụ thuộc cốt lõi: `crewai` (và các package liên quan đến `@tool`), cùng với client để giao tiếp với RAEN MCP gateway.
2.  **Triển khai CrewAI Tool Wrappers:**
    *   Sử dụng decorator `@tool` từ CrewAI để định nghĩa các tool wrappers.
    *   Viết logic gọi API/MCP gateway cho từng chức năng:
        *   Tool 1: `dispute_letter` (nhận đầu vào thông tin tranh chấp, gọi gateway để trả về bản thảo thư tranh chấp).
        *   Tool 2: `contract_analyze` (nhận nội dung/đường dẫn hợp đồng, gọi gateway để trả về kết quả phân tích).
3.  **Xây dựng Script ví dụ (Example Crew Script):**
    *   Tạo một file script minh họa (ví dụ: `examples/run_crew.py`) khởi tạo một CrewAI crew đơn giản, gán tool wrappers vừa tạo cho agent và thực thi ít nhất một luồng gọi thực tế.
4.  **Viết Tài liệu (README):**
    *   Soạn thảo `README.md` hướng dẫn chi tiết cách cài đặt, cấu hình biến môi trường (nếu có cho MCP gateway), và cách chạy script ví dụ.

---

## 3. File & Đường dẫn dự kiến sửa/tạo (Expected Files & Paths)
*(Lưu ý: Do cấu trúc repo cụ thể chưa được hiển thị chi tiết trong issue, các đường dẫn dưới đây là cấu trúc tiêu chuẩn dự kiến cho yêu cầu này).*

*   `pyproject.toml` hoặc `setup.py` *(Cấu hình gói pip-installable)*
*   `README.md` *(Tài liệu hướng dẫn)*
*   `raen_crewai_tools/__init__.py` *(Hoặc tên module chính chứa source code)*
*   `raen_crewai_tools/tools.py` *(Chứa các định nghĩa `@tool` cho `dispute_letter` và `contract_analyze`)*
*   `examples/crew_example.py` *(Script ví dụ minh họa một lời gọi thực tế)*

---

## 4. Kế hoạch tự test (Self-Test Plan)

1.  **Test cài đặt gói:**
    *   Chạy lệnh cài đặt cục bộ (ví dụ: `pip install -e .`) để đảm bảo gói có thể được cài đặt chính xác mà không có lỗi thiếu dependency.
2.  **Test Unit/Integration cho Tool Wrappers:**
    *   Kiểm tra việc gọi các `@tool` wrapper (`dispute_letter` và `contract_analyze`) với dữ liệu giả lập (mock data) hoặc kết nối trực tiếp đến RAEN MCP gateway (nếu có key test) để đảm bảo dữ liệu truyền đi và nhận về đúng định dạng mà CrewAI yêu cầu.
3.  **Test Script ví dụ:**
    *   Chạy script ví dụ (`python examples/crew_example.py`) để xác thực toàn bộ luồng hoạt động từ Agent -> Tool Wrapper -> RAEN MCP Gateway trả về kết quả thành công không có ngoại lệ (exception).
