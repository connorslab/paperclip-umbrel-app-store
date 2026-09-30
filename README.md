# Paperclip community store

Add https://github.com/connorslab/paperclip-umbrel-app-store in Umbrel’s Community App Stores.

- **Bitcoin Knots BLAKE2b**: XBT Knots 29.4.2, local block templates and private RPC.
- **Paperclip DATUM**: CONVOY-based XBT gateway, branded for Paperclip and preset to Paperclip Pool. Set your own payout address. Existing saved pool and payout settings are preserved.
- **Paperclip Wallet Beta**: on-chain, Ark and Lightning wallet preset to https://ark.paperclippool.xyz, with automatic VTXO maintenance and a bundled optional pruned-node adapter. Production ASP deposits remain closed.

All apps appear under Bitcoin. Mining images passed amd64 and arm64 builds, upstream tests, and startup/API checks. Wallet images passed startup checks on both architectures. App and image versions are pinned in each Compose file.

The public mining app IDs are `paperclip-bitcoin-knots` and `paperclip-datum`. They are separate from older `blake2b-*` installations. Installing them does not migrate existing node data or gateway settings. Do not run duplicate gateways on port 23334 or duplicate nodes on port 8333; migration needs an explicit backup and data transfer.

DATUM defaults to `pool.paperclippool.xyz:28915` with its verified public key, pooled-only mode, and no operator payout address. Keep miner traffic private. RPC credentials are generated locally and are not published to host ports.

See each app’s instructions and `upstream.json` for provenance. Mining source/build wrappers are included under `images/`; upstream consensus and mining protocol code remain intact, with Paperclip presentation changes applied before gateway compilation. MIT attribution is preserved in `LICENSE` and `NOTICE.md`.
