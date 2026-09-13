from http.server import BaseHTTPRequestHandler, HTTPServer


class DashboardHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            html = """
<!DOCTYPE html>
<html>
<head>
    <title>MeshWeaver Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: white;
            margin: 0;
            padding: 30px;
        }

        h1 {
            text-align: center;
        }

        .cards {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin: 30px 0;
        }

        .card {
            background: #1e293b;
            padding: 25px;
            width: 180px;
            text-align: center;
            border-radius: 12px;
        }

        .number {
            font-size: 35px;
            font-weight: bold;
        }

        .status {
            color: #22c55e;
        }
    </style>
</head>

<body>

    <h1>MeshWeaver Monitoring Dashboard</h1>

    <div class="cards">

        <div class="card">
            <h3>Total Nodes</h3>
            <div class="number">1</div>
        </div>

        <div class="card">
            <h3>Online</h3>
            <div class="number status">1</div>
        </div>

        <div class="card">
            <h3>Offline</h3>
            <div class="number">0</div>
        </div>

        <div class="card">
            <h3>Running Tasks</h3>
            <div class="number">0</div>
        </div>

    </div>

    <h2>MeshWeaver Status</h2>

    <div class="card">
        <p>Network: <span class="status">ONLINE</span></p>
        <p>Communication: UDP</p>
        <p>Architecture: P2P</p>
        <p>Discovery: Kademlia DHT</p>
    </div>

</body>
</html>
"""

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        else:
            self.send_response(404)
            self.end_headers()


def start_dashboard(host="127.0.0.1", port=8000):
    server = HTTPServer((host, port), DashboardHandler)

    print(f"MeshWeaver Dashboard running at http://{host}:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
        server.server_close()


if __name__ == "__main__":
    start_dashboard()