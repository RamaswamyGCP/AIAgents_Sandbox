import http.server
import socketserver
import sys

# Try ports 8000, 8001, 8002...
start_port = 8000
Handler = http.server.SimpleHTTPRequestHandler

for port in range(start_port, start_port + 10):
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"\n✅ Frontend Server started!")
            print(f"👉 Open this link: http://localhost:{port}/index.html")
            print("\n(Press Ctrl+C to stop)")
            httpd.serve_forever()
        break
    except OSError:
        print(f"Port {port} is busy, trying next...")
        continue
