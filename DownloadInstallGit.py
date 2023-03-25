import os
import requests
import subprocess
import sys
from pathlib import Path

def download_git_installer(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(save_path, "wb") as installer_file:
        for chunk in response.iter_content(chunk_size=8192):
            installer_file.write(chunk)

def install_git(installer_path):
    installation_args = [
        installer_path,
        "/VERYSILENT",
        "/NORESTART",
        "/NOCANCEL",
        "/SP-",
        "/LOG",
        "/SUPPRESSMSGBOXES",
        "/CLOSEAPPLICATIONS",
        "/RESTARTAPPLICATIONS",
        "/ADD_TO_PATH",
    ]

    result = subprocess.run(installation_args, check=True)
    return result.returncode == 0

if __name__ == "__main__":
    url = "https://github.com/git-for-windows/git/releases/download/v2.35.1.windows.2/Git-2.35.1.2-64-bit.exe"
    installer_name = "GitInstaller.exe"
    installer_path = os.path.join(os.getcwd(), installer_name)

    try:
        print("Downloading Git installer...")
        download_git_installer(url, installer_path)
        print("Git installer downloaded.")

        print("Installing Git and adding to PATH...")
        if install_git(installer_path):
            print("Git installation complete and added to PATH.")
        else:
            print("Git installation failed.")
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    finally:
        if Path(installer_path).is_file():
            os.remove(installer_path)
