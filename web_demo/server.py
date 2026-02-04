import json
import os
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Simple in-memory database
TASKS = [
    {"id": 1, "title": "Review code", "completed": False},
    {"id": 2, "title": "Write documentation", "completed": True}
]
NEXT_ID = 3

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # API Endpoint: Get all tasks
        if parsed_path.path == '/api/tasks':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(TASKS).encode('utf-8'))
            return

        # Serve Static Files
        if parsed_path.path == '/':
            filepath = 'public/index.html'
        else:
            filepath = 'public' + parsed_path.path

        # Security check: prevent directory traversal
        if '..' in filepath:
            self.send_error(403)
            return

        if os.path.exists(filepath) and os.path.isfile(filepath):
            mime_type, _ = mimetypes.guess_type(filepath)
            self.send_response(200)
            self.send_header('Content-Type', mime_type or 'application/octet-stream')
            self.end_headers()
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                global NEXT_ID
                new_task = {
                    "id": NEXT_ID,
                    "title": data.get("title", "Untitled"),
                    "completed": False
                }
                TASKS.append(new_task)
                NEXT_ID += 1
                
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(new_task).encode('utf-8'))
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
        else:
            self.send_error(404)

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        
        # Expecting /api/tasks/<id>
        if parsed_path.path.startswith('/api/tasks/'):
            try:
                task_id = int(parsed_path.path.split('/')[-1])
                global TASKS
                
                # Filter out the task with the given ID
                initial_len = len(TASKS)
                TASKS = [t for t in TASKS if t['id'] != task_id]
                
                if len(TASKS) < initial_len:
                    self.send_response(204)
                    self.end_headers()
                else:
                    self.send_error(404, "Task not found")
            except ValueError:
                self.send_error(400, "Invalid ID")
        else:
            self.send_error(404)

def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    print(f"Open http://localhost:{port} in your browser")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
