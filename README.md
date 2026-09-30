# Paperclip Beta — Umbrel Community Store

Self-hosted Bitcoin Blake2b (XBT) wallet apps. Add this repository URL through
Umbrel App Store → Community App Stores:

https://github.com/connorslab/paperclip-umbrel-app-store

Paperclip Wallet defaults to https://ark.paperclippool.xyz. The production Ark
server is preparing for launch: do not fund a wallet for it yet.

The wallet includes on-chain, Ark, and server-backed Lightning, automatic VTXO
refresh while online, a branded icon, and an optional private pruned-node adapter.
Keys remain local. An XBT blockchain connection and complete wallet backups are
required. SHA-256 BTC nodes are incompatible.

The image is pinned by digest and built for amd64 and arm64. Package startup,
upgrade, and restore acceptance tests are distinct from image build checks.

See paperclip-wallet/INSTRUCTIONS.md and paperclip-wallet/BUNDLED-PRUNED.md.
Use port 38180; remove or move a conflicting legacy test app before installation.

Source: https://github.com/connorslab/paperclip-wallet-app
