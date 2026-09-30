import json, pathlib, yaml
root=pathlib.Path('.')
for p in root.rglob('*.yml'): yaml.safe_load(p.read_text())
for p in root.rglob('*.json'): json.loads(p.read_text())
apps=sorted(p.parent.name for p in root.glob('*/umbrel-app.yml'))
assert apps==['paperclip-bitcoin-knots','paperclip-datum','paperclip-wallet']
for app in apps:
    m=yaml.safe_load((root/app/'umbrel-app.yml').read_text())
    assert m['id']==app and app.startswith('paperclip-')
    c=yaml.safe_load((root/app/'docker-compose.yml').read_text())
    for service in c['services'].values():
        assert not any('8332' in str(port) for port in service.get('ports',[]))
assert yaml.safe_load((root/apps[1]/'umbrel-app.yml').read_text())['dependencies']==[apps[0]]
print('YAML, JSON, IDs, dependency and RPC publication checks passed')
