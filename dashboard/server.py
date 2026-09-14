from http.server import BaseHTTPRequestHandler, HTTPServer
from meshweaver.node import MeshNode


node = MeshNode(port=9001)


class DashboardHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            metadata = node.get_metadata()

            status = "ONLINE" if metadata["running"] else "OFFLINE"

            resources = metadata.get("resources", {})

            cpu = resources.get("cpu_percent", 0)
            memory = resources.get("memory_percent", 0)

            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>MeshWeaver Dashboard</title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: white;
            margin: 0;
            padding: 30px;
        }}

        h1 {{
            text-align: center;
            margin-bottom: 35px;
        }}

        .container {{
            max-width: 1100px;
            margin: auto;
        }}

        .cards {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background: #1e293b;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
        }}

        .number {{
            font-size: 32px;
            font-weight: bold;
            margin-top: 10px;
        }}

        .online {{
            color: #22c55e;
        }}

        .offline {{
            color: #ef4444;
        }}

        .info {{
            background: #1e293b;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
        }}

        .row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #334155;
        }}

        .row:last-child {{
            border-bottom: none;
        }}

    </style>
</head>

<body>

<div class="container">

    <h1>MeshWeaver Monitoring Dashboard</h1>

    <div class="cards">

        <div class="card">
            <h3>Node Status</h3>
            <div class="number {'online' if metadata['running'] else 'offline'}">
                {status}
            </div>
        </div>

        <div class="card">
            <h3>Peers</h3>
            <div class="number">
                {metadata["peer_count"]}
            </div>
        </div>

        <div class="card">
            <h3>CPU</h3>
            <div class="number">
                {cpu:.1f}%
            </div>
        </div>

        <div class="card">
            <h3>Memory</h3>
            <div class="number">
                {memory:.1f}%
            </div>
        </div>

    </div>

    <div class="info">

        <h2>Node Information</h2>

        <div class="row">
            <span>Node ID</span>
            <span>{metadata["node_id"]}</span>
        </div>

        <div class="row">
            <span>Host</span>
            <span>{metadata["host"]}</span>
        </div>

        <div class="row">
            <span>Port</span>
            <span>{metadata["port"]}</span>
        </div>

        <div class="row">
            <span>Running</span>
            <span>{metadata["running"]}</span>
        </div>

        <div class="row">
            <span>Peer Count</span>
            <span>{metadata["peer_count"]}</span>
        </div>

    </div>

    <div class="info">

        <h2>MeshWeaver Architecture</h2>

        <div class="row">
            <span>Network</span>
            <span>P2P</span>
        </div>

        <div class="row">
            <span>Communication</span>
            <span>Async UDP</span>
        </div>

        <div class="row">
            <span>Peer Discovery</span>
            <span>Kademlia DHT</span>
        </div>

        <div class="row">
            <span>Resource Monitoring</span>
            <span>CPU / Memory</span>
        </div>

    </div>

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