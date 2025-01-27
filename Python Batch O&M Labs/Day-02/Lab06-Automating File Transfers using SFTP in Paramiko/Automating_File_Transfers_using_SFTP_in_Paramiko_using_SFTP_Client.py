import paramiko

def sftp_file_transfer_with_component(hostname, port, username, password, local_file_path, remote_file_path, mode="upload"):
    try:
        # Initialize Transport object
        print(f"Connecting to {hostname} via SFTP...")
        transport = paramiko.Transport((hostname, port))
        
        # Authenticate with username and password
        transport.connect(username=username, password=password)
        print(f"Connected to {hostname}!")

        # Initialize the SFTP client
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        if mode == "upload":
            # Upload the file
            print(f"Uploading {local_file_path} to {remote_file_path}...")
            sftp.put(local_file_path, remote_file_path)
            print("File uploaded successfully.")
        elif mode == "download":
            # Download the file
            print(f"Downloading {remote_file_path} to {local_file_path}...")
            sftp.get(remote_file_path, local_file_path)
            print("File downloaded successfully.")
        else:
            print("Invalid mode! Use 'upload' or 'download'.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the SFTP session and Transport connection
        if 'sftp' in locals():
            sftp.close()
            print("SFTP session closed.")
        if 'transport' in locals():
            transport.close()
            print("SFTP connection closed.")

if __name__ == "__main__":
    # Replace these with your remote host details
    hostname = "192.168.1.166"  # Remote host's IP or domain
    port = 22                             # Default SFTP/SSH port
    username = "rps"            # Your username
    password = "rps@123"            # Your password

    # File paths
    local_file_path = "/home/rps/samplefile.txt"  # Local file path
    remote_file_path = "/home/rps/secondfiletransferred.txt"  # Remote file path

    # Choose operation mode: "upload" or "download"
    mode = "upload"  # Change to "download" to fetch files from the remote server

    # Automate file transfer using SFTP component
    sftp_file_transfer_with_component(hostname, port, username, password, local_file_path, remote_file_path, mode)
