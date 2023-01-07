<# Check if pyinstaller package is installed in the current environment before
running the script#>
if (Get-Command "pyinstaller.exe" -ErrorAction Stop) 
{ 
    $exe_name = "moonlight_toggler"
    $folder_name = "script"
    
    <# Change the name of the distribution folder if it has already been changed by
    this script #>
    if (Test-Path .\dist\$folder_name) {
        Rename-Item .\dist\$folder_name $exe_name
    }
    # Build executable folder
    pyinstaller.exe .\src\main.py --windowed --onedir --noconfirm --name $exe_name
    
    # Change the name of the distribution folder for aesthetic reasons
    if (Test-Path .\dist\$exe_name) {
        Rename-Item .\dist\$exe_name $folder_name
    }
}


