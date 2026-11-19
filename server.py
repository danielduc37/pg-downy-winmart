import os
import json
import time
import base64
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    
    env_file = os.path.join(DIRECTORY, ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return ""

class OCRHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == "/api/extract":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            
            try:
                payload = json.loads(body.decode("utf-8"))
                image_base64 = payload.get("image")
                mime_type = payload.get("mime_type", "image/jpeg")

                if not image_base64:
                    self.send_error_json(400, "Vui lòng chọn ảnh hóa đơn.")
                    return

                api_key = get_api_key()
                if not api_key:
                    self.send_error_json(500, "Server chưa có API Key trong file .env.")
                    return

                extracted_text = self.call_gemini(api_key, image_base64, mime_type)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                response = json.dumps({"success": True, "text": extracted_text}, ensure_ascii=False)
                self.wfile.write(response.encode("utf-8"))

            except Exception as e:
                self.send_error_json(500, str(e))
        else:
            self.send_error(404, "Not Found")

    def call_gemini(self, api_key, image_base64, mime_type):
        prompt = (
            "Bạn là chuyên gia OCR văn bản và hóa đơn. "
            "Hãy đọc và trích xuất TOÀN BỘ nội dung chữ và số có trong ảnh hóa đơn/chứng từ này một cách đầy đủ, chính xác 100%. "
            "Giữ nguyên định dạng từng dòng, từng con số, mã số và ký tự tiếng Việt. "
            "Không bỏ sót bất kỳ dòng nào (kể cả số hóa đơn, ngày giờ, danh sách mặt hàng, số lượng, đơn giá, thành tiền, tổng tiền, điểm tích lũy, mã CQT, thông tin khuyến mãi)."
        )

        # Sử dụng các model thuộc gói Free Tier có hạn mức miễn phí cao nhất
        models = ["gemini-flash-lite-latest", "gemini-3-flash-preview"]
        last_err = None

        for model in models:
            for attempt in range(2):
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
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        resp_json = json.loads(resp.read().decode("utf-8"))
                        candidate = resp_json.get("candidates", [{}])[0]
                        text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
                        if text:
                            return text
                except urllib.error.HTTPError as e:
                    err_msg = e.read().decode("utf-8", errors="ignore")
                    last_err = f"Lỗi Google API ({e.code}): {err_msg}"
                    if e.code in [503, 429]:
                        time.sleep(1)
                        continue
                    break
                except Exception as e:
                    last_err = str(e)
                    time.sleep(1)

        raise Exception(last_err or "Không thể đọc nội dung ảnh.")

    def send_error_json(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        response = json.dumps({"success": False, "error": message}, ensure_ascii=False)
        self.wfile.write(response.encode("utf-8"))

def run():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, OCRHandler)
    print(f"Server OCR AI running at http://localhost:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
