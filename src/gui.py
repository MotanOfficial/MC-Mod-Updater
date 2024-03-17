import os
import requests
import tkinter as tk
from tkinter import messagebox

from .updator import update_mods
from . import REPO_URL, MODS_FOLDER, __version__

def remove_unused_mods():
    local_mods = os.listdir(MODS_FOLDER)
    response = requests.get(REPO_URL)
    if response.status_code == 200:
        remote_mods = [mod['name'] for mod in response.json()]
        unused_mods = set(local_mods) - set(remote_mods)
        for mod in unused_mods:
            mod_path = os.path.join(MODS_FOLDER, mod)
            print(f"Removing {mod}...")
            os.remove(mod_path)
        messagebox.showinfo("Remove Mods", "Unused mods removed successfully.")
    else:
        messagebox.showerror("Remove Mods", "Failed to retrieve mod list.")

def run():
    root = tk.Tk()
    root.title(f"MC Mod Updater v{__version__}")

    canvas = tk.Canvas(root, width=300, height=200)
    canvas.pack()

    update_button = tk.Button(root, text="Update Mods", command=update_mods, bg="brown", fg="white")
    canvas.create_window(150, 100, window=update_button)

    remove_button = tk.Button(root, text="Remove Mods", command=remove_unused_mods, bg="brown", fg="white")
    canvas.create_window(150, 150, window=remove_button)

    root.mainloop()