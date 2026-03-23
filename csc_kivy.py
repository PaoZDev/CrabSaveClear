import os
import json
import threading
import keyboard
from send2trash import send2trash
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import platform

# Configuration
APP_TITLE = "Crab Save Clear"
APP_VERSION = "0.0.1"
CONFIG_FILE = 'crab_save_clear_config.json'

class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Background Image
        self.background = Image(source='assets/image_1.png')
        self.add_widget(self.background)
        
        # Folder Path Input
        self.folder_input = TextInput(hint_text='Select Folder', size_hint=(1, 0.1))
        self.add_widget(self.folder_input)

        # Prefix Input
        self.prefix_input = TextInput(hint_text='Enter Prefix', size_hint=(1, 0.1))
        self.add_widget(self.prefix_input)

        # Hotkey Input
        self.hotkey_input = TextInput(hint_text='Set Hotkey', size_hint=(1, 0.1))
        self.add_widget(self.hotkey_input)
        
        # Browse Folder Button
        self.browse_button = Button(text='Browse Folder', size_hint=(1, 0.1))
        self.browse_button.bind(on_press=self.browse_folder)
        self.add_widget(self.browse_button)
        
        # Set Hotkey Button
        self.hotkey_button = Button(text='Set Hotkey', size_hint=(1, 0.1))
        self.hotkey_button.bind(on_press=self.set_hotkey)
        self.add_widget(self.hotkey_button)

        # Delete Files Button
        self.delete_button = Button(text='Delete Files', size_hint=(1, 0.1))
        self.delete_button.bind(on_press=self.delete_files)
        self.add_widget(self.delete_button)

        # Load configuration
        self.load_config()

    def browse_folder(self, instance):
        # Logic to browse folder (stub for example)
        print("Browsing folder...")

    def set_hotkey(self, instance):
        hotkey = self.hotkey_input.text
        if hotkey:
            keyboard.add_hotkey(hotkey, self.delete_files)
            print(f"Hotkey '{hotkey}' set.")

    def delete_files(self, instance=None):
        folder_path = self.folder_input.text
        prefix = self.prefix_input.text
        if folder_path and prefix:
            print(f"Deleting files in {folder_path} with prefix {prefix}")
            # Simulate deleting files
            send2trash(folder_path)  # Example function call


    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)
                self.folder_input.text = config.get('folder', '')
                self.prefix_input.text = config.get('prefix', '')
                self.hotkey_input.text = config.get('hotkey', '')

    def save_config(self):
        config = {
            'folder': self.folder_input.text,
            'prefix': self.prefix_input.text,
            'hotkey': self.hotkey_input.text
        }
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file)

class MyApp(App):
    def build(self):
        Window.bind(on_request_close=self.on_closing)
        return MyLayout()

    def on_closing(self, *args):
        self.root.save_config()
        return True

if __name__ == "__main__":
    MyApp().run()
