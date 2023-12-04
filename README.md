# Coup
CLI version of the popular game Coup written in Python


## Index

* Introduction
* Set-up
  * Native Python
  * Conda
  * Pyenv
* Discussion
* Limitations
* Future Work

## Introduction

This is a Command-Line-Interface version of the game Coup. This project encapsulates most of the original games functionality (as already mentioned), with a few minor differences

## Set-up

The set-up is really straight-forward since I ended up using native Python in VSCode. This was done using Python 3.10.11, and the only import needed (outside of the classes I created) is random, which is also native Python - so super easy!


### Native Python

This is how I set it up on my laptop, but for everything else I tend to use a miniconda environment 

1. Download and install Python 3.10.11 -> https://www.python.org/downloads/
2. Download the files that are in this repo, and be sure to keep them in the same parent folder!
3. Open up a terminal for an Ubuntu/Mac machine, or Powershell for a Windows machine
4. Navigate into the directory that you downloaded in Step 2 from the terminal (i.e. for me the command is cd /Documents/Coup where Coup is the parent folder I mentioned earlier - but that will probably be different for you)
5. Type python interface.py in the terminal
6. Press enter
7. Enjoy, and may the odds be ever in your favor!

### (Mini)conda

Anaconda and the far superior (in my opinion) Miniconda are alternative ways to also set up an environment where the code from this will be independent from other environments you may need. This is important because some Python programs could use 3.7, and others could use 3.12, and the different versions can break if downloaded together and mishandled. The main differences are what comes with each. Anaconda comes with a lot of stuff, so it tends to be rather bloated, but Miniconda is a lightweight version that allows you to pick only what you want to install

Anaconda download link - https://www.anaconda.com/products/individual

Miniconda download link - https://docs.conda.io/en/latest/miniconda.html

1. Install Anaconda or Miniconda using the link(s) above
2. conda create -n myenv python=3.10.11 - enter this command in terminal/Powershell this creates a specific environment called myenv (which is swappable) that has Python 3.10.11 set up. You can install multiple environments side by side that don't interfere with each other
3. conda activate myenv - (or if you changed the name be sure to swap myenv for the new name), but this is also a terminal/Powershell command
4. Start at Step 2 from the Native Python section right above

### Pyenv

Pyenv is an alternative to conda that is also really popular

Pyenv download link - https://github.com/pyenv/pyenv#installation

1. Install Pyenv using the link above
2. pyenv install 3.10.11 - terminal/Powershell command to set up the python environment
3. pyenv local 3.10.11 - terminal/Powershell command
4. Start at Step 2 from the Native Python section above

#### Conda vs Pyenv

Conda takes up more space than Pyenv because Conda is a package and environment manager, whereas Pyenv is just an environment manager and doesn't handle dependencies 

## Discussion

I'd like to share a few insights/reflections from the development process of this game. I ended up capturing most of the gameplay for this game. I took a few liberties when I created it (i.e. if you use the exchange function, you have to swap both of the cards, versus in the game I'm pretty sure you can swap one or two) - guesstimating that over 90% of the functionality of the original game is included in the backend. I also ended up creating an abstraction for a general character class that could be extended to all characters as GPT4 made some really good points and was unusually insistent upon that part. The design process was easy for me as I usually keep things as simple as they need to be, and as modular as possible without going overboard. I did consider splitting up part of the GameManagement class, but I felt like the logic of it wasn't too hard so it wasn't quite necessary. 

Capturing Coup's gameplay in digital form was key here, so understanding the rules and applying them to Python was a great way to showcase how flexible and strong Python really is! Since the UI is CLI, it had to be clear and user-friendly so that the player/user has all the necessary information in a concise and readable way. Overall, I think the trade-offs I made (choosing to focus on the backend and certain rules) were worth it as the CLI is simple and clean while maintaining the main flow of the game. 

## Limitations

I think the biggest challenge for me in this exercise was the fact that I had never heard of, let alone played, Coup. I had to implement the logic of the game while learning it / after reading about it - slightly challenging, but overall fun!

## Future Work

Here are some improvements that I think could make the game experience for this program better in the future

### Low Hanging Fruit

* The UI could have been done a few different ways and I initially wanted to build a UI, but I ended up choosing a text-based game due to time constraints
* The code could be improved in a few ways - right now it wasn't built with scalability in mind, nor is it optimized in general (i.e. copying and pasting the action_to_card_map dictionary in two different functions in the Player class), so improving reusability would be a big help too
* Expanding the number of players to match the game, where you can choose X number of humans and Y number of bots to play against
* Giving an option to go back - right now there is no way to cancel a command or a choice, but I think adding one in for the future would be beneficial
* More comprehensive unit testing - I chose to do enough to showcase how I approach it, but decided not to spend more than 5 minutes on it. 

### Everything else

* Separation of concerns is mostly implemented, but I think there are a few parts where the game logic and UI logic could be decoupled a little more
* Another improvement that could be made is training a model to play against as an AI, rather than just a random choice that it currently is
* The rules could be added to the game so a new player, or someone who hasn't played in a while, could learn the rules/get a refresher
* Integrate the last few things from the original game I didn't include
* Integrate the expansion pack as an option
* I think more docstrings and comments would be helpful to make things clear, but overall the current comments/docstrings/naming conventions should be really straightforward
* Save feature, undo/redo feature (maybe only against AI)
* Successful/failing actions are repeated in the logs so it is redundant but harmless - in the future I could remove the redundancies
* Since the AI repeats some actions that fail, it would be good to add a mechanism to prevent this, but overall it only delays the game by a few seconds so it is harmless

