import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .tools import list_docs, reload_index, retrieve_faq


class ToolServerHandler(BaseHTTPRequestHandler):
    server_version = "FAQToolServer/0.1"

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid_json"})
            return

        tool = payload.get("tool")
        args = payload.get("args") or {}

        try:
            if tool == "retrieve_faq":
                result = retrieve_faq(**args)
            elif tool == "list_docs":
                result = list_docs(**args)
            elif tool == "reload_index":
                result = reload_index(**args)
            else:
                self._send_json(400, {"error": "unknown_tool"})
                return
        except Exception as exc:
            self._send_json(500, {"error": "tool_error", "detail": str(exc)})
            return

        self._send_json(200, {"ok": True, "result": result})


def run(host="127.0.0.1", port=8765):
    server = HTTPServer((host, port), ToolServerHandler)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
