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
## Instructions for **Powershell**
* Download the files and make a `profiles` folder in the project directory: 
```powershell
git clone https://github.com/Rantunah/moonlight-toggler.git
cd moonlight-toggler
mkdir profiles
```
* Generate the profiles. Make sure you set up your screens correctly (only one enabled and with the correct resolution applied) and then run the commands bellow to generate each profile:

  1. For the physical monitor:
  * ```powershell
    .\bin\MonitorSwitcher.exe -save:.\profile\monitor.xml
    ```
  2. For the HDMI dongle: 
  * ```powershell
    .\bin\MonitorSwitcher.exe -save:.\profile\remote.xml
    ```

&nbsp;

# Usage:
Start the server.
```powershell 
python .\src\main.py
```
To terminate this server you can click CTRL+C in the terminal or terminate the `python.exe` service in the Task Manager.  

After this, your monitor should flash and change to the physical monitor profile.
If you start a Moonlight streaming session you'll see the physical screen disconnect as the remote screen comes off.

&nbsp;

# Known Issues
* When switching from a physical monitor with a larger scale than the remote one the cursor will remain scaled untill you leave the stream.

&nbsp;

# Acknowledgements
## Monitor Profile Switcher v7.00
This project distributes the executable that is depended uppon, under compliance with it's license.  
A big "thank you" to **martink87** for producing this wonderful piece of software, that has accompanied me even before I started to learn how to program. It has enabled my whole workflow with `moonlight-qt` and `GameStream`. Without it, I would probably never have started to learn how to code.  
You can find the source code for `MonitorSwitcher.exe` on it's [SourceForge page](https://sourceforge.net/projects/monitorswitcher).

## Individuals
* DemonCat, over at the moonlight-qt discord server, helped me figure out some TCP connection stuff on Christmas eve. Big thank you!