from fabric import task
@task
def install_nginx(c):
 """Installs Nginx on the remote server."""
 c.run("sudo apt update -y")
 c.run("sudo apt install -y nginx")
 print(" Nginx installed successfully.")
@task
def create_html(c):
 """Creates a sample index.html file directly on the remote server."""
 html_content = "<h1>Hi There, this is Fabric. Deployed using Fabric!</h1>"
 c.run(f'echo "{html_content}" | sudo tee /var/www/html/index.html')
 print(" HTML file created successfully.")
@task
def configure_firewall(c):
 """Configures firewall rules to allow web traffic."""
 c.run("sudo ufw allow 'Nginx Full'")
 print("Firewall configured successfully.")
@task
def restart_nginx(c):
 """Restarts the Nginx service."""
 c.run("sudo systemctl restart nginx")
 print(“Nginx restarted successfully.")
@task
def deploy(c):
 """Full deployment: Install Nginx, create HTML file, configure firewall, restart Nginx."""
 install_nginx(c)
 create_html(c)
 configure_firewall(c)
 restart_nginx(c)
 print(f" Deployment complete! Visit http://{REMOTE_HOST}/")
