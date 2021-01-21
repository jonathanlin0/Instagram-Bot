## About
This Instagram Bot came to be when I was researching methods on how to grow an Instagram account. Most of the methods I came across seemed very tedious and I felt like I could do something about it. Also, half the videos involved a paid service that I thought would not be so hard to make. After 3 different versions (console based -> pygame -> tkinter), the bot is finally finalized and put on github for everyone to enjoy! I hope you find this bot useful and you learn something from it

### Make sure all files are in one and the same folder!
Keep the README.txt, config.txt, etc files all in the same folder as the ig-bot.exe file. If not, there will be errors and you will be unable to run the program.

#### Category Key
 [1] Memes
 [2] Art
 [3] Soccer
 [4] Basketball
 [5] Baseball
 [6] luxury
 [7] Travel
 [8] Technology
 [9] Gaming
[10] Minecraft
[11] Cars

#### Additional Important Notes
Needed files that have to be in the same file as ig-bot.py or ig-bot.exe for running the .exe file:
1. generated hashtags.txt (this is where your generated hashtags go)
2. config.txt (for bot settings)
3. README.txt (this file)
4. other.txt (for storing other information regarding the program)
5. ig-bot.py or ig-bot.exe (whichever one you purchased)
6. icon.ico

When you open up the program, the program will load for up to a minute (depending on the speed of your computer). During this time, the software is loading all the required data to work. The generated hashtags will appear in the "generated hashtags.txt" file. Click the pause button to pause ALL actions. Press the button again to resume all actions (this button is a toggle).

### Notes for customers who bough the *source code* along with the bot
##### Ignore if you only bought the bot

How to convert this ig-bot.py into an exe file:
Open up command and navigate to the folder holding the current .py file. Then do "pip install pyinstaller". Afterward, do "pyinstaller ig-bot.py --onefile". This step may take a few minutes depending on the speed of your computer. Afterward, there should be a bunch of new folders. If you navigate to the folder called "dist", you will find your ig-bot.exe file.

Needed if you want to run the raw .py file:
1. pip install InstagramAPI

Note: depending on your OS and/or python version, you may have to do "pip3 install {module}" instead of just "pip install {module}".
