import os
import json
import webview
from send2trash import send2trash
import keyboard

CONFIG_FILE = 'crab_save_clear_config_2.json'

print(os.path.dirname(__file__))

class Api:
    def __init__(self):
        self.load_config()
        self.current_hotkey = self.config.get('hotkey', '')

        if self.current_hotkey:
            self.set_hotkey(self.current_hotkey)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                self.config = json.load(file)
        else:
            self.config = {"folder": "", "prefix": "", "hotkey": ""}

    def save_config(self, folder, prefix, hotkey):
        self.config['folder'] = folder
        self.config['prefix'] = prefix
        self.config['hotkey'] = hotkey
        with open(CONFIG_FILE, 'w') as file:
            json.dump(self.config, file)
        
        if hotkey:
            self.set_hotkey(hotkey)
    
    def set_hotkey(self, hotkey):
        # if self.current_hotkey:
        #     keyboard.remove_hotkey(self.current_hotkey)
        print(hotkey, keyboard.get_hotkey_name(hotkey))
        
        self.current_hotkey = hotkey
        if hotkey:
            print('set hotkey', hotkey)
            keyboard.add_hotkey(hotkey, lambda: self.delete_files(self.config['folder'], self.config['prefix']))

    def get_config(self):
        return self.config

    def delete_files(self, folder, prefix):
        if folder and prefix:
            trashed_count = 0
            for dirpath, _, filenames in os.walk(folder):
                for file_name in filenames:
                    if file_name.startswith(prefix):
                        file_path = os.path.join(dirpath, file_name)
                        send2trash(file_path)
                        trashed_count += 1
            return f"{trashed_count} files moved to trash."
        else:
            return "Folder path and prefix required."
    
    def open_folder_dialog(self):
        folder = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG)
        return folder[0] if folder else ''

# Create the API instance
api = Api()

# HTML content for the web view
html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crab Save Clear</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #0CADEC;
            color: #fff;
            text-align: center;
            padding: 20px;
        }
        input, button {
            margin: 10px 0;
            padding: 10px;
            width: 80%;
        }
        button {
            background-color: #0099CC;
            color: #fff;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Crab Save Clear</h1>
    </br>
    <label for="folder">Folder Path</label></br>
    <input id="folder" type="text" autocorrect="off" autocapitalize="none" placeholder="Folder Path" value="">
    <button onclick="selectFolder()">Browse</button>
    </br>
    <label for="prefix">File Prefix</label></br>
    <input id="prefix" type="text" autocorrect="off" autocapitalize="none" placeholder="File Prefix" value="">
    </br>
    <label for="hotkey">Global Hotkey</label></br>
    <input id="hotkey" type="text" autocorrect="off" autocapitalize="none" placeholder="Global Hotkey" value="">
    <button onclick="startListeningHotkey()">listen Hotkey</button>
    <button onclick="setHotkey()">Set Hotkey</button>
    </br>
    <button onclick="deleteFiles()">Delete Files</button>
    <button onclick="saveConfig()">Save Config</button>
    <button onclick="get_config()">Get Config</button>
    <p id="status"></p>

    <script>
        let listening = false;
        let pressedKeys = new Set();

        // Load configuration on page load
        window.addEventListener('pywebviewready', function() {
            get_config()
        })
        
        // save configuration on page close
        function closeWindow() {
            saveConfig();
            window.pywebview.api.close_window();
        }

        window.pywebview.api.register_event_listener("closing", closeWindow);

        function get_config() {
            window.pywebview.api.get_config().then(config => {
                console.log(config)
                document.getElementById('folder').value = config.folder;
                document.getElementById('prefix').value = config.prefix;
                document.getElementById('hotkey').value = config.hotkey;
            });
        }

        function selectFolder() {
            window.pywebview.api.open_folder_dialog().then(folder => {
                if (folder) {
                    document.getElementById('folder').value = folder;
                }
            });
        }

        function deleteFiles() {
            let folder = document.getElementById('folder').value;
            let prefix = document.getElementById('prefix').value;
            window.pywebview.api.delete_files(folder, prefix).then(response => {
                document.getElementById('status').innerText = response;
            });
        }

        function saveConfig() {
            let folder = document.getElementById('folder').value;
            let prefix = document.getElementById('prefix').value;
            let hotkey = document.getElementById('hotkey').value;
            window.pywebview.api.save_config(folder, prefix, hotkey).then(() => {
                document.getElementById('status').innerText = "Configuration saved!";
            });
        }

        function startListeningHotkey() {
            if (listening) return;
            listening = true;
            document.getElementById('status').innerText = "Press a key combination for the hotkey...";
            document.addEventListener('keydown', recordKey);
            document.addEventListener('keyup', finalizeHotkey);
        }

        function recordKey(event) {
            event.preventDefault();
            pressedKeys.add(event.key);

            let hotkey = Array.from(pressedKeys).sort().join('+');
            document.getElementById('hotkey').value = hotkey;
        }

        function finalizeHotkey(event) {
            document.removeEventListener('keydown', recordKey);
            document.removeEventListener('keyup', finalizeHotkey);
            listening = false;
            pressedKeys.clear();
            document.getElementById('status').innerText = "Hotkey set!";

            // Call the set_hotkey API
            let hotkey = document.getElementById('hotkey').value;
            window.pywebview.api.set_hotkey(hotkey);
        }

        function setHotkey() {
            document.getElementById('hotkey').value = key;
            document.getElementById('status').innerText = "Hotkey set to " + key;
            document.removeEventListener('keydown', setHotkey);
            listening = false;
 
            let hotkey = document.getElementById('hotkey').value;
            window.pywebview.api.set_hotkey(hotkey).then(() => {
                document.getElementById('status').innerText = "Configuration saved!";
            });
        }
    </script>
</body>
</html>
'''

# Start the webview with the API
if __name__ == '__main__':
    window = webview.create_window('Crab Save Clear', html=html, js_api=api)
    webview.start(debug=True)
