"""Health contract tests: mock RPC only, never a claim of live chain validation."""
import importlib.util
import io
import json
import pathlib
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ('images/convoy/runtime' if (ROOT / 'images').exists() else 'runtime')
spec = importlib.util.spec_from_file_location('health', RUNTIME / 'health.py')
health = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health)


class HealthTests(unittest.TestCase):
    def check_result(self, result):
        config = {'bitcoind': {'rpcurl': 'http://test.invalid:8332', 'rpcuser': 'test', 'rpcpassword': 'test'}}
        with patch('urllib.request.urlopen', return_value=io.BytesIO(json.dumps(result).encode())) as request:
            health.check(config)
            payload = json.loads(request.call_args.args[0].data)
            self.assertEqual(payload['params'], [{'rules': ['segwit', 'blake2b']}])

    def test_blake2b_template(self):
        self.check_result({'result': {'rules': ['segwit', '!blake2b']}, 'error': None})

    def test_sha256_template_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'lacks !blake2b'):
            self.check_result({'result': {'rules': ['segwit']}, 'error': None})

    def test_initial_download_rejected(self):
        with self.assertRaises(RuntimeError):
            self.check_result({'result': None, 'error': {'code': -10, 'message': 'Initial download'}})

    def test_network_failure_rejected(self):
        with patch('urllib.request.urlopen', side_effect=TimeoutError('unreachable')):
            with self.assertRaises(TimeoutError):
                health.check({'bitcoind': {'rpcurl': 'http://test.invalid', 'rpcuser': 'test', 'rpcpassword': 'test'}})


if __name__ == '__main__':
    unittest.main()
