# moolight-toggler
"This script automates the process of switching between a headless HDMI dongle and a physical monitor on Windows 11 for use with Nvidia's GameStream streaming service." 

## How it works
It reads some path information from a `config.toml`, located at the root of the project and wraps arround some commands to be passed to `MonitorSwitcher.exe`, which then does the heavy lifting and switches monitors whenever `nvstreamer.exe` is running or stops.

## Installation
### Requirements:
* Python 3.11 (this script depends uppon `tomllib`)
* Packages - `psutil`
### Instructions:
```powershell
# You can run these commands in Powershell
git clone https://github.com/Rantunah/moonlight-toggler.git
cd moonlight-toggler
mkdir profiles
<# To generate the profiles, make sure you set up your screens correctly (only one enabled and with the
correct resolution applied) and then run the commands bellow to generate each profile: #>
# For the physical monitor:
.\bin\MonitorSwitcher.exe -save:.\profile\monitor.xml
# For the HDMI dongle:
.\bin\MonitorSwitcher.exe -save:.\profile\remote.xml

```
### Usage:
```powershell
<# This starts the server. To terminate this server you can click CTRL+C in the terminal or terminate 
the 'python.exe' service in the Task Manager. #>
python .\src\main.py
```
After this, your monitor should flash and change to the physical monitor profile.
If you start a Moonlight streaming session you'll see the physical screen disconnect as the remote screen comes off.
## Known Issues
* When switching from a physical monitor with a larger scale than the remote one the cursor will remain scaled untill you leave the stream.

## Monitor Profile Switcher v7.00
This project distributes the executable that is depended uppon, under compliance with it's license.  
A big "thank you" to **martink87** for producing this wonderful piece of software, that has accompanied me even before I started to learn how to program.  
You can find the source code for this project on it's [SourceForge page](https://sourceforge.net/projects/monitorswitcher).