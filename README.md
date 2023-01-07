# moolight-toggler
This script automates the process of switching between a headless HDMI dongle and a physical monitor on **Windows 11** for use with Nvidia's GameStream streaming service.

&nbsp;

# How it works
It reads some path information from a `config.toml`, located at the root of the project and wraps arround some commands to be passed to `MonitorSwitcher.exe`, which then does the heavy lifting and switches monitors whenever `nvstreamer.exe` is running or stops.

&nbsp;

# Installation
## Requirements:
* Python 3.11 (this script depends uppon `tomllib`)
* Packages - `psutil`

&nbsp;

## Instructions for **Powershell**
* Download the files and make a `profiles` folder in the project directory:
```powershell
git clone https://github.com/Rantunah/moonlight-toggler.git
cd moonlight-toggler
mkdir profiles
```
* Generate the profiles. Make sure you set up your screens correctly before you run each command.

  1. In  Windows `Display settings`, setup the the physical monitor first, disable  the remote monitor and then run the command:
      ```powershell
      .\bin\MonitorSwitcher.exe -save:.\profile\monitor.xml
      ```
  2. Do the same, but this time for the remote monitor: 
      ```powershell
      .\bin\MonitorSwitcher.exe -save:.\profile\remote.xml
      ```

&nbsp;

## Instructions for the **pre-built `.exe`**
1. Unpack the .zip archive
    * It's recomended you keep the file structure that's in the archive.
1. Follow the instructions for profile generation above.

&nbsp;

# Usage:
## .py script
1. Navigate to the project folder and start the server.
    * Make sure you have your virtual environment activated or the required packages installed
    ```powershell
    cd <path to the moonlight-toggler folder>
    python .\src\main.py
    ```
2. To terminate this server you can click CTRL+C in the terminal or terminate the `python.exe` process in the Windows `Task Manager`, that has a location in properties that matches `moonlight-toggler\src\main.py`.

## pre-built `.exe`
1. run `moonlight_toggler.exe` in the `script` folder
2. To terminate this server use the Windows `Task Manager` to terminate the `moonlight_toggler.exe` task.

  * You can start the server at login by placing a shortcut to `moonlight-toggler.exe` in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` 


After this, your monitor should flash and change to the physical monitor profile.
If you start a Moonlight streaming session, you'll see the physical screen disconnect as the remote screen comes off.

&nbsp;

# Build from source
## Requirements:
* Packages - `pyinstaller`, `psutil`

It's not required to build from source to run the script, however, it's recommended to do it for easy startup on login.  
Make sure that you've activated your virtual environment or have the requirements installed in your environment.
1. The executable is built running the following command:   
    ```powershell
    pyinstaller.exe .\src\main.py --windowed --onedir --noconfirm --name "moonlight_toggler"
    ```
    A script that does the above and eases the process of tidying up folder names during builds is also provided
    ```powershell
    .\build.ps1
    ```
2. There will be a `dist` folder after the script compiles.
    ```powershell
    New-Item -Path ".\dist\profiles" -ItemType Directory
    Copy-Item ".\bin" ".\dist\bin"
    ```
After this the script is ready for execution.

&nbsp;

# Known Issues
* When switching from a physical monitor with a larger scale than the remote one the cursor will remain scaled untill you leave the stream.
  * There's a built in hack that **pauses the server for 10 seconds after the stream starts** to allow the user enough time to quit the stream and start it again to reset the cursor size.

&nbsp;

# Acknowledgements
## Monitor Profile Switcher v7.00
This project distributes the executable that is depended uppon, under compliance with it's license.  
A big "thank you" to **martink87** for producing this wonderful piece of software, that has accompanied me even before I started to learn how to program. It has enabled my whole workflow with `moonlight-qt` and `GameStream`. Without it, I would probably never have started to learn how to code.  
You can find the source code for `MonitorSwitcher.exe` on it's [SourceForge page](https://sourceforge.net/projects/monitorswitcher).

## Individuals
* DemonCat, over at the moonlight-qt discord server, helped me figure out some TCP connection. Big "thank you"!