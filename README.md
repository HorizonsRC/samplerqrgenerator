# Sampler QR Generator


## Installation

Download the latest release binary file from the Releases section in the sidebar. You probably want the `.whl` file. You can place this file anywhere, but I would recommend placing it in a `Plugins` folder inside your Hilltop installation, for example `C:\Hilltop\Plugins\`

Open your Hilltop directory in a terminal emulator. You can do this by navigating to the directory in File Explorer, right-clicking in white space and hitting "Open in Terminal". (In Windows 11 you might have to hit "More options" or something to bring up to bring up the Windows 10 menu for some reason.)

Enter the following commands

32x:
```
.\Libs\python.exe -m pip install <path>
```

64x:
```
.\x64\Libs\python.exe -m pip install <path>
```

where `<path>` is the relative path to the plugin `.whl` or `.tar.gz` file that you have saved.

For example, if your Hilltop directory is `C:\Hilltop` and you've saved your plugin file in `C:\Hilltop\Plugins`, then your command line would look like this:

```
PS C:\Hilltop> .\Libs\python.exe -m pip install .\Plugins\samplerqrgenerator-0.1.0_win32.whl
```
for 32 bit, or
```
PS C:\Hilltop> .\x64\Libs\python.exe -m pip install .\Plugins\samplerqrgenerator-0.1.0_win64.whl
```
for the 64 bit version.

That should do it? 

