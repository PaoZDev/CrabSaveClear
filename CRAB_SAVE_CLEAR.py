import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter
import keyboard
import threading
from send2trash import send2trash
import winsound
import json
import PIL

import ctypes
import sys

CONFIG_FILE = 'config.json'

# def is_admin():
#     """Check if the script is running as an administrator."""
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False

# if not is_admin():
#     # Re-run the script with administrator privileges
#     ctypes.windll.shell32.ShellExecuteW(
#         None, "runas", sys.executable, " ".join(sys.argv), None, 1
#     )
#     sys.exit()

def move_files_to_trash_recursive(folder_path, prefix):
    """
    Recursively moves files starting with a specific prefix to the trash.

    Args:
        folder_path (str): The path of the folder to scan.
        prefix (str): The prefix of the files to move to trash.
    """
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", f"The folder '{folder_path}' does not exist.")
        return

    try:
        trashed_count = 0

        # Walk through the directory and its subdirectories
        for dirpath, _, filenames in os.walk(folder_path):
            if not os.path.exists(dirpath):  # Ensure the directory exists
                continue
            for file_name in filenames:
                if file_name.startswith(prefix):
                    file_path = os.path.join(dirpath, file_name).replace("/", "\\")
                    if os.path.isfile(file_path):  # Ensure it's a file
                        send2trash(file_path)
                        trashed_count += 1

        winsound.PlaySound("SystemAsterisk", winsound.MB_OK)
        # messagebox.showinfo("Operation Completed", f"Moved {trashed_count} file(s) starting with '{prefix}' to the trash.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_folder():
    folder = filedialog.askdirectory(title="Select Folder")
    if folder:
        folder_path_var.set(folder)

def delete_files():
    folder_path = folder_path_var.get()
    prefix = prefix_var.get()
    if not folder_path or not prefix:
        messagebox.showwarning("Input Required", "Please select a folder and enter a prefix.")
        return
    move_files_to_trash_recursive(folder_path, prefix)

def set_hotkey():
    global current_hotkey
    hotkey = hotkey_var.get()
    if not hotkey:
        messagebox.showwarning("Input Required", "Please enter a hotkey.")
        return

    # Unregister the previous hotkey if set
    if current_hotkey:
        keyboard.remove_hotkey(current_hotkey)

    # Register the new hotkey
    current_hotkey = hotkey
    keyboard.add_hotkey(hotkey, delete_files)
    messagebox.showinfo("Hotkey Set", f"Hotkey '{hotkey}' is now active for moving files to trash.")

def run_hotkey_listener():
    """Keep the hotkey listener running in a separate thread."""
    keyboard.wait()

def save_config():
    config['folder'] = folder_path_var.get()
    config['prefix'] = prefix_var.get()
    config['hotkey'] = hotkey_var.get()
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent = 4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            print(config)
            folder_path_var.set(config["folder"])
            prefix_var.set(config["prefix"])
            hotkey_var.set(config["hotkey"])
            if hotkey_var.get():
                current_hotkey = hotkey_var.get()
                try:
                    keyboard.add_hotkey(current_hotkey, delete_files)
                except Exception as e:
                    messagebox.showerror("Error", f"Hotkey: {e}")
            return config
    else:
        return {}

def on_closing():
   # Save the window position when the application is closed
   save_config()
    
   # Destroy the root window
   root.destroy()

# Dark mode
customtkinter.set_appearance_mode("dark")

# Create the main GUI window
root = customtkinter.CTk()
root.title("Save Clear")
root.geometry("500x350")

root.protocol("WM_DELETE_WINDOW", on_closing)

# set minimum window size value
root.minsize(500, 350)
 
# set maximum window size value
root.maxsize(500, 350)

# Custom Font
my_font = customtkinter.CTkFont(family='Roboto Slab Medium', size=30)

# Create a bg label
image = PIL.Image.open("NACRE.png")
background_image = customtkinter.CTkImage(image, size=(500, 350))
bg_lbl = customtkinter.CTkLabel(root, text="", image=background_image)
bg_lbl.place(x=0, y=0)

# Folder path input
folder_path_var = tk.StringVar()
prefix_var = tk.StringVar()
hotkey_var = tk.StringVar()
current_hotkey = None

config = load_config()
print(config)

my_label = customtkinter.CTkLabel(root, text="Folder Path", font = my_font)
my_label.pack(pady=0)

folder_frame = tk.Frame(root)
folder_frame.pack(pady=2)
tk.Entry(folder_frame, textvariable=folder_path_var, width=40).pack(side=tk.LEFT, padx=5)
tk.Button(folder_frame, text="Browse", command=browse_folder).pack(side=tk.LEFT)

# Prefix input
tk.Label(root, text="File Prefix:").pack(pady=5)
tk.Entry(root, textvariable=prefix_var, width=40).pack(pady=5)

# Hotkey input
tk.Label(root, text="Set Global Hotkey:").pack(pady=5)
hotkey_frame = tk.Frame(root)
hotkey_frame.pack(pady=5)
tk.Entry(hotkey_frame, textvariable=hotkey_var, width=20).pack(side=tk.LEFT, padx=5)
tk.Button(hotkey_frame, text="Set Hotkey", command=set_hotkey).pack(side=tk.LEFT)

# Delete button
tk.Button(root, text="Move Files to Trash", command=delete_files, bg="blue", fg="white").pack(pady=20)

# Start the hotkey listener in a separate thread
threading.Thread(target=run_hotkey_listener, daemon=True).start()

# Run the GUI
root.mainloop()
