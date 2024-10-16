import json
import numpy as np
from time import sleep

from reddit_fetcher import RedditStoryFetcher
from gen_audio_subtitle import AudioSubtitleGenerator
from post_to_insta import InstagramUploader

from gen_vid import VideoGenerator

from dotenv import load_dotenv
import os
load_dotenv()


USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

MIN_SLEEP_TIME_HOURS = 4
MAX_SLEEP_TIME_HOURS = 12
AVG_SLEEP_TIME_HOURS = 8
VARIANCE_SLEEP_TIME_HOURS = 2

SECONDS_IN_A_HOUR = 3600


if __name__ == "__main__":
    uploader = InstagramUploader(
        username=USERNAME,
        password=PASSWORD,
        session_file="session.json",
        video_file="video.mp4",
        thumbnail_file="thumbnail.png",
        caption_file="reddit_title.txt",
        hashtags_file="hashtags.txt"
    )
    uploader.login_user()

    while True:
        # fetch stories if there are none to be processed
        with open("to_be_processed.json", "r") as f:
            data = json.load(f)
            if len(data) == 0:
                print("No stories to be processed. Fetching new stories...")
                fetcher = RedditStoryFetcher("subreddits.txt", "stories.json")
                fetcher.run("to_be_processed.json")

        # generate audio and subtitles
        print("Generating audio and subtitles...")
        generator = AudioSubtitleGenerator(mode="system")
        generator.run()

        print("Generating video...")
        # generate video
        processor = VideoGenerator(
            video_file="bg_vid.mp4",
            audio_file="output_audio.mp3",
            subtitle_file="output_captions.vtt",
            title_file="reddit_title.txt",
            replacements_file="replacements.json",
            output_video="video.mp4",
            thumbnail_file="thumbnail.png"
        )
        processor.process_video()

        print("Posting to Instagram")
        # post video to IG
        uploader.upload_clip()

        print("Successful post!")
                
        # sleep time is normal distribution N(8, 2) hours
        # minumum 4 hours, maximum 12 hours
        sleep_time = np.random.normal(AVG_SLEEP_TIME_HOURS, VARIANCE_SLEEP_TIME_HOURS)
        sleep_time = np.clip(sleep_time, MIN_SLEEP_TIME_HOURS, MAX_SLEEP_TIME_HOURS)
        print(f"Sleeping for {round(sleep_time, 2)} hours...")
        sleep(sleep_time * SECONDS_IN_A_HOUR) # convert to seconds

        print("\n\n\n")