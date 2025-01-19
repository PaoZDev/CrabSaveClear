import os
import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, Entry, Button, PhotoImage
import keyboard
import threading
from send2trash import send2trash
import winsound
import json
import sys

APP_TITLE = "Crab Save Clear"
APP_VERSION = "0.0.1"
APP_ICON = "app.ico"

# import ctypes

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

def resource_path(filename):
    try:
        base_path = sys._MEIPASS
        base_path = os.path.abspath(".")
    except Exception:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, filename).replace("/", "\\")

def relative_to_assets(filename):
    try:
        base_path = sys._MEIPASS
        base_path = os.path.join(base_path, "CrabSaveClear")
    except Exception:
        base_path =  os.path.join(os.path.dirname(__file__), "assets/")

    return os.path.join(base_path, filename).replace("/", "\\")

def relative_to_exe(filename):
    try:
        base_path = sys._MEIPASS
        base_path = os.path.join(base_path, "CrabSaveClear")
    except Exception:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, filename).replace("/", "\\")


CONFIG_FILE = resource_path('crab_save_clear_config.json')


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
    try:
        keyboard.add_hotkey(hotkey, delete_files)
        messagebox.showinfo("Hotkey Set", f"Hotkey '{hotkey}' is now active for moving files to trash.")
    except Exception as e:
        current_hotkey = ""
        messagebox.showerror("Hotkey Set", e)

def run_hotkey_listener():
    """Keep the hotkey listener running in a separate thread."""
    keyboard.wait()

def save_config():
    config['folder'] = folder_path_var.get()
    config['prefix'] = prefix_var.get()
    config['hotkey'] = hotkey_var.get()
    print("config saved:")
    print(CONFIG_FILE)
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent = 4)

def load_config():
    print("load config:")
    print(CONFIG_FILE)
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
   window.destroy()


window = tk.Tk()
window.iconbitmap(window, relative_to_exe(APP_ICON))
window.title(APP_TITLE)
window.geometry("700x500")
window.configure(bg = "#0CADEC")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", on_closing)

# Folder path input
folder_path_var = tk.StringVar()
prefix_var = tk.StringVar()
hotkey_var = tk.StringVar()
current_hotkey = None

config = load_config()

canvas = Canvas(
    window,
    bg = "#22bcf5",
    height = 500,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0,
    250.0,
    image=image_image_1
)


button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    window,
    image=button_image_1, 
    command=browse_folder, 
    borderwidth=0, 
    background="#0CADEC", 
    activebackground="#0CADEC"

)

button_1.place(
    x=370.8248291015625,
    y=264.0,
    width=72.17518615722656,
    height=27.167882919311523
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    92.0,
    246.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    92.0,
    334.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    92.0,
    420.0,
    image=image_image_4
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    196.0,
    277.0,
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
    x=51.0,
    y=268.0,
    width=290.0,
    height=20.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    196.0,
    365.0,
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
    x=51.0,
    y=356.0,
    width=290.0,
    height=20.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    196.0,
    451.0,
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
    x=51.0,
    y=442.0,
    width=290.0,
    height=20.0
)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    window,
    image=button_image_2, 
    command=set_hotkey, 
    borderwidth=0, 
    background="#22bcf5", 
    activebackground="#22bcf5"
)
button_2.place(
    x=371.0,
    y=437.0,
    width=88.0,
    height=27.0
)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    window,
    image=button_image_3, 
    command=delete_files, 
    borderwidth=0, 
    background="#09abeb", 
    activebackground="#09abeb"
)
button_3.place(
    x=477.0,
    y=151.0,
    width=178.7633514404297,
    height=198.45762634277344
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    658.0,
    484.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    683.0,
    484.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    672.0,
    484.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    176.0,
    102.0,
    image=image_image_8
)

# show app version
txt_version = canvas.create_text(640, 492, anchor = tk.SE, text=f"v{APP_VERSION}", fill="#038ee9")

# Start the hotkey listener in a separate thread
threading.Thread(target=run_hotkey_listener, daemon=True).start()

# Run the GUI
window.mainloop()