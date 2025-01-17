<p align="center">
  <img src="app.ico" width="128px" height="128px" alt="Crab Save Clear icon">
</p>
<h1 align="center">Crab Save Clear</h1>

Easily clear your saves in the game "Another Crab's Treasure". Use a hotkey or the clear button to move all the save files to the trash bin.

<p align="center">
  <img width="700px" height="500px" src="preview.png" alt="Preview of the app on windows" />
</p>

## Usage

Follow these steps to use Crab Save Clear:

1. Set the path to your save folder.
2. Set the prefix of the save files (e.g., `saveFile-`).
3. Set a hotkey, such as `f14` or `ctrl+alt+f10`.
4. Click the **Delete files** button or use your hotkey to move the files to the trash bin.

To retrieve your files, they are moved to the system bin.

## Download

**Download the lastest version from the [dist folder](https://github.com/PaoZDev/CrabSaveClear/raw/refs/heads/main/dist/CrabSaveClear.exe) or the [Releases page](https://github.com/PaoZDev/CrabSaveClear/releases).**

## Installation

Ensure Python and pip are installed on your computer.

1. Clone the repository
2. Install the required packages:
  ```
  pip install -r requirements.txt
  ```

## Build EXE Instructions

To build the executable, follow these steps:

1. Install `pyinstaller`:
   ```bash
   pip install pyinstaller
   ```
2. Build from the `.spec` file:
   ```bash
   pyinstaller CrabSaveClear.spec
   ```
3. Alternatively, build using the following command:
   ```bash
   pyinstaller --onefile --windowed --noconsole --clean --icon=app.ico --name CrabSaveClear CRAB_SAVE_CLEAR.py
   ```

## Contribution

Contributions are welcome! Feel free to open an issue or a pull request if you have suggestions or improvements.

## License

This project is licensed under the MIT License - see the `LICENSE` file for more details.