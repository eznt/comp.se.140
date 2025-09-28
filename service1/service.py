import http.server, os, time, datetime, shutil, requests

PORT = int(os.environ.get("PORT"))
SERVICE2_URL = os.environ.get("SERVICE2_URL")
STORAGE_URL = os.environ.get("STORAGE_URL")
VSTORAGE = os.environ.get("VSTORAGE_PATH")

UP = time.time()

def now():
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

def uptime_hours():
    return (time.time() - UP) / 3600

def free():
    return shutil.disk_usage("/").free / (1024 * 1024)

def create_record():
    return f"{now()}: uptime {uptime_hours():.2f} hours, free disk in root: {free():.1f} MBytes"

class Service(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            record = "Timestamp1: " + create_record()
            try:
                requests.post(f"{STORAGE_URL}/log", data=record, headers={"Content-Type":"text/plain"})
            except:
                pass
            with open(VSTORAGE, "a", encoding="utf-8") as file:
                file.write(record + "\n")
            try:
                response = requests.get(f"{SERVICE2_URL}/status")
            except:
                pass
            service2_record = response.text
            self.respond_text(record + "\n" + service2_record + "\n")

        elif self.path == "/log":
            try:
                response = requests.get(f"{STORAGE_URL}/log")
            except:
                pass
            self.respond_text(response.text)

    def respond_text(self, text):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(text.encode("utf-8"))

def main():
    server = http.server.HTTPServer(("0.0.0.0", PORT), Service)
    print(f"Service 1 running on port {PORT}", flush=True)
    server.serve_forever()
if __name__ == "__main__":
    main()