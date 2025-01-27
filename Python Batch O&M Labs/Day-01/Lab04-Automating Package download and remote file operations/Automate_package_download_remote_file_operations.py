import pexpect

def ssh_connect(host, username, password):
    """Connect to a remote host via SSH using pexpect."""
    ssh_command = f"ssh {username}@{host}"
    child = pexpect.spawn(ssh_command)

    # Handle password prompt
    try:
        child.expect("password:")
        child.sendline(password)
        child.expect("[$#>] ")  # Wait for shell prompt
    except pexpect.exceptions.TIMEOUT:
        print("Connection timed out.")
        return None
    
    return child

def install_package(child, package_name):
    """Install a package on the remote machine using a package manager."""
    command = f"sudo apt-get install -y {package_name}"
    child.sendline(command)
    child.expect("password for")  # Sudo password prompt
    sudo_password = input("Enter sudo password: ")
    child.sendline(sudo_password)
    child.expect("[$#>] ")  # Wait for shell prompt
    print(f"Installed {package_name} on the remote machine.")

def upload_file(child, local_path, remote_path):
    """Upload a file to the remote machine using scp."""
    scp_command = f"scp {local_path} {child.before.decode().strip()}:{remote_path}"
    scp_child = pexpect.spawn(scp_command)

    # Handle password prompt
    try:
        scp_child.expect("password:")
        scp_child.sendline(password)
        scp_child.expect(pexpect.EOF)
        print(f"Uploaded {local_path} to {remote_path}.")
    except pexpect.exceptions.TIMEOUT:
        print("SCP operation timed out.")


def download_file(child, remote_path, local_path):
    """Download a file from the remote machine using scp."""
    scp_command = f"scp {child.before.decode().strip()}:{remote_path} {local_path}"
    scp_child = pexpect.spawn(scp_command)

    # Handle password prompt
    try:
        scp_child.expect("password:")
        scp_child.sendline(password)
        scp_child.expect(pexpect.EOF)
        print(f"Downloaded {remote_path} to {local_path}.")
    except pexpect.exceptions.TIMEOUT:
        print("SCP operation timed out.")

def run_remote_command(child, command):
    """Run a command on the remote machine."""
    child.sendline(command)
    child.expect("[$#>] ")  # Wait for shell prompt
    print(child.before.decode().strip())

def main():
    host = input("Enter the remote host IP or domain: ")
    username = input("Enter the SSH username: ")
    password = input("Enter the SSH password: ")

    # Connect to the remote host
    child = ssh_connect(host, username, password)
    if child is None:
        return

    # Example operations
    package_name = input("Enter the package name to install: ")
    install_package(child, package_name)

    local_file = input("Enter the local file path to upload: ")
    remote_file = input("Enter the remote file path: ")
    upload_file(child, local_file, remote_file)

    remote_file_to_download = input("Enter the remote file path to download: ")
    local_file_save_path = input("Enter the local path to save the file: ")
    download_file(child, remote_file_to_download, local_file_save_path)

    command = input("Enter a command to run on the remote machine: ")
    run_remote_command(child, command)

    # Exit SSH
    child.sendline("exit")
    child.close()

if __name__ == "__main__":
    main()
