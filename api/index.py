from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve index.html or health check
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        
        # Try finding index.html in current or parent dir
        for p in ["index.html", "../index.html", os.path.join(os.path.dirname(__file__), "..", "index.html")]:
            if os.path.exists(p):
                with open(p, "rb") as f:
                    self.wfile.write(f.read())
                return
        self.wfile.write(b"pg.downy.winmart API is running")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body.decode("utf-8"))
            image_base64 = payload.get("image")
            mime_type = payload.get("mime_type", "image/jpeg")

            if not image_base64:
                self.send_error_json(400, "Vui lòng chọn ảnh hóa đơn.")
                return

            api_key = os.environ.get("GEMINI_API_KEY", "").strip()
            if not api_key:
                self.send_error_json(500, "Chưa cài đặt GEMINI_API_KEY trên Vercel Environment Variables.")
                return

            prompt = (
                "Bạn là chuyên gia OCR văn bản và hóa đơn. "
                "Hãy đọc và trích xuất TOÀN BỘ nội dung chữ và số có trong ảnh hóa đơn/chứng từ này một cách đầy đủ, chính xác 100%. "
                "Giữ nguyên định dạng từng dòng, từng con số, mã số và ký tự tiếng Việt. "
                "Không bỏ sót bất kỳ dòng nào (kể cả số hóa đơn, ngày giờ, danh sách mặt hàng, số lượng, đơn giá, thành tiền, tổng tiền, điểm tích lũy, mã CQT, thông tin khuyến mãi)."
            )

            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"
            req_data = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 4096
                }
            }

            req = urllib.request.Request(
                endpoint,
                data=json.dumps(req_data).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                text = resp_json["candidates"][0]["content"]["parts"][0]["text"]

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "text": text}, ensure_ascii=False).encode("utf-8"))

        except Exception as e:
            self.send_error_json(500, str(e))

    def send_error_json(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"success": False, "error": message}, ensure_ascii=False).encode("utf-8"))

app = handler
