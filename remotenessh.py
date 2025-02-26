#!/usr/bin/env python3
import sys
import re
import os
import subprocess

def validate_port(port: str):
    return re.fullmatch(r"[1-9]\d{0,4}", port) and (1 <= int(port) <= 65535)

def check_args(local_port: str, ip: str, remote_port: str):
    if not re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", ip) or any(not (0 <= int(o) <= 255) for o in ip.split(".")):
        sys.exit(f"[-] Error: '{ip}' is not a valid IPv4 address. (0-255.0-255.0-255.0-255)")

    if not validate_port(local_port):
        sys.exit(f"[-] Error: '{local_port}' is not a valid local port. (1-65535)")

    if not validate_port(remote_port):
        sys.exit(f"[-] Error: '{remote_port}' is not a valid remote port. (1-65535)")

    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(f"[!] Usage: python3 {sys.argv[0]} <Local_port> <Server_IPv4> <Remote_server_port>")

    check = check_args(sys.argv[1], sys.argv[2], sys.argv[3])
    if check:
        local_port = sys.argv[1]
        remote_ip = sys.argv[2]
        remote_port = sys.argv[3]
        service_name = f"remotenessh-{local_port}-{remote_ip}-{remote_port}"
        new_script_fullpath = f"/usr/bin/{service_name}.sh"
        new_service_fullpath = f"/etc/systemd/system/{service_name}.service"

        print(f"[+] Valid IP and ports: {local_port}:{remote_ip}:{remote_port}")

        # check if the service file already exists
        if os.path.isfile(new_service_fullpath):
            sys.exit(f"Error: The systemd service file '{new_service_fullpath}' already exists.")
        
        # content of the script to be executed via systemd
        script_content = [
            "#!/usr/bin/env bash",
            f"ssh -o StrictHostKeyChecking=accept-new root@{remote_ip} -N -R 127.0.0.1:{remote_port}:127.0.0.1:{local_port}"
        ]
        # content of the systemd service that executes the script
        service_content = [
            "[Unit]",
            f"Description=SSH reverse tunnel of localhost:{local_port} to {remote_ip}:{remote_port} (by remotenessh.py)",
            "After=network.target",
            "StartLimitIntervalSec=0",
            "[Service]",
            "Type=simple",
            "Restart=always",
            "RestartSec=3",
            "User=root",
            f"ExecStart={new_script_fullpath}",
            "[Install]",
            "WantedBy=multi-user.target"
        ]
        # write the service file with read permission
        with open(new_service_fullpath, "w") as f:
            f.write('\n'.join(service_content))
        os.chmod(new_service_fullpath, 0o644)
        # write the script with execution permission
        with open(new_script_fullpath, "w") as f:
            f.write('\n'.join(script_content))
        os.chmod(new_script_fullpath, 0o755)

        print(f"[+] Systemd service file created at '{new_service_fullpath}'")
        print(f"[+] Execution script created at '{new_script_fullpath}'")
        print(f"[!] Activating service via systemd...\n")

        try:
            # Reload systemd daemons
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            # Enable and start the service
            subprocess.run(["systemctl", "enable", "--now", f"{service_name}.service"], check=True)

            print(f"[+] Service {service_name}.service configured, enabled, and started successfully.")
            print(f"[+] Check the service status with the following command: systemctl status {service_name}")

        except subprocess.CalledProcessError as e:
            print(f"[-] Error executing command: {e}")
