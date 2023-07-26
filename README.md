# ssh_file_backup_and_git_commitment
Read the Readme. there is no warranty and no guarantee that this software will work as intended.
# SSH File Transfer and Git Operation Tool

This Python script is designed to interact with a local Linux server that has SSH enabled and to perform file transfer and basic Git operations. The connection to the SSH server is password-protected. 

## Functionalities

- Connect to a Linux server using SSH
- Create a directory on the server with proper permission settings
- Upload files from the local machine to the created directory on the server
- Initialize the directory as a Git repository
- Perform Git operations such as stage and commit the uploaded files
- Set directory permissions

After launching the script, users will be prompted for server IP address, username, password, directory to be created and the file(s) to upload.

The script requires the `paramiko` and `easygui` Python packages.

## Requirements

To run the script, you need:

- Python 3.6+
- paramiko
- easygui
- scp

You can install required Python packages using pip:

```bash
pip install paramiko easygui scp
```

## Usage

To use this script:

1. Clone this repository or download the file
2. Run the script with python:

   ```bash
   python filename.py
   ```

Replace `filename.py` with the name you have saved this file as.

The script will prompt you to enter the server IP address, username, password, the name of the directory to be created in the server's home directory, and the local file to be uploaded to the server. 

## Assumptions

This script assumes your Linux server has SSH enabled and your account has the necessary permissions to create directories and perform Git operations. If not, please make sure to configure your server accordingly. 

This script also assumes you're running it in a environment that supports GUI-based dialog boxes, as it uses the `easygui` package for user input. If not, you'll need to modify the parts of the script that use `easygui.enterbox` and `easygui.fileopenbox` to get user input in a different way.

## Disclaimer 

Please be aware of the security implications of transmitting your credentials in plain text and connecting to SSH servers without validating SSH host keys. Use this script wisely and responsibly.
