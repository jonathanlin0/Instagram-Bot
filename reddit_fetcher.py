import requests
import json
import emoji
from time import sleep

class RedditStoryFetcher:
    def __init__(self, subreddits_file, existing_stories_file, max_num_tries=5, min_upvote_ratio=0.9):
        self.subreddits_file = subreddits_file
        self.existing_stories_file = existing_stories_file
        self.max_num_tries = max_num_tries
        self.min_upvote_ratio = min_upvote_ratio
        self.stories = []

    @staticmethod
    def replace_emojis(text, replacement=""):
        return emoji.replace_emoji(text, replacement)

    @staticmethod
    def process_text(text):
        return RedditStoryFetcher.replace_emojis(text.replace("\n", " ").replace("\u2019", "'").replace("\u201c", " ").replace("\u201d", " ").replace("AITA", "Am I the asshole"))

    def fetch_stories(self):
        with open(self.subreddits_file, "r") as f:
            subreddits = f.read().split("\n")
        
        assert len(subreddits) > 0 and subreddits[0] != ""

        for subreddit in subreddits:
            print("")
            print(f"Getting stories from r/{subreddit}")
            for i in range(self.max_num_tries):
                r = requests.get(f"https://www.reddit.com/r/{subreddit}/top.json?t=month?limit=99", headers={'User-agent': 'Mozilla/5.0'})
                if r.status_code == 200:
                    print(f"Successfully downloaded stories from r/{subreddit}")
                    break
                else:
                    print(f"Error downloading stories from r/{subreddit}: {r.status_code}. Trying again...")
                    sleep(1)

                if i == self.max_num_tries - 1:
                    print(f"Failed to download stories from r/{subreddit} after {self.max_num_tries} tries.")
                    print("Exiting to prevent ratelimits...")
                    exit()

            data = r.json()
            raw_stories = data["data"]["children"]

            for story in raw_stories:
                clean_title = self.process_text(story["data"]["title"])
                clean_text = self.process_text(story["data"]["selftext"])

                # limit length of text to 1450 characters (so under 90 seconds of audio)
                # check that text (story) is at least 10 characters, so that it's not like a caption
                # limit length of title to 800 characters (so title is under a minute)
                if clean_title and len(clean_text) <= 1450 and len(clean_text) > 20 and len(clean_title) <= 800:
                    self.stories.append({
                        "title": clean_title,
                        "text": clean_text,
                        "ups": story["data"]["ups"],
                        "upvote_ratio": story["data"]["upvote_ratio"],
                        "subreddit": story["data"]["subreddit"],
                        "permalink": story["data"]["permalink"],
                        "created": story["data"]["created"],
                        "id": story["data"]["id"]
                    })

    def save_stories(self, output_file):
        # sort stories by upvote ratio
        self.stories = sorted(self.stories, key=lambda x: x.get('upvote_ratio', 0), reverse=True)

        # remove stories with low upvote ratios
        self.stories = [story for story in self.stories if story["upvote_ratio"] >= self.min_upvote_ratio]

        # remove stories that already exist
        existing_stories = json.load(open(self.existing_stories_file, "r"))
        existing_ids = [story["id"] for story in existing_stories]
        self.stories = [story for story in self.stories if story["id"] not in existing_ids]

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.stories, f, ensure_ascii=False, indent=4)

    def run(self, output_file):
        self.fetch_stories()
        self.save_stories(output_file)

if __name__ == "__main__":
    fetcher = RedditStoryFetcher("subreddits.txt", "stories.json")
    fetcher.run("to_be_processed.json")