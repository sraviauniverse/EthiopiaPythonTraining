
import pexpect

# Define variables
remote_host = "remote_host"
username = "user"
private_key_path = "~/.ssh/my_ssh_key"

# SSH command
ssh_command = f"ssh -i {private_key_path} {username}@{remote_host}"

# Spawn the SSH session
child = pexpect.spawn(ssh_command, timeout=30)

# Handle SSH prompts
try:
    child.expect("Are you sure you want to continue connecting (yes/no/[fingerprint])?")
    child.sendline("yes")
except pexpect.exceptions.TIMEOUT:
    pass

# Interact with the shell
child.interact()
