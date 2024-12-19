# Tactigon Shapes

Tactigon Shapes is a VPS (Visual Programming System) that let you code programs to create natural interfaces using Tactigon ecosystem. It is made of a web application that hosts a customized version of [Blockly](https://developers.google.com/blockly?hl=it). Tactigon Shapes let's you build your program to use Tactigon Skin natural interface in a easy way.

## Tactigon Ecosystem

Tactigon ecosystem is made of:
 - [Tactigon Gear](https://pypi.org/project/tactigon-gear/) to connect to a Tactigon Skin wearable device and do gesture recognition
 - [Tactigon Speech](https://pypi.org/project/tactigon-speech/) to implement voice recognition on top of Tactigon Gear
 - [Tactigon Arduino Braccio](https://pypi.org/project/tactigon-arduino-braccio/) to connect to the Arduino Braccio device

## Requirements

In order to use the Tactigon SDK the following prerequisites need to be observed:

### Instructions for Mac/Linux:
To setup the required tools on your system, follow the steps below:

- CPU with AVX/FMA support
  - To check if your Mac supports **AVX/FMA** you can go to **About This Mac**. Check the CPU model and verify its features online.
- Git [Download Git](https://git-scm.com/downloads)
- Python 3.8.10 [Download Python 3.8.10](https://www.python.org/downloads/release/python-3810/)

### Instructions for Windows Users:
To set up the required tools on your Windows 10 or Windows 11 operating system, follow the steps below:
- CPU with AVX/FMA support
  - To check if your CPU supports AVX/FMA you can press **Win + R** then type **msinfo32** and press Enter. Check the CPU model and verify its features online.
- Git [Download Git](https://git-scm.com/downloads)
- Python 3.8.10 [Download Python 3.8.10](https://www.python.org/downloads/release/python-3810/)
- Microsoft C++ Build Tools and Windows 10/11 SDK. 

#### Microsoft C++ Build Tools and Windows 10/11 SDK installation
Open the Visual Studio Installer on your system. if you do not have, [Download Visual Studio Installer](https://visualstudio.microsoft.com/downloads/)
- From the Visual Studio Installer, click Modify or select Install for new installation.
- Go to the individual components tab and install the latest version 
  - MSVC v143 - VS 2022 C++ Build Tools x64/x86 (latest version)
  - Windows 10/11 SDK (latest version matching your windows version)

![Screenshot 2024-11-21 162339](https://github.com/user-attachments/assets/5f6332f1-be2b-4fee-ad62-7feb734db710)

## Install

To install the correct dependecies it is mandatory to follow the following step:
```zsh
py -3.8 -m venv venv
.\venv\Scripts\activate
pip install flask==3.0.3 flask_socketio==5.3.6 gevent==24.2.1 tactigon_gear==5.2.0 PyAudio==0.2.13 pynput==1.7.7 sympy==1.13.2
pip install deepspeech-tflite==0.9.3 --no-deps
pip install tactigon_speech==5.0.8.post1 --no-deps
```