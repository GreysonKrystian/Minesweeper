# Minesweeper

![alt text](https://forthebadge.com/images/badges/made-with-python.svg)

# Table of contents


- [Requirements](#requirements)
- [Project description](#project-description)
- [Possible future improvements](#possible-future-improvements)
- [Screenshots](#screenshots)
- [License](#license)


# Requirements

Project should be build in Python3. Moreover, the project requires modules included in [Requirements.txt](requirements.txt) to build. 

# Project description

[(Back to top)](#table-of-contents)

The project is my implementation of popular classic game minesweeper. More info about game can be found [here](https://en.wikipedia.org/wiki/Minesweeper_(video_game))
It was created as one of my university one-person projects in 2020/2021 semestr. The main aim of projects was to learn fundamentals of OOP and Python.
Projects is written in Python3 with UI created in [QT](https://www.qt.io) module for python (PyQt).

Project consists of several main modules:
- Game
- Board
- Classes of game entities
- Difficulty UI
- main UI
- tests

*Game* - Wrapper for entieties, contains functions responsible for checking if game should end and calculating statistics.
*Board* - Intializes game board with configuration chosen by player.
*Entities* - Classes responsible for managing game entites such as flags, mines etc.
*Difficulty UI* - Qt class that manages starting screen where player chooses difficulty of the game 
*Main UI* - Main qt class which displays window with actual game.


# Possible future improvements

[(Back to top)](#table-of-contents)

It was my first bigger programming project so there are many topics in this project which could be improved.
These main topics are:
- code readability and reusability - the code has some issues when comes to following design priciples. In project
 we can some violations of DRY principle. Moreover number of indentations in some functions makes code harder to read and debug.
- not using appropriate python modules - game engine can be improved with Numpy. It will also decrease indentation hell.
- better UI - The Qt design used in project looks quite primitive and could be improved. Alternative solution is to completly change 
framework to for example PyGame.
- create Mobile/Web version of the game.


# Screenshots

[(Back to top)](#table-of-contents)

<strong>MENU</strong>:
<br>
<p align="center" width="100%">
<img alt="Screenshot from menu" src="https://raw.github.com/GreysonKrystian/Minesweeper/master/Example%20Photos/Menu_1.png" width=800 height= auto>
<br>
<br>
<img alt="Screenshot from menu" src="https://raw.github.com/GreysonKrystian/Minesweeper/master/Example%20Photos/Menu_2.png" width=800 height= auto>
</p>

<strong>GAMEPLAY</strong>:
<br>
<p align="center" width="100%">
<img alt="Screenshot of gameplay" src="https://raw.github.com/GreysonKrystian/Minesweeper/master/Example%20Photos/Gameplay_1.png" width=800 height= auto>
 <br>
 <br>
<img alt="Screenshot of gameplay" src="https://raw.github.com/GreysonKrystian/Minesweeper/master/Example%20Photos/Gameplay_Won.png" width=800 height= auto> 
<br>
<br>
<img alt="Screenshot of gameplay" src="https://raw.github.com/GreysonKrystian/Minesweeper/master/Example%20Photos/Game_Ended.png" width=800 height= auto>
<br>
<br>
</p>





# License

[(Back to top)](#table-of-contents)


The MIT License (MIT) 2022 - [Krystian Grela](https://github.com/GreysonKrystian/). Please have a look at the [LICENSE.md](LICENSE.md) for more details.
