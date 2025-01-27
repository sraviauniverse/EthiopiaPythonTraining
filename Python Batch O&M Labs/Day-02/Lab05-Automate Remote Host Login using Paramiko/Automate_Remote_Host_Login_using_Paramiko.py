import paramiko
import time

def connect_to_remote_host(hostname, port, username, password):
    try:
        # Initialize SSH client
        ssh_client = paramiko.SSHClient()
        
        # Automatically add the host key if it's not already in known_hosts
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the remote host
        print(f"Connecting to {hostname}...")
        ssh_client.connect(hostname, port=port, username=username, password=password)
        print(f"Connected to {hostname}!")
        
        # Open an interactive shell session
        shell = ssh_client.invoke_shell()
        print("Interactive shell started. You can now run commands on the remote host.")
        return ssh_client, shell

    except Exception as e:
        print(f"An error occurred during connection: {e}")
        return None, None

def interact_with_remote(shell):
    try:
        while True:
            # Prompt the user for commands to execute on the remote host
            command = input("Enter command to execute (or type 'exit' to quit): ").strip()
            if command.lower() == 'exit':
                print("Exiting interactive shell...")
                break
            
            # Send the command to the remote shell
            shell.send(command + '\n')
            
            # Wait for the command to execute
            time.sleep(1)
            
            # Read all available output
            output = ""
            while shell.recv_ready():
                output += shell.recv(1024).decode()

            # Display the command output
            print(output)
    except KeyboardInterrupt:
        print("\nExiting interactive session...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace these with your remote host details
    hostname = "192.168.1.166"  # Remote host's IP or domain
    port = 22                             # Default SSH port
    username = "rps"            # Your username
    password = "rps@123"            # Your password

    # Connect to the remote host and start the interactive shell
    ssh_client, shell = connect_to_remote_host(hostname, port, username, password)

    if ssh_client and shell:
        # Interact with the remote host
        interact_with_remote(shell)
        
        # Close the connection after the session
        ssh_client.close()
        print("Connection closed.")
