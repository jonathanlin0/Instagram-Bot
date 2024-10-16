import asyncio
from tqdm.asyncio import tqdm
import edge_tts
from moviepy.editor import AudioFileClip
import json

class AudioSubtitleGenerator:
    MAX_CHARS = 1500
    VOICE = "en-US-JennyNeural"
    AUDIO_OUTPUT_FILE = "output_audio.mp3"
    SUBTITLE_OUTPUT_FILE = "output_captions.vtt"

    def __init__(self, mode="system"):
        assert mode in ["system", "manual"]
        self.mode = mode

    def load_text(self):
        if self.mode == "system":
            print("Loading in story from to_be_processed.json")
            
            # get story from to_be_processed.json
            with open("to_be_processed.json", "r") as f:
                data = json.load(f)
                first_story = data[0]
                title = first_story["title"]
                story = first_story["text"]
            
            # write to appropriate files
            with open("story_title.txt", "w") as f:
                f.write(title)
            with open("story.txt", "w") as f:
                f.write(story)
            
            # remove first element from to_be_processed.json
            data.pop(0)
            # update files
            with open("to_be_processed.json", "w") as f:
                json.dump(data, f, indent=4)
            
            # story to stories.json
            with open("stories.json", "r") as f:
                stories = json.load(f)
                stories.append(first_story)
            with open("stories.json", "w") as f:
                json.dump(stories, f, indent=4)


    async def generate_audio_and_subtitles(self, text, audio_output_file=None, subtitle_output_file=None):
        audio_output_file = audio_output_file or self.AUDIO_OUTPUT_FILE
        subtitle_output_file = subtitle_output_file or self.SUBTITLE_OUTPUT_FILE

        print("Starting to generate audio and subtitles...")
        assert len(text) > 0
        assert len(text) < self.MAX_CHARS

        communicate = edge_tts.Communicate(text, self.VOICE)
        submaker = edge_tts.SubMaker()

        # Get the length of the text to estimate the number of chunks
        total_chunks = len(text.split())

        # Initialize the tqdm progress bar
        with tqdm(total=total_chunks, desc="Generating Audio", unit="chunk") as pbar:
            with open(audio_output_file, "wb") as file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
                    pbar.update(1)  # Update the progress bar

        with open(subtitle_output_file, "w", encoding="utf-8") as file:
            file.write(submaker.generate_subs(words_in_cue=1))

        print("Audio and subtitles generated successfully!")

    def run(self):
        self.load_text()

        # Process the title. this is done to see how long the title audio is
        text = ""
        with open("story_title.txt", "r") as f:
            text += f.read()
        asyncio.run(self.generate_audio_and_subtitles(text))

        # Calculate length of title audio by looking at the subtitle file
        with open("title_length.txt", "w") as f:
            with open(self.SUBTITLE_OUTPUT_FILE, "r") as f2:
                subtitle_text = f2.read()
                length = subtitle_text[subtitle_text.rfind(":") + 1: subtitle_text.rfind(":") + 7]
            f.write(str(length))

        # Add period between text and body of text, if necessary
        if "." not in text[-2:] and "?" not in text[-2:] and "!" not in text[-2:]:
            text += ". "

        # add in the rest of the text
        with open("story.txt", "r") as f:
            text += f.read()

        asyncio.run(self.generate_audio_and_subtitles(text))

        # Adjust the subtitle words by cleaning them
        with open("replacements.json", "r") as f:
            replacements = json.load(f)
        with open(self.SUBTITLE_OUTPUT_FILE, "r") as f:
            lines = f.read()
        for bad_word, replacement in replacements.items():
            lines = lines.replace(bad_word, replacement)
        with open(self.SUBTITLE_OUTPUT_FILE, "w") as f:
            f.write(lines)


if __name__ == "__main__":
    generator = AudioSubtitleGenerator("system")
    generator.run()