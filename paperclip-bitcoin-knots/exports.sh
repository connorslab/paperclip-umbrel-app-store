#!/usr/bin/env bash
# Umbrel sources exports; preserve the caller's shell options.
export APP_PAPERCLIP_KNOTS_RPC_HOST="paperclip-bitcoin-knots_node_1"
export APP_PAPERCLIP_KNOTS_RPC_PORT="8332"
if [[ ! -f "${EXPORTS_APP_DIR}/.env" ]]; then
  (umask 077; printf 'export APP_PAPERCLIP_KNOTS_RPC_USER=umbrel\nexport APP_PAPERCLIP_KNOTS_RPC_PASS=%s\n' "$(openssl rand -hex 32)" > "${EXPORTS_APP_DIR}/.env")
fi
# shellcheck disable=SC1091
source "${EXPORTS_APP_DIR}/.env"
