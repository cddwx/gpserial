# Description

A client program for a step motor control system.

![主界面](main.png)


# Develop environment

* Python 2.7.13
* pyserial 3.0.0(Make it work under windows XP)
* wxPython 4.0.0a1
* PyInstaller 3.3

# PyInstaller build guide

Under project root, execute the following command

~~~~
mkdir build
cp pyinstaller_build/* build
cd build
make
~~~~

Then PyInstaller will generate "build" and "dist" directories, and a "*.spec" file, your executeable program is laying under dist/MAIN_SCRIPT. directory.

# PyInstaller note

For pubsub package at least in wxPython 3.0.1.1 and 4.0.0a1, though Pyinstaller has related hooks, it now not only cannot handle it correctly, but make trouble, so I disable the hooks(mv hooks-wx.lib.pubsub.py to hooks-wx.lib.pubsub.py.bak) and write one pre_safe_import_module hooks in my project(under PROJECT_DIR/pyinstaller_build/hooks directory), it works fine for me.
