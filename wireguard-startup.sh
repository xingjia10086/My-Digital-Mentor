#!/bin/bash
set -e

# Update system
apt-get update
apt-get install -y wireguard qrencode

# Enable IP forwarding
echo "net.ipv4.ip_forward = 1" > /etc/sysctl.d/99-wireguard.conf
sysctl -p /etc/sysctl.d/99-wireguard.conf

# Generate server keys
cd /etc/wireguard
umask 077

if [ ! -f server_private.key ]; then
    wg genkey | tee server_private.key | wg pubkey > server_public.key
    wg genkey | tee client_private.key | wg pubkey > client_public.key
fi

SERVER_PRIVATE=$(cat server_private.key)
SERVER_PUBLIC=$(cat server_public.key)
CLIENT_PRIVATE=$(cat client_private.key)
CLIENT_PUBLIC=$(cat client_public.key)

# Get the main network interface
MAIN_IFACE=$(ip route show default | awk '{print $5}' | head -1)

# Create server config
cat > /etc/wireguard/wg0.conf << EOF
[Interface]
PrivateKey = ${SERVER_PRIVATE}
Address = 10.66.66.1/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o ${MAIN_IFACE} -j MASQUERADE; iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o ${MAIN_IFACE} -j MASQUERADE; iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT
DNS = 8.8.8.8, 8.8.4.4

[Peer]
PublicKey = ${CLIENT_PUBLIC}
AllowedIPs = 10.66.66.2/32
EOF

# Create client config for reference
EXTERNAL_IP=$(curl -s http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip -H "Metadata-Flavor: Google")

cat > /etc/wireguard/client.conf << EOF
[Interface]
PrivateKey = ${CLIENT_PRIVATE}
Address = 10.66.66.2/24
DNS = 8.8.8.8, 8.8.4.4

[Peer]
PublicKey = ${SERVER_PUBLIC}
Endpoint = ${EXTERNAL_IP}:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
EOF

# Enable and start WireGuard
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0

echo "WireGuard setup complete!" > /tmp/wireguard-setup-done
