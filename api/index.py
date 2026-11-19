from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
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
                self.send_error_json(500, "Server chưa được cấu hình GEMINI_API_KEY trong Environment Variables.")
                return

            extracted_text = self.call_gemini(api_key, image_base64, mime_type)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            response = json.dumps({"success": True, "text": extracted_text}, ensure_ascii=False)
            self.wfile.write(response.encode("utf-8"))

        except Exception as e:
            self.send_error_json(500, str(e))

    def call_gemini(self, api_key, image_base64, mime_type):
        prompt = (
            "Bạn là chuyên gia OCR văn bản và hóa đơn. "
            "Hãy đọc và trích xuất TOÀN BỘ nội dung chữ và số có trong ảnh hóa đơn/chứng từ này một cách đầy đủ, chính xác 100%. "
            "Giữ nguyên định dạng từng dòng, từng con số, mã số và ký tự tiếng Việt. "
            "Không bỏ sót bất kỳ dòng nào (kể cả số hóa đơn, ngày giờ, danh sách mặt hàng, số lượng, đơn giá, thành tiền, tổng tiền, điểm tích lũy, mã CQT, thông tin khuyến mãi)."
        )

        models = ["gemini-flash-lite-latest", "gemini-3-flash-preview"]
        last_err = None

        for model in models:
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
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

            try:
                req = urllib.request.Request(
                    endpoint,
                    data=json.dumps(req_data).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=35) as resp:
                    resp_json = json.loads(resp.read().decode("utf-8"))
                    candidate = resp_json.get("candidates", [{}])[0]
                    text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
                    if text:
                        return text
            except Exception as e:
                last_err = str(e)

        raise Exception(last_err or "Không thể đọc nội dung ảnh.")

    def send_error_json(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        response = json.dumps({"success": False, "error": message}, ensure_ascii=False)
        self.wfile.write(response.encode("utf-8"))

app = handler
