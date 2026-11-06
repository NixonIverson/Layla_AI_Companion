"""Serves index.html and forwards /api/* to your local Ollama. No pip installs needed."""
import http.server, urllib.request, urllib.error, json, os

OLLAMA = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
PORT = int(os.environ.get("PORT", 8000))
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/"):
            return self.proxy()
        try:
            with open(os.path.join(ROOT, "index.html"), "rb") as f:
                data = f.read()
        except OSError:
            return self.send_error(404)
        self.reply(200, data, "text/html; charset=utf-8")

    def do_POST(self):
        self.proxy()

    def proxy(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n) if n else None
        req = urllib.request.Request(OLLAMA + self.path, data=body, method=self.command,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                self.reply(r.status, r.read(), "application/json")
        except urllib.error.HTTPError as e:
            self.reply(e.code, e.read(), "application/json")
        except Exception as e:
            self.reply(502, json.dumps({"error": f"Can't reach Ollama at {OLLAMA}: {e}"}).encode(), "application/json")

    def reply(self, code, data, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"Open http://localhost:{PORT}  (Ollama: {OLLAMA})")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()