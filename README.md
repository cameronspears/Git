# Git Installer for Windows

This Python script automates the process of downloading and installing the latest 64-bit version of Git for Windows on your system. It checks if Git is already installed, offers an update if a newer version is available, and adds Git cmd to the system environment variables PATH.

## Requirements

- Python 3.6 or higher
- requests library

You can install the requests library using pip by running the following command:
```
pip install requests
```
## Usage

1. Download or clone the repository containing the Python script.
2. Open a command prompt or terminal in the directory where the script is located.
3. Run the script using Python by executing the following command:
```
python git_installer.py
```
The script will check if Git is already installed on your system. If it is, it will offer you the option to update Git to the latest version. If Git is not installed, it will proceed to download and install the latest 64-bit version of Git for Windows.

Once the installation is complete, Git cmd should be added to your system environment variables PATH. You may need to restart any command prompts or applications that rely on the PATH variable for the changes to take effect.

## Notes

This script is designed specifically for Windows systems. It will not work on other operating systems.
