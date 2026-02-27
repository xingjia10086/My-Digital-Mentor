#!/bin/bash
set -ex

# Stop any existing wg0
sudo wg-quick down wg0 2>/dev/null || true
sudo ip link delete wg0 2>/dev/null || true

# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/99-wireguard.conf

# Read keys
SERVER_PRIVATE=$(sudo cat /etc/wireguard/server_private.key)
CLIENT_PUBLIC=$(sudo cat /etc/wireguard/client_public.key)

# Write clean server config
sudo tee /etc/wireguard/wg0.conf > /dev/null << EOF
[Interface]
PrivateKey = ${SERVER_PRIVATE}
Address = 10.66.66.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ens4 -j MASQUERADE; iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o ens4 -j MASQUERADE; iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT

[Peer]
PublicKey = ${CLIENT_PUBLIC}
AllowedIPs = 10.66.66.2/32
EOF

sudo chmod 600 /etc/wireguard/wg0.conf

# Start WireGuard
sudo systemctl restart wg-quick@wg0
sudo systemctl enable wg-quick@wg0

echo "===STATUS==="
sudo systemctl status wg-quick@wg0 --no-pager
echo "===WG==="
sudo wg show
echo "===DONE==="
