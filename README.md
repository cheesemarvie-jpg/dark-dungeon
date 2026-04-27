# Dark Dungeon



## Overview



Dark Dungeon is a 2D dungeon exploration game developed with Python and Pygame.



The player explores a randomly generated maze while managing limited visibility and items.

The game focuses on exploration under darkness and strategic use of skills and items.



## Environment



* Python 3.13.7
* pygame 2.6.1
* Windows 11



## How to Run



Install dependencies:



pip install -r requirements.txt



Run the game:



python main.py



Alternatively, run the executable in the bin folder.



## Controls



WASD : Move

Enter : Screen transition,  Use item

ESC : Quit



## Project Structure



source/

 main.py	Entry point of the game

 config.py	Global configuration values



 scene/		Scene management system

 	base\_scene.py

 	start\_scene.py

 	game\_scene.py

 	skill\_select\_scene.py

 	result\_scene.py

&#x09;pause\_scene.py

&#x20;	waiting\_scene.py

&#x20;	tutorial\_scene.py

 maze/		Maze generation

 	maze.py

 	maze\_generater.py

 entities/	Game objects such as player and dungeon structure

 	player.py

 	goal.py

 	gage.py

 	dark.py

 	chest.py

 	wall.py

 	route.py

 	broken\_wall.py

 	spotlight.py

 	mainlight.py

 	wisp.py

 systems/	Gameplay systems

 	item.py

 	skill.py

 	status.py

 	text\_sprite.py

&#x09;font/	font file



## Technical Features



### Random Maze Generation

The dungeon layout is procedurally generated at runtime.



### Lighting System

The player can only see within a limited area, merge black screen and light objects to implement.





 

