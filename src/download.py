import os
import requests

from . import MODS_FOLDER

def download_mod(file_url, destination):
    response = requests.get(file_url)
    with open(destination, 'wb') as f:
        f.write(response.content)

def update_mod(mod):
    mod_name = mod['name']
    mod_download_url = mod['download_url']
    mod_path = os.path.join(MODS_FOLDER, mod_name)
    if os.path.exists(mod_path):
        print(f"{mod_name} is already up to date.")
    else:
        print(f"Downloading {mod_name}...")
        download_mod(mod_download_url, mod_path)
        print(f"{mod_name} downloaded.")
