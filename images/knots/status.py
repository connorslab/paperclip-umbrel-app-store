import http.server, json, subprocess
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        data={}
        for method in ['getblockchaininfo','getdeploymentinfo']:
            p=subprocess.run(['bitcoin-cli','-datadir=/data',method],capture_output=True,text=True,timeout=15)
            try: data[method]=json.loads(p.stdout)
            except ValueError: data[method]={'status':'Node starting or RPC unavailable'}
        self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers()
        self.wfile.write(json.dumps(data,indent=2).encode())
http.server.HTTPServer(('0.0.0.0',8080),Handler).serve_forever()
