import os
import time
import paramiko
import easygui as eg
import time
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from scp import SCPClient
def run_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    # Waiting for the command to complete
    while not stdout.channel.exit_status_ready():
        time.sleep(1)

def dlg(title):
    return eg.enterbox(title)

def ssh_connect(address, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(address, username=username, password=password)
    return ssh

def sudo_mkdir(ssh, password, dirname):
    run_command(ssh, f'echo {password} | sudo -S mkdir ~/{dirname}')
    time.sleep(6)
def create_sudo_dir(ssh, password, dirname):
    commands = [
        f"echo {password} | sudo -S chgrp usergroup ~/{dirname}",  # change group to a group your user is part of
        f"echo {password} | sudo -S chmod 770 ~/{dirname}"  # set permissions for owner and group only
    ]
    for cmd in commands:
        run_command(ssh, cmd)
def create_dir(ssh, password, dirname):
    commands = [
        f'echo {password} | sudo -S mkdir -p ~/{dirname}', # creates the directory with superuser privileges
        f'echo {password} | sudo -S chown {username}:{username} ~/{dirname}', # changes directory owner to connecting user
        f'echo {password} | sudo -S chmod 775 ~/{dirname}'  # changes directory permissions to allow read, write, and execute access for owner and group.
    ]
    for command in commands:
        run_command(ssh, command)
        time.sleep(1) 
def upload_file(ssh, local_path, remote_path):
    scp = SCPClient(ssh.get_transport()) 
    scp.put(local_path, remote_path.replace('//','/'))


def git_initialize(ssh, dirname):
    run_command(ssh, f'cd ~/{dirname} && git init')

def git_commit(ssh, dirname, filename):
    run_command(ssh, f'cd ~/{dirname} && git add {filename} && git commit -m "Committed {filename}"')

def check_if_file_exists(ssh, dirname, filename):
    stdin, stdout, stderr = ssh.exec_command(f'cd ~/{dirname} && if [ -f {filename} ]; then echo "True"; else echo "False"; fi')
    # Waiting for the command to complete
    while not stdout.channel.exit_status_ready():
        time.sleep(1)
    return stdout.read().decode().strip() == 'True'

address = dlg('Input your server IP address')
username = dlg('Enter the username')
password = dlg("Enter the SSH and sudo password")
dirname = dlg("Enter name of the directory to be created in the home (~) directory on server")
local_path = eg.fileopenbox("Select the file(s) to upload")
file_name = local_path
print(file_name)
#remote_path = f'~/{dirname}/{os.path.basename(local_path)}'
remote_path = f'~/{dirname}/' + os.path.basename(local_path)
remote_dir = f'~/{dirname}/'
ssh = ssh_connect(address, username, password)
#sudo_mkdir(ssh, password, dirname)
create_dir(ssh, password, dirname)
run_command(ssh, f'echo {password} | sudo -S chown {username} ~/{dirname}')
ssh.close()
ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(address, username=username, password=password)
upload_file(ssh, file_name, remote_dir)

file_already_exists = check_if_file_exists(ssh, dirname, os.path.basename(file_name))
if file_already_exists:
    run_command(ssh, f'cd ~/{dirname} && git rm -f {os.path.basename(file_name)}')

git_initialize(ssh, dirname)
git_commit(ssh, dirname, os.path.basename(file_name))

ssh.close()
ssh = ssh_connect(address, username, password)
run_command(ssh, f'echo {password} | sudo -S chown root ~/{dirname}')
run_command(ssh, f'echo {password} | sudo -S chown root:root ~/{dirname}')
run_command(ssh, f'echo {password} | sudo -S chmod 700 ~/{dirname}')
ssh.close()
print("Pronto")
time.sleep(5)
