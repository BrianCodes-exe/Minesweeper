<a name='Minesweeper'></a>
# Minesweeper

![Image of a flagged tile in Minesweeper](https://raw.githubusercontent.com/BrianCodes-exe/Minesweeper/main/images/flagged.ico)

# Table of Contents
- [About this Project](#About)
  - [Built With](#Builtwith)
- [Usage](#Usage)
  - [Help Installing Python](#HelpInstall)
- [The Game](#Thegame)
  - [Features](#Features)
  - [Algorithms](#Algorithms)
- [Additional Information](#AddInfo)
  - [Basics of the Game](#Basics)
  - [The Struggles and Issues](#Struggles)
  - [To Do & Add Features](#ToDo)

<a name="About"></a>
# About this Project
<p>This project consists of a Python program that uses Tkinter (a python widget library) to run rounds of the old yet popular video game Minesweeper. I had originally created a terminal (non-gui) version of Minesweeper in C++ for my CS 135 assignment. So, I wanted to take my programming skills to the next step by creating a program that runs games of Minesweeper with Graphical User Interface.</p>

<a name='Builtwith'></a>
## Built With
<p>The one and only language used for this project was Python (v3.8.2). The imported libraries were:</p>

```
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
```

1. ***Tkinter*** is a Python library that acts as a GUI toolkit that contains the ***Tk*** and ***Tcl*** classes to load in different widget objects.
2. ***Messagebox*** module that is supported by the ***Tk*** class is used as a pop up message within the program to inform or request additional information from the user.
3. The ***Image*** and ***ImageTk*** modules from ***PIL*** were needed as only .gif images were supported for the ***Tk*** class, while for my program .png files were used. So, ***ImageTk*** was needed to open and use the .png images for the tiles.
4. The Python's Generate Pseudo-random Numbers library ***Random*** was used to generate random coordinates on the board to place the mine.

<a name='Usage'></a>
# Usage
<p>In order to run the program, you must have the Python Interpreter installed on your device and added to your path. (If you are using a device with Mac OS or Linux, it is highly likely that Python is already pre-installed on your device.</p>
<p>To check if you have Python installed just open up your terminal and type in:</p>

`python --version`

<p>If you do not have Python installed and need further help, read the section below. ↓↓↓↓↓↓</p>

<a name="HelpInstall"></a>
## Installing Python
1. First go to this [link](https://www.python.org/downloads/release/python-382/) to download the Python version used for this program. 

*Previous versions of python, such as python v2 may not run the program properly as some functions and syntax used in the program are python v3 specific.*

2. Then, when Python is being installed, make sure to check the box where it says **Add to path**. This will make sure the Python interpretor is added to the system path so that you can run the python command on the terminal.

3. Once, Python is now installed, make sure python is properly installed on your device by typing into your terminal:

`python --version`

4. Once it shows the version of Python you installed, you can download the source code for this program and run this command into the path you have the source code.

`python minesweeper.py`

5. Congrats! You're all set to use the program.

<a name='Thegame'></a>
# The Game
<p> <strong><i>Minesweeper</i></strong> is a very fun game that can get addicting sometimes as the game gets harder with more tiles and more mines on the field! In order to make Minesweeper an enjoyable game, it comes with certain basic features (Some that are known to the users and others not), such as difficulty and different sized boards, being able to restart or reload the board, and making sure that the first tile picked by the user isn't a mine. Along with those features, the game includes a few algorithms that helps the game run smooth and quick, with no bugs.</p>

<a name='Features'></a>
## Features
1. **Difficulty**. </br>
![Show Difficulty Menu Bar](https://github.com/BrianCodes-exe/Minesweeper/blob/main/images/readme_images/difficulty_tab.png?raw=true)
<p>Once the program is up and running, the Minesweeper window will open up with a default of beginner difficulty. You can choose a different difficulty by clicking the difficulty tab on the menu bar and the board will automatically reload the board.</p>

 - **Beginner** -9x9 Board with 10 mines-
 - **Intermediate** -16x16 Board with 40 mines-
 - **Hard** -16x30 Board with 99 mines
 - **Expert** -20x30 Board with 145 mines-

2. **First Picked Tile** </br>
![First picked tile](https://github.com/BrianCodes-exe/Minesweeper/blob/main/images/readme_images/first_pick.png?raw=true)
<p>This feature is a simple but hidden feature that makes sure that the first picked tile by the user is never a mine. In most versions of Minesweeper nowadays, this feature is included, but it was never a requirement. However, it is still nice to have this feature so that the user doesn't accidently pick a tile with the mine on their first pick and have the game be over right away.</p>

3. **Other Features** </br>
This project is still pretty new in development and was created just for fun, but that doesn't mean more features won't be added. Stay in tune for more features to come out. Check the [To Do & Add Features](#ToDo) section for more features that are expected to come out.

<a name='Algorithms'></a>
## Algorithms
### UML Diagram for Class Minesweeper
![UML Diagram for Minesweeper Class](https://github.com/BrianCodes-exe/Minesweeper/blob/main/images/readme_images/uml.png?raw=true)
<p>For the main solution of this program a Class named Minesweeper was created, inherited off of the Tk class included in the tkinter library. The class has 4 main methods to ensure that the game functions properly.</p>

1. **Initialize variables and set up the game**
<p>The constructor will initialize most of the class variables while creating the display window for the game and making sure the difficulty is set to the one the user wants. Then, setup_game will make sure that the board is created of the tiles based off the difficulty.</p>

2. **Take in user input and allow program to respond**
<p>The on_click and on_flag functions will be called whenever the user left or right clicks a tile. However, for the first picked tile, the initialize_mines function will be called to place mines in random tiles except the user selected tile. This is to ensure that one of the features work properly. Afterwards, these two functions will still continue to get called for each user click, while always checking if the conditions for the game ending is true.</p>

3. **Run the main gameplay algorithm**
<p>The check_nearby and surrounding functions get called as each tile is clicked on. These two functions are the main gameplay algorithms that show the users how many mines are near the tile and if the tile that is clicked on has a mine itself.</p>

4. **Check the game results**
<p>Whenever the condition for a game ending scenario is met, the gameover function is called. If the user had clicked on a mine, then a messagebox will pop up informing that the user has clicked on a mine and it will reveal all the locations of the other mines. Otherwise, if the user has flagged all the tiles with the mines, then a messagebox will pop up informing that the user has won the game.</p>

<a name='AddInfo'></a>
# Additional Information
<p>Below additional sections about the project such as additional features I plan on adding to the program.</p>

<a name='ToDo'></a>
## To Do & Add Features
1. Add a restart button that reloads the board smoothly, without having to restart using the difficulty tab.

2. Add a timer to keep track of highscores on a separate txt files.

[Back to the Top ↑↑↑↑↑](#Minesweeper)
