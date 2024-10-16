import re
from moviepy.editor import VideoFileClip, TextClip, ImageClip, CompositeVideoClip, AudioFileClip, ColorClip, concatenate_audioclips, concatenate_videoclips
import random
from PIL import Image, ImageDraw
import numpy as np
import json

# Function to parse VTT file
def parse_vtt(vtt_file, offset=0):
    subtitles = []
    with open(vtt_file, 'r') as file:
        for line in file:
            match = re.match(r'(\d{2}):(\d{2}):(\d{2})\.(\d{3}) --> (\d{2}):(\d{2}):(\d{2})\.(\d{3})', line)
            if match:
                start_time = int(match.group(1)) * 3600 + int(match.group(2)) * 60 + int(match.group(3)) + int(match.group(4)) / 1000
                end_time = int(match.group(5)) * 3600 + int(match.group(6)) * 60 + int(match.group(7)) + int(match.group(8)) / 1000
                start_time += offset
                end_time += offset
                word = next(file).strip()
                subtitles.append((word, start_time, end_time))
    return subtitles

# Function to create a rounded rectangle
def create_rounded_rectangle(size, radius, color):
    image = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius, fill=color)
    return image

random_trim = random.randint(1, 10) * 60  # Trim amount in seconds (1 to 10 minutes)

# Load your video
video = VideoFileClip("bg_vid.mp4")

# Trim the beginning of the video
if video.duration > random_trim:
    video = video.subclip(random_trim, video.duration)
else:
    raise ValueError("The video is not long enough to be trimmed by the specified amount.")

# Crop the video to 9:16 ratio
height = video.h
new_width = int(height * 9 / 16)
x_center = video.w // 2
x1 = x_center - new_width // 2
x2 = x_center + new_width // 2

video = video.crop(x1=x1, y1=0, x2=x2, y2=height)

# Load the audio files
with open("title_length.txt", "r") as f:
    intro_audio_duration = float(f.read().strip())
main_audio = AudioFileClip("output_audio3.mp3")

# Ensure the video is longer than the main audio
assert video.duration > main_audio.duration, "The video is not longer than the main audio duration."

# Clip the video to the same length as the main audio
video = video.subclip(0, main_audio.duration)

# Parse subtitles without any offset
subtitles = parse_vtt("output_audio3.vtt", offset=0)

# Create a list of text clips for each subtitle word
text_clips = []
for word, start_time, end_time in subtitles:
    text_clip = (TextClip(word, fontsize=65, color='white', font='Impact', stroke_color='black', stroke_width=2)
                    .set_position('center')
                    .set_start(start_time)
                    .set_end(end_time))
    text_clips.append(text_clip)

# Create the intro text box
with open("title.txt", 'r') as file:
    intro_text = file.read().strip()

# Split intro_text into 32-character chunks, but keep entire words together
with open("replacements.json", "r") as f:
    replacements = json.load(f)
temp = [""]
intro_text_words = intro_text.split(" ")
for word in intro_text_words:
    if word in replacements:
        word = replacements[word]
    if len(temp[-1]) + 1 + len(word) <= 32:
        temp[-1] += " " + word
    else:
        temp.append(word)
intro_text = "\n".join(temp)
intro_text_clip = (TextClip(intro_text, fontsize=45, color='black', font='Impact')
                   .set_position('center')
                   .set_duration(intro_audio_duration))

# Create a rounded rectangle background for the intro text
text_width, text_height = intro_text_clip.size
rounded_rectangle_image = create_rounded_rectangle((text_width + 20, text_height + 20), 20, (255, 255, 255))
rounded_rectangle_np = np.array(rounded_rectangle_image)
rounded_rectangle_clip = ImageClip(rounded_rectangle_np).set_duration(intro_audio_duration)
intro_clip = CompositeVideoClip([rounded_rectangle_clip.set_position('center'), intro_text_clip.set_position('center')])

username_text_clip = (TextClip("@le_spongebob", fontsize=55, color='black', font='Impact')
                .set_position(('center', int(video.h * 0.6)))
                .set_duration(video.duration))

# Create a rounded rectangle background for the intro text
username_width, username_height = username_text_clip.size
rounded_rectangle_username = create_rounded_rectangle((username_width + 20, username_height + 20), 20, (255, 255, 255))
rounded_rectangle_username = np.array(rounded_rectangle_username)
rounded_rectangle_username = ImageClip(rounded_rectangle_username).set_duration(video.duration)
username_clip = CompositeVideoClip([rounded_rectangle_username.set_position('center'), username_text_clip.set_position('center')])

# combine everything together
# random offset cuz username and username box isn't vertically aligned for some reason
combined_video = CompositeVideoClip([video] + text_clips + [intro_clip.set_position('center')] + [rounded_rectangle_username.set_position(('center', int(video.h * 0.6) - 7)), username_text_clip.set_position(('center', int(video.h * 0.6)))])

# Set the audio of the video to be only the main audio
final_video = combined_video.set_audio(main_audio)

# Write the result to a file
final_video.write_videofile("video.mp4", codec='libx264', fps=30)

# Save the first frame of the final video to "thumbnail.png"
first_frame = final_video.get_frame(0)
thumbnail = Image.fromarray(first_frame)
thumbnail.save("thumbnail.png")