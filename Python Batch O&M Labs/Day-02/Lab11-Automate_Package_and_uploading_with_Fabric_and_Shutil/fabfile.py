from fabric import task
import os
import shutil

@task
def create_archive(c, source_dir, archive_name=None):
    """Creates a zip archive including the original folder."""
    folder_name = os.path.basename(source_dir.rstrip(os.sep))  # Ensure folder name is correct
    archive_name = archive_name or f"{folder_name}.zip"  # Name the archive based on the folder

    shutil.make_archive(folder_name, 'zip', root_dir=os.path.dirname(source_dir), base_dir=folder_name)
    print(f"Archive {archive_name} created successfully.")
    return archive_name

@task
def upload_and_extract(c, local_archive, remote_path):
    """Uploads the archive to a remote server and extracts it while preserving the folder name."""
    remote_archive = os.path.join(remote_path, os.path.basename(local_archive))
    
    print("Uploading archive...")
    c.put(local_archive, remote_archive)
    print(f"Archive uploaded to {remote_archive}")
    
    # Extract to remote_path while preserving the folder name
    print("Extracting archive...")
    c.run(f"unzip {remote_archive} -d {remote_path}")
    c.run(f"rm {remote_archive}")  # Optional: Remove the archive after extraction
    
    print(f"Extraction complete. Folder structure preserved under {remote_path}.")
    
@task
def package_and_deploy(c, source_dir, remote_path):
    """Packages, uploads, and extracts files on the remote server."""
    archive_name = create_archive(c, source_dir)
    upload_and_extract(c, archive_name, remote_path)
