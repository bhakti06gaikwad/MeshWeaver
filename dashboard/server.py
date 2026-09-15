import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from meshweaver.node import MeshNode


node = MeshNode(host="127.0.0.1", port=9001)


def start_node():
    asyncio.run(node.start())


# Start MeshWeaver node in background
node_thread = threading.Thread(target=start_node, daemon=True)
node_thread.start()


class DashboardHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        metadata = node.get_metadata()
        resources = metadata.get("resources", {})

        status = "ONLINE" if metadata.get("running") else "OFFLINE"

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
                }}

                .container {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 20px;
                    margin-top: 30px;
                }}

                .card {{
                    background: #1e293b;
                    padding: 25px;
                    border-radius: 12px;
                    text-align: center;
                }}

                .value {{
                    font-size: 28px;
                    font-weight: bold;
                    margin-top: 10px;
                }}

                .online {{
                    color: #22c55e;
                }}

                .section {{
                    background: #1e293b;
                    margin-top: 30px;
                    padding: 25px;
                    border-radius: 12px;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}

                th, td {{
                    padding: 12px;
                    border-bottom: 1px solid #334155;
                    text-align: left;
                }}
            </style>
        </head>

        <body>

            <h1>MeshWeaver Monitoring Dashboard</h1>

            <div class="container">

                <div class="card">
                    <div>Total Nodes</div>
                    <div class="value">1</div>
                </div>

                <div class="card">
                    <div>Online Nodes</div>
                    <div class="value online">
                        {1 if metadata.get("running") else 0}
                    </div>
                </div>

                <div class="card">
                    <div>CPU Usage</div>
                    <div class="value">
                        {resources.get("cpu_percent", 0)}%
                    </div>
                </div>

                <div class="card">
                    <div>Memory Usage</div>
                    <div class="value">
                        {resources.get("memory_percent", 0)}%
                    </div>
                </div>

            </div>

            <div class="section">

                <h2>Node Information</h2>

                <table>
                    <tr>
                        <th>Node ID</th>
                        <td>{metadata.get("node_id")}</td>
                    </tr>

                    <tr>
                        <th>Host</th>
                        <td>{metadata.get("host")}</td>
                    </tr>

                    <tr>
                        <th>Port</th>
                        <td>{metadata.get("port")}</td>
                    </tr>

                    <tr>
                        <th>Status</th>
                        <td class="online">{status}</td>
                    </tr>

                    <tr>
                        <th>Peer Count</th>
                        <td>{metadata.get("peer_count", 0)}</td>
                    </tr>
                </table>

            </div>

            <div class="section">

                <h2>System Resources</h2>

                <p>
                    CPU Usage:
                    <b>{resources.get("cpu_percent", 0)}%</b>
                </p>

                <p>
                    Memory Usage:
                    <b>{resources.get("memory_percent", 0)}%</b>
                </p>

            </div>

        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write(html.encode("utf-8"))


def main():
    print("===================================")
    print("     MeshWeaver Dashboard")
    print("===================================")
    print("Dashboard: http://127.0.0.1:8000")
    print("Node:      127.0.0.1:9001")
    print("===================================")

    server = HTTPServer(("127.0.0.1", 8000), DashboardHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard...")
        node.stop()
        server.server_close()


if __name__ == "__main__":
    main()