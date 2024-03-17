import os
import requests
from tkinter import messagebox

from . import REPO_URL, MODS_FOLDER
from .download import update_mod

def update_mods():
    if not os.path.exists(MODS_FOLDER):
        os.makedirs(MODS_FOLDER)

    response = requests.get(REPO_URL)
    if response.status_code == 200:
        mods_list = response.json()
        for mod in mods_list:
            update_mod(mod)
        messagebox.showinfo("Update Mods", "Mods updated successfully.")
    else:
        messagebox.showerror("Update Mods", "Failed to retrieve mod list.")
