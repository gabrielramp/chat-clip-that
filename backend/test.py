# test.py
import json
from moviepy.editor import VideoFileClip, CompositeVideoClip, vfx, TextClip, ColorClip, ImageClip, concatenate_videoclips
from constants import *
from effects import add_vine_boom_effect, add_spin_effect, add_flying_image, add_sound_effect, add_goku_effect
from util import deepfry_video, return_json_as_object, return_time_since_0, return_two_arrays
from openai import OpenAI
from json_result import json_result_array
from dotenv import load_dotenv

load_dotenv()

def play_bruh(video, start_time):
    return add_sound_effect(BRUH, video, start_time, .75)

def play_amongus(video, start_time):
    return add_sound_effect(AMONG_US_PATH, video, start_time, 1)

def play_ooooo(video, start_time):
    return add_sound_effect(OOOOO, video, start_time, 4)

def play_fart(video, start_time):
    return add_sound_effect(FART, video, start_time, 1.75)

def play_airhorn(video, start_time):
    return add_sound_effect(AIRHORN_AUDIO_PATH, video, start_time, 1.75)

def play_who_invited(video, start_time):
    return add_sound_effect(WHO_INVITED, video, start_time, 6.5)

def play_nerd(video, start_time):
    return add_sound_effect(NERD, video, start_time, 1.75)

def play_taco_bell(video, start_time):
    return add_sound_effect(TACO_BELL, video, start_time, 1.75)

def play_oooooo(video, start_time):
    return add_sound_effect(OOOOO, video, start_time, 1.75)

def play_supahotfire(video, start_time):
    return add_sound_effect(SUPA_HOT_FIRE_PATH, video, start_time, 1.75)

def play_yay(video, start_time):
    return add_sound_effect(YAY_PATH, video, start_time, 1.75)

def play_taco_bell(video, start_time):
    return add_sound_effect(TACO_BELL, video, start_time, 1.75)

def play_metal_pipe(video, start_time):
    return add_sound_effect(METAL_PIPE_PATH, video, start_time, 1.75)

def play_minecraft_oof(video, start_time):
    return add_sound_effect(MINECRAFT_OOF_PATH, video, start_time, 1)

def play_he_needs_some_milk(video, start_time):
    return add_sound_effect(HE_NEEDS_SOME_MILK_PATH, video, start_time, 1.5)

def play_man_screaming(video, start_time):
    return add_sound_effect(MAN_SCREAMING_PATH, video, start_time, 1.75)

def play_rizz(video, start_time):
    return add_sound_effect(RIZZ, video, start_time, 1)

def play_brain(video, start_time):
    return add_sound_effect(BRAIN_ANHURISM, video, start_time, 1.75)

def plat_fortnite_death(video, start_time):
    return add_sound_effect(FORTNITE_DEATH_PATH, video, start_time, 2)

def play_wasted(video, start_time, duration=3.5):
    print("Adding red text 'WASTED'.")
    # Add red text
    text = TextClip("WASTED", fontsize=70, color='red', font='Amiri-Bold')
    text = text.set_duration(duration).set_start(start_time).set_position('center')

    print("Combining clips.")
    # Combine the original video and the text
    final_video = CompositeVideoClip([video, text])
    final_video = add_sound_effect(WASTED_SOUND, final_video, start_time, 3.5)

    return final_video
    

def play_nerd_gif(video, nerd_gif_path, start_time):
    # Load the background video
    # Load the nerd gif video
    nerd_gif = VideoFileClip(nerd_gif_path).set_start(start_time)

    nerd_gif = nerd_gif.subclip(0, 6)
    # Create a mask for the green screen
    nerd_gif = nerd_gif.fx(vfx.mask_color, color=[0, 255, 0], thr=100, s=5)

    # Overlay the nerd gif onto the background video
    composite_video = CompositeVideoClip([video, nerd_gif.set_position(("center", "center"))])

    return composite_video

def play_quick_scope_gif(video, quick_scope_path, start_time):
    # Load the quick scope gif video
    quick_scope_gif = VideoFileClip(quick_scope_path).set_start(start_time)

    # Create a subclip of the quick scope gif video
    quick_scope_gif = quick_scope_gif.subclip(0, 1.5)

    # Create a mask for the green screen
    quick_scope_gif = quick_scope_gif.fx(vfx.mask_color, color=[0, 255, 0], thr=100, s=5)

    # Overlay the quick scope gif onto the background video
    composite_video = CompositeVideoClip([video, quick_scope_gif.set_position(("center", "center"))])

    return composite_video

