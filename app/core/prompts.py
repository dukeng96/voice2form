from datetime import date
from typing import Dict

WEEKDAY_VI = {
    0: "Thứ hai",
    1: "Thứ ba",
    2: "Thứ tư",
    3: "Thứ năm",
    4: "Thứ sáu",
    5: "Thứ bảy",
    6: "Chủ nhật",
}
TODAY = date.today().isoformat()           # ví dụ: "2025-07-14"
TODAY_WEEKDAY = WEEKDAY_VI[date.today().weekday()]

FIX_JSON_PROMPT = """
Bạn là *trình sửa JSON*.
Dưới đây là chuỗi JSON **bị lỗi cú pháp** như sau: {json_bug}

{bad_json}

Hãy:
1. Sửa lại để JSON hợp lệ tuyệt đối (RFC 8259).
2. Giữ nguyên tối đa nội dung, khóa, thứ tự; chỉ thêm/bỏ ký tự để hợp lệ.
3. KHÔNG thêm mô tả, KHÔNG bọc ```json, KHÔNG in thừa bất kỳ chữ nào khác.

Chỉ trả về **duy nhất** chuỗi JSON hợp lệ và không thêm text gì khác.
"""

VAT_TU_PROMPT = r"""Bạn là trình trích xuất thông tin cho ứng dụng Nông Nghiệp Số.
Đọc câu nói sau của người dân: {input_text}

Trả về một object JSON với đầy đủ các khóa sau.
Nếu thông tin không có, ghi giá trị là chuỗi rỗng "". Chỉ xuất JSON, không thêm chú thích.

```json
{{
  "loaiVatTu": "",          // Ví dụ: "Phân bón", "Thuốc BVTV", "Giống"
  "tenVatTu": "",           // Tên sản phẩm hoặc hoạt chất: "N-P-K 20-10-10"
  "danhMuc": "",            // Nhóm: "Phân bón vô cơ"
  "thuongHieu": "",         // Thương hiệu / nhà SX: "Đất Xanh"
  "nguonGoc": "",           // "Nội địa" | "Nhập khẩu" | …
  "donViTinhSuDung": "",    // Đơn vị khi sử dụng: "kg", "lít"
  "donViLuuKho": ""         // Đơn vị lưu kho: "bao", "chai"
}}
```
"""

CHUNG_TU_PROMPT = r"""Bạn là trình trích xuất chứng từ mua vật tư cho ứng dụng Nông Nghiệp Số.
Hôm nay là {current_date} ({current_weekday}).
Đọc câu nói sau của người dân: {input_text}

Trả về một object JSON với định dạng dưới đây.
Nếu thiếu thông tin, để "" hoặc [] nếu là mảng. Chỉ xuất JSON, không kèm văn bản khác.

```json
{{
  "tenGianHang": "",        // Tên cửa hàng/đại lý
  "diaChiGianHang": "",     // Địa chỉ (xã, huyện, tỉnh…)
  "ngayMuaHang": "",        // Định dạng ISO: "YYYY-MM-DD", mặc định năm 2025
  "muaVu": "",              // Ví dụ: "Mùa vụ 2024"
  "loaiChungTu": "",        // "Chứng từ mua hàng", "Hóa đơn bán lẻ"…
  "dauVaoNhom": [],           // Danh sách vật tư thuộc nhóm trang trại
  "dauVaoTrangTrai": ""     // “Đầu vào của trang trại” / “Thuê ngoài”
}}
```
"""

CONG_VIEC_PROMPT = r"""Bạn là trình trích xuất thông tin công việc nông nghiệp cho ứng dụng Nông Nghiệp Số.
Hôm nay là {current_date} ({current_weekday}).
Đọc câu nói sau của người dân: {input_text}

Trả về một object JSON với cấu trúc sau.
Nếu không tìm thấy thông tin, để "" hoặc []. Chỉ xuất JSON, không giải thích thêm.

```json
{{
  "tenCongViec": "",        // Ví dụ: "Bón phân cải tạo đất"
  "ngayThucHien": "",       // "YYYY-MM-DD" hoặc suy luận từ “hôm qua”, “tuần trước”
  "moTa": "",               // Mô tả ngắn 1-2 câu
  "danhSachVatTu": [
    {{
      "tenVatTu": "",       // Ví dụ: "NPK 2-9-0"
      "luong": "",          // Số lượng, có thể kèm đơn vị: "4"
      "donVi": "",          // "kg", "gam", "lít"…
      "tansuat": ""         // "1 cây", "1 gốc" (nếu không nói thì để trống)
    }}
  ]
}}
```
"""

PROMPTS: Dict[str, str] = {
    "vat_tu": VAT_TU_PROMPT,
    "chung_tu": CHUNG_TU_PROMPT,
    "cong_viec": CONG_VIEC_PROMPT,
}
