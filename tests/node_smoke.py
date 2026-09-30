"""Mainnet wrapper startup on an isolated Docker network; no chain sync."""
import json
import subprocess
import sys
import time

arch = sys.argv[1]
name = 'knots-smoke-' + arch
def docker(*args):
    return subprocess.check_output(['docker', *args], text=True, stderr=subprocess.DEVNULL)

try:
    docker('run', '-d', '--name', name, '--platform', 'linux/'+arch,
           '--network', 'none', '--tmpfs', '/data:uid=1000,gid=1000',
           '-e', 'RPC_USER=smoke', '-e', 'RPC_PASSWORD=smoke-only-password', 'knots:test')
    for i in range(40):
        try:
            chain = json.loads(docker('exec', name, 'bitcoin-cli', '-datadir=/data', 'getblockchaininfo'))
            assert chain['chain'] == 'main'
            assert chain['blocks'] == 0
            break
        except subprocess.CalledProcessError:
            time.sleep(1)
    else:
        raise AssertionError('Knots wrapper did not start RPC')
    status = json.loads(docker('exec', name, 'curl', '-fsS', 'http://127.0.0.1:8080/'))
    assert status['getblockchaininfo']['chain'] == 'main'
    assert 'getdeploymentinfo' in status
    docker('exec', name, 'bitcoin-cli', '-datadir=/data', 'stop')
    print(arch + ': mainnet wrapper, generated RPC auth and status API passed on isolated network')
finally:
    subprocess.run(['docker', 'logs', name], check=False)
    subprocess.run(['docker', 'rm', '-f', name], check=False)
