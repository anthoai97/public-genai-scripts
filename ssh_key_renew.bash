#!/bin/bash
# Replace 'devuser' with your desired username

# Create user
useradd -m -s /bin/bash devuser

# Add user to sudoers
echo "devuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/devuser
chmod 440 /etc/sudoers.d/devuser

# Set up SSH
mkdir -p /home/devuser/.ssh
chmod 700 /home/devuser/.ssh

# Paste your public key below
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC..." > /home/devuser/.ssh/authorized_keys

chmod 600 /home/devuser/.ssh/authorized_keys
chown -R devuser:devuser /home/devuser/.ssh
