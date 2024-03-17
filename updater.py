import os
import requests
import zipfile
import shutil

# GitHub repository URL
repo_url = 'https://github.com/MotanOfficial/MC-Mod-Updater/tree/main/Mods'

# Get the current directory of the script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Local mods folder (current directory)
mods_folder = script_dir

def download_mod(file_url, destination):
    response = requests.get(file_url)
    with open(destination, 'wb') as f:
        f.write(response.content)

def update_mods():
    response = requests.get(repo_url)
    if response.status_code == 200:
        mods_list = response.json()
        for mod in mods_list:
            mod_name = mod['name']
            mod_download_url = mod['download_url']
            mod_path = os.path.join(mods_folder, mod_name)
            if os.path.exists(mod_path):
                print(f"Updating {mod_name}...")
                download_mod(mod_download_url, mod_path)
            else:
                print(f"Downloading {mod_name}...")
                download_mod(mod_download_url, mod_path)
    else:
        print("Failed to retrieve mod list.")

def remove_unused_mods():
    local_mods = os.listdir(mods_folder)
    response = requests.get(repo_url)
    if response.status_code == 200:
        remote_mods = [mod['name'] for mod in response.json()]
        unused_mods = set(local_mods) - set(remote_mods)
        for mod in unused_mods:
            mod_path = os.path.join(mods_folder, mod)
            print(f"Removing {mod}...")
            os.remove(mod_path)
    else:
        print("Failed to retrieve mod list.")

def main():
    print("Checking for updates...")
    update_mods()
    print("Removing unused mods...")
    remove_unused_mods()
    print("Update process completed.")

if __name__ == "__main__":
    main()
