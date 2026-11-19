# ⚡ Smart OCR AI - Trích xuất Văn bản & Hóa đơn Thông minh (100% Free)

Ứng dụng Web OCR trực quan, hiện đại, chạy trực tiếp trên trình duyệt sử dụng mô hình **Google Gemini Flash** mạnh mẽ nhất.

---

## 🌟 Tính năng nổi bật
1. **100% Miễn phí & Không cần máy chủ (Zero Server Cost):** Web chạy hoàn toàn bằng HTML + JavaScript thuần, trực tiếp gọi API của Google từ trình duyệt của người dùng.
2. **Đa dạng phương thức nhập ảnh:**
   - Kéo & thả file ảnh trực tiếp vào giao diện.
   - Bấm chọn file từ máy tính hoặc điện thoại (JPG, PNG, WEBP, HEIC...).
   - **Dán trực tiếp từ bộ nhớ tạm (`Ctrl + V`)**: Chụp màn hình rồi paste vào là xong ngay!
3. **4 Chế độ trích xuất chuyên sâu:**
   - 🧾 **Hóa đơn & Chứng từ (Smart Receipt):** Tự động bóc tách tên cửa hàng, ngày giờ, bảng danh sách món (Đơn giá, SL, Thành tiền), tổng tiền, mã CQT, voucher khuyến mãi.
   - 📊 **Bảng biểu (Table):** Xuất bảng Markdown Table chuẩn, copy 1-click dán vào Excel / Google Sheets.
   - 📝 **Toàn bộ văn bản (Raw OCR):** Đọc nguyên bản từng dòng chữ, số hiệu, biểu tượng.
   - 💻 **JSON Structured:** Trích xuất dạng JSON chuẩn phục vụ lập trình và tự động hóa.
4. **Tiện ích:**
   - Nút **Sao chép 1-click** toàn bộ nội dung.
   - Nút **Tải file kết quả (.txt, .md, .json)**.
   - Quản lý API Key an toàn trong LocalStorage của máy người dùng.

---

## 🚀 Hướng dẫn sử dụng ngay trên máy tính
1. Vào thư mục `ocr-web/`.
2. **Nhấp đúp chuột vào file `index.html`** để mở bằng Chrome, Edge, Cốc Cốc hoặc bất kỳ trình duyệt nào.
3. Bấm **"Cài đặt API Key"** ở góc phải:
   - Nếu chưa có key, bấm vào link [Google AI Studio](https://aistudio.google.com/app/apikey).
   - Đăng nhập tài khoản Google và bấm **Create API key** (Miễn phí 1.500 lượt/ngày).
   - Dán mã key vào web và bấm **Lưu & Áp dụng**.
4. Kéo ảnh hoặc bấm `Ctrl + V` và bấm **Bắt đầu Đọc Chữ**!

---

## 🌐 Cách đưa lên mạng online cho bất kỳ ai cũng vào được (0 đồng)

### Cách 1: Dùng Vercel (Khuyên dùng - Nhanh nhất)
1. Đăng ký tài khoản miễn phí tại [vercel.com](https://vercel.com).
2. Cài đặt hoặc dùng giao diện Web của Vercel kéo thả thư mục `ocr-web` lên.
3. Vercel sẽ tự động cấp cho bạn một đường link HTTPS công khai (ví dụ: `https://smart-ocr-ai.vercel.app`) để gửi cho bất kỳ ai.

### Cách 2: Dùng Netlify Drop (Không cần tạo tài khoản phức tạp)
1. Truy cập [app.netlify.com/drop](https://app.netlify.com/drop).
2. Kéo cả thư mục `ocr-web` thả vào khung trình duyệt.
3. Sau 5 giây, Netlify sẽ cấp cho bạn một đường link online dùng được ngay lập tức!

### Cách 3: Dùng GitHub Pages
1. Tạo 1 repository mới trên GitHub (chế độ Public).
2. Tải file `index.html` lên repository.
3. Vào **Settings** -> **Pages** -> mục **Branch** chọn `main` và bấm **Save**.
4. Link web sẽ có dạng: `https://<ten-tai-khoan>.github.io/<ten-repo>`.
