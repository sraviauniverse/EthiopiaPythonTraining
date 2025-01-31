import asyncio
import pexpect
import nest_asyncio

async def ssh_connect(host, username, password):
    """Connect to a remote host via SSH using pexpect and handle unknown host key prompt."""
    ssh_command = f"ssh {username}@{host}"
    child = pexpect.spawn(ssh_command, timeout=None)
    try:
        index = child.expect(["Are you sure you want to continue connecting", "password:", pexpect.EOF, pexpect.TIMEOUT], timeout=10)
        if index == 0:
            child.sendline("yes")
            child.expect("password:")
            child.sendline(password)
        elif index == 1:
            child.sendline(password)
        child.expect("[$#>] ", timeout=None)
        return child
    except pexpect.exceptions.TIMEOUT:
        print("Connection timed out.")
        return None

async def install_package(child, package_name, sudo_password):
    """Install a package on the remote machine."""
    command = f"echo {sudo_password} | sudo -S apt-get install -y {package_name}"
    child.sendline(command)
    try:
        index = child.expect(["Do you want to continue? [Y/n]", "password for", "[$#>] "], timeout=None)
        if index == 0:
            child.sendline("Y")  # Confirm installation
            child.expect("[$#>] ", timeout=None)  # Wait for prompt again
        elif index == 1:
            child.sendline(sudo_password)  # Send sudo password
            child.expect("[$#>] ", timeout=None)  # Wait for prompt again
        print(f"Installed {package_name} on the remote machine.")
    except pexpect.exceptions.TIMEOUT:
        print(f"Timeout while installing {package_name}. Check network or try again.")

async def main():
    host = input("Enter the remote host IP or domain: ")
    username = input("Enter the SSH username: ")
    password = input("Enter the SSH password: ")
    sudo_password = input("Enter the sudo password: ")
    
    child = await ssh_connect(host, username, password)
    if child is None:
        return
    
    package_name = input("Enter the package name to install: ")
    await install_package(child, package_name, sudo_password)
    
    child.sendline("exit")
    child.close()

if __name__ == "__main__":
    nest_asyncio.apply()  # Apply nest_asyncio patch
    asyncio.run(main())
