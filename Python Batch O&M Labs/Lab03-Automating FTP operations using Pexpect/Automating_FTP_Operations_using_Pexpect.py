import pexpect

def ftp_automation(host, username, password, commands):
    try:
        # Spawn the FTP session
        ftp_command = f"ftp {host}"
        print(f"Connecting to FTP server: {host}")
        child = pexpect.spawn(ftp_command, timeout=30)
        
        # Handle login prompts
        child.expect("Name .*:")  # Match the prompt for username
        child.sendline(username)
        child.expect("Password:")  # Match the prompt for password
        child.sendline(password)
        
        # Check if login was successful
        index = child.expect(["ftp>", "Login incorrect", pexpect.EOF, pexpect.TIMEOUT])
        if index == 1:
            print("Login failed. Please check your username or password.")
            return
        elif index in [2, 3]:
            print("Error: Connection failed.")
            return
        
        print("Login successful. Executing commands...")
        
        # Execute each command
        for command in commands:
            print(f"Executing: {command}")
            child.sendline(command)
            child.expect("ftp>")
            output = child.before.decode()
            print(f"Output:\n{output}")
        
        # Close the FTP session
        child.sendline("bye")
        child.expect(pexpect.EOF)
        print("FTP session closed.")
        
    except pexpect.exceptions.TIMEOUT:
        print("Error: Operation timed out.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace with your FTP server details and commands
    ftp_host = "ftp_host_ip_address"
    ftp_username = "username"
    ftp_password = "Password"
    
    # List of commands to execute
    ftp_commands = [
        "ls",  # List files in the current directory
        "cd files",  # Change to the 'files' directory
        "put localfile.txt",  # Upload a file, Replace the filename with your file
        "get remotefile.txt",  # Download a file, Replace the filename with the file that is in your ftp server
        "pwd",  # Print working directory
    ]
    
    # Automate the FTP operations
    ftp_automation(ftp_host, ftp_username, ftp_password, ftp_commands)

