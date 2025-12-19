import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    # Allow WASM files to be served correctly
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()

if __name__ == "__main__":
    # Ensure we are in the project root
    if not os.path.exists("src") or not os.path.exists("web"):
        print("Error: Please run this script from the project root folder.")
        exit(1)

    print(f"🚀 Starting server at http://localhost:{PORT}")
    print("Opening browser...")
    
    # Open specifically the web folder
    webbrowser.open(f"http://localhost:{PORT}/web/")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")