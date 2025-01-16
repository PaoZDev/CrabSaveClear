import os
import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, Entry, Text, Button, PhotoImage
import keyboard
import threading
from send2trash import send2trash
import winsound
import json
import PIL

import ctypes
import sys

DIR_PATH = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(DIR_PATH, 'crab_save_clear_config.json')

def is_admin():
    """Check if the script is running as an administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Re-run the script with administrator privileges
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

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
        print(os.path.abspath(CONFIG_FILE))
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
   window.destroy()

def relative_to_assets(path: str):
    # return os.path.dirname(__file__) / "build/assets/frame0" / path
    return os.path.join(os.path.dirname(__file__), "build/assets/frame0/", path).replace("/", "\\")

window = tk.Tk()
window.title("Save Clear")
window.geometry("500x300")
window.configure(bg = "#FFFFFF")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", on_closing)

# Folder path input
folder_path_var = tk.StringVar()
prefix_var = tk.StringVar()
hotkey_var = tk.StringVar()
current_hotkey = None

config = load_config()

print(relative_to_assets("image_1.png"))

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 300,
    width = 500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

# bg
canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    250.0,
    150.0,
    image=image_image_1
)

# Browse btn
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=browse_folder,
    relief="flat"
)
button_1.place(
    x=237.0,
    y=162.0,
    width=46.0,
    height=14.0
)

# Browse input
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    129.5,
    169.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#CFCFCF",
    fg="#000716",
    highlightthickness=0,
    textvariable=folder_path_var
)
entry_1.place(
    x=37.0,
    y=159.0,
    width=185.0,
    height=18.0
)

canvas.create_text(
    27.0,
    138.0,
    anchor="nw",
    text="Folder Path",
    fill="#DFD1BD",
    font=("LoewNext Bold", 14 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    129.5,
    217.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#CFCFCF",
    fg="#000716",
    highlightthickness=0,
    textvariable=prefix_var
)
entry_2.place(
    x=37.0,
    y=207.0,
    width=185.0,
    height=18.0
)

canvas.create_text(
    23.0,
    186.0,
    anchor="nw",
    text="File Prefix",
    fill="#DFD1BD",
    font=("LoewNext Bold", 14 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=set_hotkey,
    relief="flat"
)
button_2.place(
    x=237.0,
    y=258.0,
    width=46.0,
    height=13.0
)

canvas.create_text(
    19.0,
    235.0,
    anchor="nw",
    text="Global Hotkey",
    fill="#DFD1BD",
    font=("LoewNext Bold", 14 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    129.5,
    265.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#CFCFCF",
    fg="#000716",
    highlightthickness=0,
    textvariable=hotkey_var
)
entry_3.place(
    x=37.0,
    y=255.0,
    width=185.0,
    height=18.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=delete_files,
    relief="flat"
)
button_3.place(
    x=341.0,
    y=86.0,
    width=118.0,
    height=131.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    465.0,
    288.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    490.0,
    288.0,
    image=image_image_3
)

canvas.create_text(
    475.0,
    285.0,
    anchor="nw",
    text="x",
    fill="#FFFFFF",
    font=("Lato Regular", 8 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    110.0,
    64.0,
    image=image_image_4
)

# Start the hotkey listener in a separate thread
threading.Thread(target=run_hotkey_listener, daemon=True).start()

# Run the GUI
window.mainloop()