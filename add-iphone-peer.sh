#!/bin/bash
set -e

# Generate iPhone keys
sudo bash -c 'cd /etc/wireguard && wg genkey | tee iphone_private.key | wg pubkey > iphone_public.key'

IPHONE_PRIV=$(sudo cat /etc/wireguard/iphone_private.key)
IPHONE_PUB=$(sudo cat /etc/wireguard/iphone_public.key)
SERVER_PUB=$(sudo cat /etc/wireguard/server_public.key)

# Add iPhone peer to server config
echo "" | sudo tee -a /etc/wireguard/wg0.conf > /dev/null
echo "[Peer]" | sudo tee -a /etc/wireguard/wg0.conf > /dev/null
echo "PublicKey = $IPHONE_PUB" | sudo tee -a /etc/wireguard/wg0.conf > /dev/null
echo "AllowedIPs = 10.66.66.3/32" | sudo tee -a /etc/wireguard/wg0.conf > /dev/null

# Add peer to running WireGuard
sudo wg set wg0 peer "$IPHONE_PUB" allowed-ips 10.66.66.3/32

echo "===IPHONE_PRIVATE_KEY==="
echo "$IPHONE_PRIV"
echo "===IPHONE_PUBLIC_KEY==="
echo "$IPHONE_PUB"
echo "===SERVER_PUBLIC_KEY==="
echo "$SERVER_PUB"
echo "===WG_SHOW==="
sudo wg show
echo "===DONE==="
