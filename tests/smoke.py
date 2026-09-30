"""Container startup without a synced node: checks configuration/API, not mining."""
import json
import subprocess
import sys
import time
import urllib.request

arch = sys.argv[1]
name = 'convoy-smoke-' + arch
def docker(*args):
    return subprocess.check_output(['docker', *args], text=True)

try:
    docker('run', '-d', '--name', name, '--platform', 'linux/'+arch,
           '--tmpfs', '/data:uid=1000,gid=1000', '-p', '127.0.0.1:17152:7152',
           '-e', 'RPC_URL=http://127.0.0.1:1', '-e', 'RPC_USER=smoke',
           '-e', 'RPC_PASSWORD=smoke', '-e', 'ADMIN_PASSWORD=smoke-test-only-password', 'convoy:test')
    for i in range(30):
        try:
            with urllib.request.urlopen('http://127.0.0.1:17152/', timeout=2) as r:
                assert r.status == 200
            break
        except Exception:
            time.sleep(1)
    else:
        raise AssertionError('CONVOY dashboard never became reachable')
    c = json.loads(docker('exec', name, 'cat', '/data/datum_gateway_config.json'))
    assert c['datum']['pool_host'] == 'pool.paperclippool.xyz' and c['datum']['pooled_mining_only'] is True
    assert len(c['datum']['pool_pubkey']) == 128
    assert c['mining']['pool_address'] == ''
    assert c['api']['listen_addr'] == '0.0.0.0' and c['stratum']['listen_port'] == 23334
    with urllib.request.urlopen('http://127.0.0.1:17152/NOTIFY', timeout=3) as r:
        assert r.status == 200
    print(arch + ': generated JSON, Paperclip defaults, dashboard HTTP and /NOTIFY passed; no live-node/ASIC test')
finally:
    subprocess.run(['docker', 'logs', name], check=False)
    subprocess.run(['docker', 'rm', '-f', name], check=False)
