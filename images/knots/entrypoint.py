import hashlib, hmac, os, pathlib, secrets, subprocess
p=pathlib.Path('/data/bitcoin.conf')
if not p.exists():
    p.write_text('server=1\ntxindex=0\ndisablewallet=1\nblockmaxweight=785000\nmaxmempool=1000\n')
if 'includeconf=rpc.conf' not in p.read_text().splitlines():
    with p.open('a') as f:
        f.write('\nincludeconf=rpc.conf\n')
user=os.environ['RPC_USER']; password=os.environ['RPC_PASSWORD']
if any(x in user+password for x in '\r\n'): raise ValueError('Invalid credentials')
secret=pathlib.Path('/data/rpc.conf')
salt=secrets.token_hex(16)
digest=hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()
# Keep cookie authentication for bitcoin-cli and hashed credentials for CONVOY.
secret.write_text('rpcauth='+user+':'+salt+'$'+digest+'\n')
secret.chmod(0o600)
subprocess.Popen(['python3','/opt/knots/status.py'])
os.execvp('bitcoind',['bitcoind','-datadir=/data','-chain=main','-server=1','-rpcbind=0.0.0.0','-rpcallowip=10.21.0.0/16','-rpcport=8332','-port=8333','-printtoconsole=1','-blocknotify=curl --max-time 3 -fsS http://blake2b-convoy-datum_gateway_1:7152/NOTIFY >/dev/null || true'])