def create_intro():
    # Create a background color clip
    intro_background = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=5)

    # Load the logo image
    logo = ImageClip(LOGO).set_duration(5).set_position(('center', 'top')).resize(height=200).margin(top=20, opacity=0)

    # Composite the text and logo on the background
    intro_clip = CompositeVideoClip([intro_background, logo])

    return intro_clip

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

    client = OpenAI(api_key=OPENAI_API_KEY)

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

            image = ImageClip(AIRHORN_IMAGE_PATH).set_duration(1).set_start(timestamp)

            # Apply resize effect
            image = image.fx(vfx.resize, lambda t: t / 1 + TEENY_TINY_SCALAR)

            # Apply spin effect
            image = image.fx(vfx.rotate, lambda t: 360 * t / 1)

            # Define the animation for the image to move from start_pos to center and back
            start_pos = (100, 100)  # Example start position (x, y)
            W, H = video.size

            # Move from start_pos to center
            image_to_center = image.set_position(lambda t: (
                (start_pos[0] + (W / 2 - start_pos[0]) * (t / 0.5), start_pos[1] + (H / 2 - start_pos[1]) * (t / 0.5)) if t < 0.5 else
                (W / 2, H / 2)
            ))

            # Move from center to start_pos
            image_from_center = image.set_position(lambda t: (
                (W / 2 + (start_pos[0] - W / 2) * ((t - 0.5) / 0.5), H / 2 + (start_pos[1] - H / 2) * ((t - 0.5) / 0.5)) if t >= 0.5 else
                (W / 2, H / 2)
            ))

            # Combine the two animations
            video = CompositeVideoClip([video, image_to_center, image_from_center])            

        elif key == "<drip_goku>":
            video = add_goku_effect(video, timestamp, 2.5, True)
        elif key == "<brain_anhurism>":
            video = play_brain(video, timestamp)
        elif key == "<who_invited>":
            video = play_who_invited(video, timestamp)
        elif key == "<nerd>":
            video = play_nerd_gif(video, NERD_GIF, timestamp)
        elif key == "<taco_bell_bong>":
            video = play_taco_bell(video, timestamp)
        elif key == "<yay>":
            video = play_yay(video, timestamp)
        elif key == "<taco_bell>":
            video = play_taco_bell(video, timestamp)
            
            image = ImageClip(TACO_BELL_IMAGE).set_duration(2).set_start(timestamp)
            image = image.fx(vfx.resize, .75)
            W, H = video.size
            image = image.set_position(((W - image.w) / 2 + 50, 'center'))
            
            # Overlay the static image on the video
            video = CompositeVideoClip([video, image])

        elif key == "<metal_pipe>":
            video = play_metal_pipe(video, timestamp)
        elif key == "<among_us>":
            video = play_amongus(video, timestamp)

            image = ImageClip(WOKE_AMONGUS).set_duration(1).set_start(timestamp)
            image = image.fx(vfx.resize, .15)
            W, H = video.size
            image = image.set_position(((W - image.w) / 2 + 50, 'center'))
            
            # Overlay the static image on the video
            video = CompositeVideoClip([video, image])
        elif key == "<minecraft_oof>":
            video = play_minecraft_oof(video, timestamp)
        elif key == "<he_needs_some_milk>":
            video = play_he_needs_some_milk(video, timestamp)
        elif key == "<man_screaming>":
            video = play_man_screaming(video, timestamp)
        elif key == "<rizz>":
            video = play_rizz(video, timestamp)
            image = ImageClip(HEART_FRAME)

            # Set the duration and start time for the image overlay
            overlay_duration = 3  # Duration in seconds
            image = image.set_duration(overlay_duration).set_start(timestamp)

            # Set the position of the image overlay (e.g., top-left corner)
            image = image.set_position(("center", "center"))

            video = CompositeVideoClip([video, image])
        elif key == "<wasted>":
            video = play_wasted(video, timestamp)
        elif key == "<fornite_death>":
            video = plat_fortnite_death(video, timestamp)
        else:
            print("Invalid key " + key)

    # Export the final video with audio
    video.write_videofile(OUTPUT_VIDEO_PATH, codec="libx264", audio_codec="aac")