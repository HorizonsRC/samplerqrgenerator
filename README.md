# Sampler QR Generator


## Installation

### Download the Plugin files

Download the latest release binary file from the Releases section in the sidebar. You probably want the `.whl` files. It is likely that you would need to install both the 32 and 64 bit versions of the plugin. You can place this file anywhere, but I would recommend placing it in a `Plugins` folder inside your Hilltop installation, for example `C:\Hilltop\Plugins\`

Open your Hilltop directory in a terminal emulator. You can do this by navigating to the directory in File Explorer, right-clicking in white space and hitting "Open in Terminal". (In Windows 11 you might have to hit "More options" or something to bring up to bring up the Windows 10 menu for some reason.)

Enter the following commands:

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
PS C:\Hilltop> .\Libs\python.exe -m pip install .\Plugins\samplerqrgenerator-0.1.1.whl
```
for 32 bit, or
```
PS C:\Hilltop> .\x64\Libs\python.exe -m pip install .\Plugins\samplerqrgenerator-0.1.1.whl
```
for the 64 bit version.

Finally you need to specify the directory to which the plugin with save the qr code files that it creates. This configuration can be placed in your `HilltopSystem.dsn` file, under the `[Sampler]` heading, like this:

```
[Sampler]
LabelOutputDir = \\directory\for\qr\code\output
```

# Build instructions

This section is for developers who want to build the source binaries for release.

Due to the two supported architectures, we need to make separate releases for 32 and 64-bit  architectures. Unfortunately this information cannot be passed as "platform" specifications as this will block installation of the wheel on a machine that doesn't have a CPU architecture that agrees with the Hilltop architecture. 

For that reason we can specify the Hilltop architecture as a `build-number`, which is just a suffix to the version number used to differentiate different builds of the same version. This can be passed to the build backend with the following build command: 

```
../../x64/Libs/python.exe -m build -w -C="--build-option=--build-number 64bit --python-tag py310" -n .
```

We'll use the convention that a build number of `32bit` is a plugin intended for the 32 bit Hilltop, and build number `64bit` is for 64 bit Hilltop.

Note that the above command also specifies the python version. This is just a failsafe that might prevent installations of the plugins using other python interpreters installed on the user's system. 
