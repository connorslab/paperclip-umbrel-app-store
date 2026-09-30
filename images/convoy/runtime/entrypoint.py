import json, os, pathlib, secrets

POOL_PUBLIC_KEY = 'eb9c7885044ca6dc7a4af3761cb739cbf88e88f6852e6c4b4f754710ec0cc8c9fb4a78cb35bbfe6ac4ec83feb0030e5e8ac065baf87d9ab21489011f3d865478'

def configure(p=pathlib.Path('/data/datum_gateway_config.json')):
    if p.exists():
        c = json.loads(p.read_text())
    else:
        c = {'mining': {'pool_address': '', 'coinbase_tag_primary': 'PaperclipPool', 'coinbase_tag_secondary': 'Home miner', 'abw_verify_all_shares_on_disclosure': True}, 'datum': {'pool_host': 'pool.paperclippool.xyz', 'pool_port': 28915, 'pool_pubkey': POOL_PUBLIC_KEY, 'pooled_mining_only': True, 'pool_pass_full_users': True}, 'api': {'admin_password': os.environ.get('ADMIN_PASSWORD') or secrets.token_urlsafe(32), 'modify_conf': True}}
    if os.environ.get('RPC_URL'):
        c['bitcoind'] = {'rpcurl': os.environ['RPC_URL'], 'rpcuser': os.environ['RPC_USER'], 'rpcpassword': os.environ['RPC_PASSWORD'], 'notify_fallback': False}
    c.setdefault('stratum', {}).update(listen_addr='0.0.0.0', listen_port=23334)
    c.setdefault('api', {}).update(listen_addr='0.0.0.0', listen_port=7152)
    c['logger'] = {'log_to_console': True, 'log_to_file': False}
    if not c['api'].get('admin_password'):
        raise ValueError('An admin password is required')
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(c, indent=2) + '\n')
    tmp.chmod(0o600)
    tmp.replace(p)
    return c

if __name__ == '__main__':
    configure()
    os.execvp('datum_gateway', ['datum_gateway', '-c', '/data/datum_gateway_config.json'])
