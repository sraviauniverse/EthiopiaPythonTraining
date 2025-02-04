from fabric import task
import os
import tarfile
@task
def create_archive(c, source_dir, archive_name="project.tar.gz"):
 """Creates a tar.gz archive of the specified directory."""
 with tarfile.open(archive_name, "w:gz") as tar:
 tar.add(source_dir, arcname=os.path.basename(source_dir))
 print(f"Archive {archive_name} created successfully.")
@task
def upload_and_extract(c, local_archive, remote_path):
 """Uploads the archive to a remote server and extracts it."""
 remote_archive = os.path.join(remote_path, os.path.basename(local_archive))
 print("Uploading archive...")
 c.put(local_archive, remote_archive)
 print(f"Archive uploaded to {remote_archive}")
 print("Extracting archive...")
 c.run(f"tar -xzf {remote_archive} -C {remote_path}")
 c.run(f"rm {remote_archive}") # Optional: Remove the archive after extraction
 print("Extraction complete.")
@task
def package_and_deploy(c, source_dir, remote_path):
 """Packages, uploads, and extracts files on the remote server."""
 archive_name = "project.tar.gz"
 create_archive(c, source_dir, archive_name)
 upload_and_extract(c, archive_name, remote_path)
