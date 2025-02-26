# Remotenessh

## Overview
**Remotenessh** is a lightweight, python fully built-in cybersecurity tool designed to create `encrypted SSH reverse tunnels` as a `systemd services`, enabling persistent port sharing without the need for NAT or routers/firewalls network configurations.

Remotenessh uses SSH key-based authentication to establish secure connections with remote servers. Whether for port forwarding in `WAN environments` or within local `LAN networks`, this tool offers a flexible and minimalistic solution for secure port forwarding.

## Features
- **Encrypted SSH Tunneling:** Uses SSH reverse tunnels to securely forward ports.
- **No Need for NATs:** Eliminates the need for NAT configurations or complex network reconfigurations.
- **Native Python:** No external dependencies – uses only Python’s standard libraries.
- **systemd Integration:** Automatically creates and configures a systemd service for persistent tunnel management.
- **Flexible Deployment:** Works in both WAN environments (via VPS) and LAN networks.

## Requirements
- Python 3.x
- A Unix-based operating system with systemd support
- SSH access to the remote server (configured with asymmetric key authentication)
- Root privileges for service installation

## Installation & Configuration
1. **Prerequisites:**  
   Ensure that SSH key-based authentication is configured on the remote server.

2. **Execution:**  

   Run the [`remotenessh.py`](remotenessh.py) script with the following syntax:

   ```bash
   python3 remotenessh.py <Local_Port> <Server_IP> <Remote_Port>
   ```

   **Example:**

   ```bash
   python3 remotenessh.py 8080 150.136.85.87 9090
   ```

   The above command creates a systemd service called **`remotenessh-8080-150.136.85.87-9090`** that establishes an SSH reverse tunnel from your local host on port `8080` to the remote server’s localhost **(127.0.0.1)** on port `9090`.

   <p align="center">
     <img alt="Remotenessh" src="https://i.imgur.com/WRxP7DF.png" title="Remotenessh" width="70%">
   </p>

3. **systemd Integration:**  
   The script will perform the following actions:
   - Validate the parameters (IPv4 addresses and port ranges).
   - Generate a bash script in `/usr/bin/` that executes the SSH reverse tunnel command.
   - Create a corresponding systemd service file in `/etc/systemd/system/`.
   - Reload the systemd daemon and automatically enable/start the service.

4. **Service Management:**  
   To check the status or manage the service, use standard systemd commands:

   To check the service status:
   ```bash
   systemctl status remotenessh-<Local_Port>-<Server_IP>-<Remote_Port>.service
   ```   
   To view the service logs and debug information:
   ```bash
   journalctl -u remotenessh-<Local_Port>-<Server_IP>-<Remote_Port>.service
   ```
   To view the service configuration file:
   ```bash
   systemctl cat remotenessh-<Local_Port>-<Server_IP>-<Remote_Port>.service
   ```
   
   Replace the placeholders with the values used.

## Technical Details
- **Validation:**  
  The script uses regular expressions to ensure that the provided IP addresses and local and remote port numbers are valid.
  
- **Service Creation:**  
  A custom systemd service is generated that executes a bash script to establish the SSH tunnel. The service is configured to automatically restart in case of failures.

## License
Distributed under the MIT License. See the `LICENSE` file for more information.