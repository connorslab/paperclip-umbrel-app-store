# Paperclip community store

Add https://github.com/connorslab/paperclip-umbrel-app-store in Umbrel’s Community App Stores.

- **Paperclip DATUM**: CONVOY-based XBT gateway, branded for Paperclip and preset to Paperclip Pool. Set your own payout address. Existing saved pool and payout settings are preserved.
- **Paperclip Wallet Beta**: on-chain, Ark and Lightning wallet preset to https://ark.paperclippool.xyz, with automatic VTXO maintenance and a bundled optional pruned-node adapter. The production Ark server is open in beta; check live status before funding.

All apps appear under Bitcoin. Mining images passed amd64 and arm64 builds, upstream tests, and startup/API checks. Wallet images passed startup checks on both architectures. App and image versions are pinned in each Compose file.

Install a Blake2b Knots node from [Retropex](https://github.com/Retropex/Bitcoin-store) (`btc-bitcoinknots`) or [PaulsCode](https://github.com/paulscode/umbrel-store) (`paulscode-knots-blake2b`). DATUM uses Umbrel's Bitcoin provider selection and inherits that node's RPC host, port and credentials. Select the Blake2b node, not a SHA-256 Bitcoin node.

The former `paperclip-bitcoin-knots` app is no longer offered in this catalog. This does not uninstall an existing node or move its data. Back up and explicitly migrate an existing installation before selecting its replacement. Do not run duplicate gateways on port 23334. Existing wallet connections remain saved separately; never uninstall a node that still serves a wallet.

DATUM defaults to `pool.paperclippool.xyz:28915` with its verified public key, pooled-only mode, and no operator payout address. Keep miner traffic private. RPC credentials are generated locally and are not published to host ports.

See each app’s instructions and `upstream.json` for provenance. Mining source/build wrappers are included under `images/`; upstream consensus and mining protocol code remain intact, with Paperclip presentation changes applied before gateway compilation. MIT attribution is preserved in `LICENSE` and `NOTICE.md`.


## Wallet 0.9.0

Ordinary single-input Ark sends allocate 1,056 sats without change or 1,584 sats
with change for recovery on compatible servers, about 60% less than 0.8.3.
Lightning and tree recovery budgets are unchanged. The browser adds payment
review, clearer status and connection settings, and smoother navigation.

The wallet accepts the selected node's standard RPC exports when Umbrel supplies
them. If no installed node connection appears during setup, enter the RPC details
from your Retropex or PaulsCode Blake2b node. Manual and remote-node connections
remain supported. Installing a local node is not required to update an existing
wallet. Saved wallet connections are never silently replaced.

Back up the complete wallet before updating. The image is pinned by digest.
Removing the old Knots catalog entry does not uninstall a node or remove its data.

## 0.9.1 setup hotfix

Fixes new-wallet ASP defaults and setup layout. Paperclip is prefilled, configured custom servers are respected, and switching node modes preserves edits. Checkboxes and action buttons now have separate layouts. Existing wallet data, recovery formats, and fees are unchanged. Update in place after backing up the complete wallet.

## Wallet 0.9.2

Sign-in stays responsive while the node is syncing or unavailable. Use the app
password shown by Umbrel. Balances and activity can load independently, with
clear messages when data is unavailable. Dedicated transaction result screens
distinguish completion, failure, pending confirmation, and unknown outcomes.
Interrupted payments are never automatically resent. Existing wallet data,
authentication, connection settings, fees, and recovery formats are preserved.

## Wallet 0.9.3

Fixes blockchain RPC connections that could remain stuck after a canceled request or a closed server connection, leaving Ark balances unavailable. Connections can recover without restarting the wallet. Existing keys, authentication, settings, fees, recovery data, and older-client compatibility are unchanged. Interrupted payments are not automatically retried. Back up the complete wallet before updating.
