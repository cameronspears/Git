import os
import platform
import requests
import subprocess
import sys
from pathlib import Path

def main():
    if platform.system() != "Windows":
        print("This script is designed for Windows systems.")
        sys.exit(1)

    if is_git_installed():
        handle_existing_git_installation()
    else:
        install_latest_git_version()

def get_latest_git_release():
    api_url = "https://api.github.com/repos/git-for-windows/git/releases/latest"
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    asset_64bit = find_64bit_asset(data["assets"])

    if asset_64bit is None:
        raise Exception("64-bit Git installer not found in release assets")

    return data["tag_name"], asset_64bit["browser_download_url"]

def find_64bit_asset(assets):
    for asset in assets:
        if "64-bit.exe" in asset["name"]:
            return asset
    return None

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
        "/SUPPRESSMSGBOXES",
        "/CLOSEAPPLICATIONS",
        "/RESTARTAPPLICATIONS",
        "/ADD_TO_PATH",
    ]

    result = subprocess.run(installation_args, check=True)
    return result.returncode == 0

def is_git_installed():
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except FileNotFoundError:
        return False

def get_git_version():
    result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
    version_str = result.stdout.strip().split()[-1]
    return version_str

def handle_existing_git_installation():
    current_version = get_git_version()
    print(f"Git is already installed: {current_version}")

    latest_version, url = get_latest_git_release()

    latest_version = latest_version.lstrip('v') # remove 'v' prefix from latest version
    if current_version == latest_version:
        print("Git is up to date!")
        repair_choice = input("Do you want to repair the Git installation? (y/n): ")
        if repair_choice.lower() != "y":
            sys.exit(0)
    else:
        update_choice = input(f"Do you want to update Git to the latest version ({latest_version})? (y/n): ")
        if update_choice.lower() != "y":
            sys.exit(0)

    install_latest_git_version(url)

def install_latest_git_version(url=None):
    if url is None:
        latest_version, url = get_latest_git_release()
    else:
        _, latest_version = get_latest_git_release()

    installer_name = "GitInstaller.exe"
    installer_path = os.path.join(os.getcwd(), installer_name)

    try:
        print(f"Downloading Git {latest_version} installer...")
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

if __name__ == "__main__":
    main()
