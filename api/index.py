from http.server import BaseHTTPRequestHandler
from .db import get_connection, init_db, increment_and_get_count

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            conn = get_connection()
            init_db(conn)
            count = increment_and_get_count(conn)
            message = f"Hello, this is homepage for ordering food service. Visits: {count}"

            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode('utf-8'))
        finally:
            try:
                conn.close()
            except Exception:
                pass
        return
