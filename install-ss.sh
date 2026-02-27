#!/bin/bash
set -e

# Install Shadowsocks
sudo apt-get update
sudo apt-get install -y shadowsocks-libev

# Generate a random password
SS_PASS=$(openssl rand -base64 16)

# Create Shadowsocks config
sudo tee /etc/shadowsocks-libev/config.json > /dev/null << EOF
{
    "server": "0.0.0.0",
    "server_port": 8388,
    "password": "${SS_PASS}",
    "timeout": 300,
    "method": "aes-256-gcm",
    "fast_open": true,
    "mode": "tcp_and_udp"
}
EOF

# Enable and start
sudo systemctl enable shadowsocks-libev
sudo systemctl restart shadowsocks-libev

echo "===STATUS==="
sudo systemctl status shadowsocks-libev --no-pager
echo "===PASSWORD==="
echo "$SS_PASS"
echo "===DONE==="
