import os
import requests
import threading
import sys
import tkinter as tk
from tkinter import messagebox

# GitHub repository URL
repo_url = 'https://api.github.com/repos/MotanOfficial/MC-Mod-Updater/contents/Mods'

# Get the current directory of the script
script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

# Local mods folder (current directory)
mods_folder = os.path.join(script_dir, 'mods')

def download_mod(file_url, destination):
    response = requests.get(file_url)
    with open(destination, 'wb') as f:
        f.write(response.content)

def update_mod(mod):
    mod_name = mod['name']
    mod_download_url = mod['download_url']
    mod_path = os.path.join(mods_folder, mod_name)
    if os.path.exists(mod_path):
        print(f"{mod_name} is already up to date.")
    else:
        print(f"Downloading {mod_name}...")
        download_mod(mod_download_url, mod_path)
        print(f"{mod_name} downloaded.")

def update_mods():
    # Create mods folder if it doesn't exist
    if not os.path.exists(mods_folder):
        os.makedirs(mods_folder)

    response = requests.get(repo_url)
    if response.status_code == 200:
        mods_list = response.json()
        threads = []
        for mod in mods_list:
            thread = threading.Thread(target=update_mod, args=(mod,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        messagebox.showinfo("Update Mods", "Mods updated successfully.")
    else:
        messagebox.showerror("Update Mods", "Failed to retrieve mod list.")

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
        messagebox.showinfo("Remove Mods", "Unused mods removed successfully.")
    else:
        messagebox.showerror("Remove Mods", "Failed to retrieve mod list.")

def main():
    root = tk.Tk()
    root.title("MC Mod Updater")

    canvas = tk.Canvas(root, width=300, height=200)
    canvas.pack()

    update_button = tk.Button(root, text="Update Mods", command=update_mods, bg="brown", fg="white")
    canvas.create_window(150, 100, window=update_button)

    remove_button = tk.Button(root, text="Remove Mods", command=remove_unused_mods, bg="brown", fg="white")
    canvas.create_window(150, 150, window=remove_button)

    root.mainloop()

if __name__ == "__main__":
    main()
