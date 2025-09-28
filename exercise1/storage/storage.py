import http.server, os

LOG_PATH = os.environ.get("LOG_PATH")
PORT = int(os.environ.get("PORT"))

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

class Storage(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/log":
            n = int(self.headers.get("Content-Length", 0))
            record = self.rfile.read(n)
            with open(LOG_PATH, "a", encoding="utf-8") as file:
                file.write(record + "\n")
            self.send_response(200)
            self.end_headers()

    def do_GET(self):
        if self.path == "/log":
            try:
                with open(LOG_PATH, "r", encoding="utf-8") as file:
                    data = file.read()
            except FileNotFoundError:
                data = ""
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(data)

def main():
    server = http.server.HTTPServer(("0.0.0.0", PORT), Storage)
    print(f"Storage running on port {PORT}")
    server.serve_forever()
if __name__ == "__main__":
    main()