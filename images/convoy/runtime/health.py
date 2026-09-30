import base64, json, socket, sys, urllib.request

def check(c):
    b = c['bitcoind']
    if b.get('rpccookiefile'):
        with open(b['rpccookiefile']) as f: auth = f.read().strip()
    else:
        auth = b['rpcuser'] + ':' + b['rpcpassword']
    request = urllib.request.Request(b['rpcurl'], json.dumps({'jsonrpc':'1.0','id':'health','method':'getblocktemplate','params':[{'rules':['segwit','blake2b']}]}).encode(), {'Authorization':'Basic '+base64.b64encode(auth.encode()).decode(), 'Content-Type':'application/json'})
    with urllib.request.urlopen(request, timeout=10) as r: result = json.load(r)
    if result.get('error'): raise RuntimeError(str(result['error']))
    if '!blake2b' not in result['result'].get('rules', []):
        raise RuntimeError('Bitcoin template lacks !blake2b. Use a synchronized BLAKE2b-capable Knots node with BLAKE2b active.')

if __name__ == '__main__':
    try:
        with open('/data/datum_gateway_config.json') as f: check(json.load(f))
        for port in (7152, 23334):
            with socket.create_connection(('127.0.0.1', port), 3): pass
        with urllib.request.urlopen('http://127.0.0.1:7152/', timeout=3) as r:
            if r.status != 200: raise RuntimeError('Dashboard unavailable')
        print('BLAKE2b RPC, dashboard and Stratum healthy')
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
