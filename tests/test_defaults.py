import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('entrypoint', Path(__file__).resolve().parents[1] / 'images/convoy/runtime/entrypoint.py')
entrypoint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entrypoint)


class DefaultsTest(unittest.TestCase):
    def test_new_install_and_existing_owner_configuration(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict('os.environ', {}, clear=True):
            path = Path(directory) / 'config.json'
            config = entrypoint.configure(path)
            self.assertEqual(config['datum']['pool_host'], 'pool.paperclippool.xyz')
            self.assertEqual(config['datum']['pool_pubkey'], entrypoint.POOL_PUBLIC_KEY)
            self.assertTrue(config['datum']['pooled_mining_only'])
            self.assertEqual(config['mining']['pool_address'], '')
            config['datum']['pool_host'] = 'owner-selected.example'
            config['datum']['pooled_mining_only'] = False
            config['mining']['pool_address'] = 'owner-payout-preserved'
            config['mining']['coinbase_tag_primary'] = 'Owner'
            path.write_text(json.dumps(config))
            saved = entrypoint.configure(path)
            self.assertEqual(saved['datum'], config['datum'])
            self.assertEqual(saved['mining'], config['mining'])
            self.assertEqual(saved['api']['admin_password'], config['api']['admin_password'])
