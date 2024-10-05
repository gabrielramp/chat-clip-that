# test.py
import json
from moviepy.editor import VideoFileClip
from constants import *
from effects import add_vine_boom_effect, add_spin_effect, add_flying_image, add_sound_effect, add_goku_effect
from util import deepfry_video, return_json_as_object, return_time_since_0, return_two_arrays
from openai import OpenAI
from json_result import json_result_array

def play_bruh(video, start_time):
    video = add_sound_effect(BRUH, video, start_time, .75)
    return video

def play_amongus(video, start_time):
    video = add_sound_effect(AMONG_US_PATH, video, start_time, 1)
    return video

def play_ooooo(video, start_time):
    video = add_sound_effect(OOOOO, video, start_time, 4)
    return video

def play_fart(video, start_time):
    video = add_sound_effect(FART, video, start_time, 1.75)
    return video

def play_airhorn(video, start_time):
    video = add_sound_effect(AIRHORN_AUDIO_PATH, video, start_time, 1.75)
    return video

def play_who_invited(video, start_time):
    video = add_sound_effect(WHO_INVITED, video, start_time, 6.5)
    return video

def play_nerd(video, start_time):
    video = add_sound_effect(NERD, video, start_time, 1.75)
    return video

def play_taco_bell(video, start_time):
    video = add_sound_effect(TACO_BELL, video, start_time, 1.75)
    return video

def play_oooooo(video, start_time):
    video = add_sound_effect(OOOOO, video, start_time, 1.75)
    return video

def play_supahotfire(video, start_time):
    video = add_sound_effect(SUPA_HOT_FIRE_PATH, video, start_time, 1.75)
    return video

def play_yay(video, start_time):
    video = add_sound_effect(YAY_PATH, video, start_time, 1.75)
    return video

def play_taco_bell(video, start_time):
    video = add_sound_effect(TACO_BELL, video, start_time, 1.75)
    return video

def play_metal_pipe(video, start_time):
    video = add_sound_effect(METAL_PIPE_PATH, video, start_time, 1.75)
    return video

def play_minecraft_oof(video, start_time):
    video = add_sound_effect(MINECRAFT_OOF_PATH, video, start_time, 1)
    return video

def play_he_needs_some_milk(video, start_time):
    video = add_sound_effect(HE_NEEDS_SOME_MILK_PATH, video, start_time, 1.5)
    return video

def play_man_screaming(video, start_time):
    video = add_sound_effect(MAN_SCREAMING_PATH, video, start_time, 1.75)
    return video

def start_editing():
    video = VideoFileClip("just-saved/final_clip.mp4").set_fps(24)

    # Load the MP4 video
    with open("just-saved/final_clip.json", "r") as file:
        json_string = file.read()
    json_object2 = json.loads(json_string)

    # Get words and timestamps
    words, times = return_two_arrays(json_object2)

    print(words)
    print(times)

    client = OpenAI(api_key=OPENAI_KEY)

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": str(words) + " " + str(times)},
        ],
        response_format=json_result_array,
    )

    results_dicts = [result.dict() for result in completion.choices[0].message.parsed.results]

    # Serialize the list of dictionaries to JSON
    string = json.dumps(results_dicts)
    print(string)

    json_object = return_json_as_object(string)

    for item in json_object:
        key = item["meme_token"]
        timestamp = float(item["timestamp"])
        
        if key == "<vine_boom>":
            video = add_vine_boom_effect(video, timestamp, 1, True)
        elif key == "<bruh>":
            video = play_bruh(video, timestamp)
        elif key == "<airhorn>":
            video = play_airhorn(video, timestamp)
        elif key == "<drip_goku>":
            video = add_goku_effect(video, timestamp, 2.5, True)
        elif key == "<fart>":
            video = play_fart(video, timestamp)
        elif key == "<who_invited>":
            video = play_who_invited(video, timestamp)
        elif key == "<nerd>":
            video = play_nerd(video, timestamp)
        elif key == "<taco_bell_bong>":
            video = play_taco_bell(video, timestamp)
        elif key == "<yay>":
            video = play_yay(video, timestamp)
        elif key == "<taco_bell>":
            video = play_taco_bell(video, timestamp)
        elif key == "<metal_pipe>":
            video = play_metal_pipe(video, timestamp)
        elif key == "<among_us_reveal>":
            video = play_amongus(video, timestamp)
        elif key == "<minecraft_oof>":
            video = play_minecraft_oof(video, timestamp)
        elif key == "<he_needs_some_milk>":
            video = play_he_needs_some_milk(video, timestamp)
        elif key == "<man_screaming>":
            video = play_man_screaming(video, timestamp)
        else:
            print("Invalid key " + key)

    # Export the final video with audio
    video.write_videofile(OUTPUT_VIDEO_PATH, codec="libx264", audio_codec="aac")
