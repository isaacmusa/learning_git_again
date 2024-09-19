#!/usr/bin/env python3


import telnetlib
import time

# Function to send commands and read response
def send_command(tn, command, wait_time=1):
    tn.write(command.encode('ascii') + b'\n')
    time.sleep(wait_time)
    output = tn.read_very_eager().decode('ascii')
    print(output)
    return output

# Function to handle the full Telnet session
def telnet_session(hostname, username, password, commands):
    tn = telnetlib.Telnet(hostname)

    # Login sequence
    tn.read_until(b"Username: ")
    tn.write(username.encode('ascii') + b"\n")

    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

    # Handle password change prompt
    if b"Change now? [Y/N]:" in tn.read_until(b"Change now? [Y/N]: "):
        tn.write(b"n\n")

    for command in commands:
        send_command(tn, command)

    tn.close()

# Example of telnet workflow
def main():
    # Define the commands to send
    commands_isis = ["dis isis pe", "tracert 10.98.70.11"]

    # Start telnet session for each device
    print("Connecting to 10.98.12.10")
    telnet_session("10.98.12.10", "huawei2", "DCNglo@!!123", commands_isis)

    print("Connecting to 10.98.65.246")
    telnet_session("10.98.65.246", "kano_dcn", "Admin123,.", commands_isis)

    print("Connecting to 10.98.23.24")
    telnet_session("10.98.23.24", "huawei2", "DCNglo@!!123", ["dis isis pe ve", "tracert 10.98.70.11"])

if __name__ == "__main__":
    main()
