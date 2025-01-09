# Tactigon Shapes

Tactigon Shapes is an extension of [Blockly](https://developers.google.com/blockly) which is a project by Google and it allows you to create visual, drag-and-drop block-based programming interfaces. Instead of typing code, you can create programs by connecting blocks together. From Tactigon Shapes you can generate code in JavaScript, Python, PHP, or Dart based on the visual blocks. But we recommend using Python because almost all of our projects speak Python. 

### Key Features of Tactigon Shapes:
- Visual Programming: Drag-and-drop interface that helps users understand programming concepts.
- Code Generation: Automatically generates code in multiple programming languages.
- Customizable: You can create your own blocks and define their behavior.

## Tactigon Ecosystem

Tactigon ecosystem is consists of:
 - [Tactigon Gear](https://pypi.org/project/tactigon-gear/) to connect to a Tactigon Skin wearable device and do gesture recognition
 - [Tactigon Speech](https://pypi.org/project/tactigon-speech/) to implement voice recognition on top of Tactigon Gear
 - [Tactigon Arduino Braccio](https://pypi.org/project/tactigon-arduino-braccio/) to connect to the Arduino Braccio device

## Requirements

In order to use the Tactigon SDK the following prerequisites need to be observed:

### Instructions for Mac/Linux:
To set the required tools on your system, follow the steps below:

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
Open the Visual Studio Installer on your system. if you do not have one, [Download Visual Studio Installer](https://visualstudio.microsoft.com/downloads/)
- From the Visual Studio Installer, click Modify or select Install for new installation.
- Go to the individual components tab and install the latest version 
  - MSVC v143 - VS 2022 C++ Build Tools x64/x86 (latest version)
  - Windows 10/11 SDK (latest version matching your Windows version)

![Screenshot 2024-11-21 162339](https://github.com/user-attachments/assets/5f6332f1-be2b-4fee-ad62-7feb734db710)

## Clone Tactigon Shapes

1. Copy the URL for HTTPS by clicking the Code button.

![image](https://github.com/user-attachments/assets/bc9664eb-ba03-4ad4-b11d-9f29fcdd2289)


2. Open the Command Line for Windows or Terminal for Mac/Linux and run the following command.

```
git clone https://github.com/TactigonTeam/Tactigon-Shape.git
```

![image](https://github.com/user-attachments/assets/7027d8b3-9388-4f67-a7f9-fb967fa49b1d)

3. Navigate to the Tactigon SDK folder and open the project with your favorite code editor.

![Code_0JguwTxnH2](https://github.com/user-attachments/assets/18b8e6d9-e264-4730-bd16-f29607859186)

## Create Virtual Environment
It is recommended to create a dedicated Python virtual environment and install the packages into it. 

To create a virtual environment, run the following code.
```
python -m venv venv
```

If your operating system is MacOS or Linux you can activate the virtual environment by running this command.
```
source venv/bin/activate
```
For Windows users, you can execute this command to activate the Virtual Environment.
```
.\venv\Scripts\activate
```

Depending on your installation (Linux, Raspberry, Mac users) you may need to use `python3` and `pip3` instead of `python` and `pip` respectively.

## Install

To install the correct dependencies it is mandatory to follow the following step:
```zsh
pip install flask==3.0.3 flask_socketio==5.3.6 gevent==24.2.1 tactigon_gear==5.2.0 PyAudio==0.2.13 pynput==1.7.7 sympy==1.13.2
pip install deepspeech-tflite==0.9.3 --no-deps
pip install tactigon_speech==5.0.8.post1 --no-deps
```
![image](https://github.com/user-attachments/assets/94d27fbe-58fe-4519-9127-b97bac8677c5)

## Run Tactigon Shapes 
1. Simply execute the main.py by running the following command.
```
python .\main.py
```
![image](https://github.com/user-attachments/assets/b279bc37-f1ba-4714-bf09-233f1ac90837)

2. Open the web browser and type this http://127.0.0.1:5123 on the search bar. You will see a page where you can connect to TSkin device.

![image](https://github.com/user-attachments/assets/e576893d-e499-4b2f-aeae-d825a4102087)

3. Once you complete the initial configuration, then you will be redirected to the Shapes page.

![image](https://github.com/user-attachments/assets/4449bfb8-4473-467d-8231-e9a83dfc53fa)

## How to use Shapes

Using Shapes is like building with LEGO bricks, you drag, drop, and connect pieces to create something functional. This section guides you step-by-step on how to use shapes.

### Once you are on the Home webpage.
- On this page, you can see some of our example shapes, such as Powerpoint, Braccio voice, and so on.
- On the left side, you will see all your shapes, and on the right side, you can see the snapshot of your shape.

### Create New Shape
- Click the Add Shape button, and you will see a popup window to enter a name and a description.
- The shape name should be unique. Now, click on the Add Shape button.
- You will be redirected to the edit page where you can modify your shape. Here you can either modify the shape or click save.
- If you successfully created your shape, you will be redirected to the home page with a success notification.

https://github.com/user-attachments/assets/65e7d149-e559-4a5b-a746-5a0868d2227e

### Edit Shape
- Click on the shape you want to modify and click the Edit code button on the right side to modify the shape. You will be redirected to the edit workspace where you can change your shape.
- On the left, you will see categories like Logic, Math, Gesture, Touch, etc. When you click a category, you can see all the blocks related to that category.
- Select a category and drag one of the blocks into the workspace. For example, in the Touch category, you will find a hand gesture block which gives you the finger gesture from the TSkin device.

Think of blocks like puzzle pieces. This means you can now connect them by dragging one block and placing it under or inside another block. However, ensure that your shapes snap together; otherwise, the program will not execute.

https://github.com/user-attachments/assets/d8b41a1d-e9d1-4bbe-afb6-de68e38764ab

### Run Your First Shape
- When you are done building, click the toggle button to see what your program does.
- You will see a page with both your shape and the terminal with the output.

https://github.com/user-attachments/assets/6cc84398-4954-4650-b0ad-2eb0e861bfb6

### Delete Shape
- You can delete the shape by clicking the bin icon next to shape name.
  
![image](https://github.com/user-attachments/assets/ccdb6c47-4b53-4894-a19b-7ac307c63a00)

## How to create your own blocks in Tactigon Shape

We'll walk you through how to create the block and handle the Python code generation. The easiest step is to create your custom blocks on the Blockly Developer website:  [Blockly Developer Tools](https://developers.google.com/blockly/guides/create-custom-blocks/blockly-developer-tools). This platform provides an intuitive interface for defining block shapes, fields, and behavior without needing to write code manually. You can customize the block's appearance, input types, and logic connections. Once your block is designed, the tool generates the corresponding JSON and JavaScript code, which can be easily integrated into Tactigon Shapes project.

### Steps to Create Custom Blocks

1. **Create a Category (Optional)**  
   - If you want to organize your blocks, you can create a new category or assign your block to an existing category.  
   - To create a new category, go to the [Edit](https://github.com/TactigonTeam/Tactigon-Shape/blob/master/tactigon_shapes/modules/shapes/templates/shapes/edit.jinja) page in the **Shape** module.

```
  <category name="To Uppercase" colour="#f1c40f ">
      <block type="to_uppercase">
      </block>
  </category>
```

2. **Design Your Block**  
   - Use the Blockly Developer Tools to create your new block by customizing its inputs, logic, and appearance.  
   - Once done, copy the generated JSON code for your block.
```
 Blockly.Blocks['to_uppercase'] = {
        init: function () {
            this.jsonInit({
                "type": "to_uppercase",
                "tooltip": "",
                "helpUrl": "",
                "message0": "To Uppercase %1",
                "args0": [
                  {
                    "type": "input_value",
                    "name": "TEXT",
                    "check": "String"
                  }
                ],
                "previousStatement": null,
                "nextStatement": null,
                "colour": '#f1c40f'
              });
        }
};
```

3. **Add the Block to Tactigon Shapes**  
   - Paste the JSON code into the [Custom blocks file](https://github.com/TactigonTeam/Tactigon-Shape/blob/master/tactigon_shapes/modules/shapes/static/js/custom_blocks.js) page in the **Shapes** module.  
   - After adding it, you will see both the new category (if created) and the new block in the Tactigon Shapes workspace.

![image](https://github.com/user-attachments/assets/711d0e14-5972-4583-bb06-41b1fcb64ad7)

4. **Write Custom Code for the Block**  
   - You can create custom Python code for your block in the [Custom blocks file](https://github.com/TactigonTeam/Tactigon-Shape/blob/master/tactigon_shapes/modules/shapes/static/js/custom_blocks.js) page in the **Shapes** module.
```
    python.pythonGenerator.forBlock['to_uppercase'] = function(block) {
        var text_to_print = Blockly.Python.valueToCode(block, 'TEXT', Blockly.Python.ORDER_ATOMIC) || "''";
        var code = `debug(logging_queue, ${text_to_print}.upper())\n`;
        return code;
    };  
```

5. **Run and Test**  
   - After creating your block, rerun the project and test your block by running your shape.

![image](https://github.com/user-attachments/assets/f71ef35e-48df-4880-a7dd-e257b713105b)

Here we have attached a demo video about how to create your own block in the Tactigon Shapes project.

https://github.com/user-attachments/assets/f0057429-2cc8-4c83-92eb-250ed9f52483
