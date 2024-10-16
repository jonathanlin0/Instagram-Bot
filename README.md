
# About
This app contains two main parts. The first part is the root directory of this repo. It is a tool for you to automatically scrape the trending stories on reddit, generate a video of a person narrating the story with a customizable background, and post it to Instagram.

The second part is a tool you can run to increase your Instagram followers automatically. I created this program in high school (was one of my first projects), so the code is a little messy. The program exploits user behavior to increase your Instagram followers with real people. An example is that people like following users who follow celebrity accounts, so one of the strategies is to continuously follow and unfollow celebrity accounts (follow and unfollow because the followers list is chronological). Another example is that people follow people who engage in their posts, especially if the post doesn't have many likes or comments. So another algorithm is to like and/or comment on specific posts with little amount of engagement.

# Project 1

## Getting Started

### Environment File
Change the `.env` file. `USERNAME` is your Instagram username and `PASSWORD` is your Instagram password. Reels are automatically created and posted based on a random schedule. The program will periodically post to your account, and the paused time between each post is normally distributed. `AVG_SLEEP_TIME_HOURS` is the mean of this sleep normal distribution, and `VARIANCE_SLEEP_TIME_HOURS` is the variance of the normal distribution. `MIN_SLEEP_TIME_HOURS` is the minimum time to sleep, and `MAX_SLEEP_TIME_HOURS` is the maximum time to sleep (both of these variables are done to protect against tail events).

### Other Settings
- Fill in `subreddits.txt` with a list of subreddits you want to grab posts from. Put each unique subreddit on a new line, like how it currently is.
- Fill out `replacements.json`. This file is a dictionary/hashmap that maps the original word to the word you want to replace it with when captioning. This feature exists mainly to censor profanity or derogatory language.
- Grab a video, whether it's your own or a free to use public video, and put it into the root directory. Name it `bg_vid.mp4`

### Run
Make sure you have all the needed packages installed using pip. Then run `python auto_post.py`

### Automatically Unfollowing Users
Completely unrelated to either project, you can run `python growth/unfollow.py` to unfollow everyone you're currently unfollowing. The account it uses is the one you set in `.env`.

## File Descriptions

You don't need to read this. Not really relevant to using the program. I just keep it in case I ever return to this project.

`gen_audio_subtitle.py` generates the audio and subtitle files to be used later in the process.

`gen_vid.py` generates the actual video based on existing data files

`auto_post.py` automatically posts reels to Instagram.

`reddit_fetcher.py` grabs stories from reddit.

`stories.json` stores all the reddit posts you've posted using this software

`to_be_processed.json` holds the stories that have been scrapped but not been posted yet.

`bg_vid.mp4` replace with the actual background video. The program will automatically pick a place to start for the background when the video is being generated.

`output_audio.mp3` the text to speech audio that is produced.

`thumbnail.png` The thumbnail of the video that is created.

`replacements.json` are all the words you want to replace. It's a dictionary to map the original word to the word you want to replace it with. It's typically used for profanity or dergatory language.

`subreddits.txt` are the subreddits that you want to grab information from.

`title_length.txt` The time it takes for the audio to state the title. Is formatted weirdly. Automatically produced.

`growth/followed.txt` serves as a cache for the user IDs of users you've followed.

`growth/unfollowed.txt` serves as a cache for the user IDs of users the program has unfollowed for you.

`growth/unfollow.py` automatically unfollows users. Grabs from `growth/followed.txt` and unfollows the people on that list. Once you've unfollowed them, the user ID is added to `growth/unfollowed.txt`. When the `growth/unfollow.py` is first run, it checks if the following cache is empty. If it is, then it'll ping Instagram's servers to update the list of people you're following.

# Project 2

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

### Notes for customers who bought the *source code* along with the bot
##### Ignore if you only bought the bot

How to convert this ig-bot.py into an exe file:
Open up command and navigate to the folder holding the current .py file. Then do "pip install pyinstaller". Afterward, do "pyinstaller ig-bot.py --onefile". This step may take a few minutes depending on the speed of your computer. Afterward, there should be a bunch of new folders. If you navigate to the folder called "dist", you will find your ig-bot.exe file.

Needed if you want to run the raw .py file:
1. pip install InstagramAPI

Note: depending on your OS and/or python version, you may have to do "pip3 install {module}" instead of just "pip install {module}".


Disclaimer: The programs in this repository rely on private APIs to connect to Instagram's servers.