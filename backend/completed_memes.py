# completed_memes.py
from effects import add_sound_effect, add_vine_boom_effect, add_flying_image
from util import *
from constants import *

def add_ultra_instinct_goku_effect(video, start_time, duration, play_sound=False):
    if play_sound:
        video = add_sound_effect(ULTRA_INSTINCT_PATH, video, start_time, duration)
    
    video = add_static_image_of_goku(video, DRIP_GOKU_PATH, start_time, duration)

    return video

def add_hairhorn_effect(video, start_time, duration, end_pos, spin=False, play_sound=False):
    if play_sound:
        video = add_sound_effect(AIRHORN_AUDIO_PATH, video, start_time, duration)
    
    # Define the start positions for the four corners
    start_positions = [
        (0, 0),  # Top-left corner
        (video.size[0], 0),  # Top-right corner
        (0, video.size[1]),  # Bottom-left corner
        (video.size[0], video.size[1])  # Bottom-right corner
    ]
    
    # Add flying image from each corner to the center
    for start_pos in start_positions:
        video = add_flying_image(video, AIRHORN_IMAGE_PATH, start_time, duration, start_pos, end_pos, spin)

    return video

def better_call_saul_effect(video, start_time, duration, end_pos, spin=False, play_sound=False):
    if play_sound:
        video = add_sound_effect(BETTER_CALL_SAUL_PATH, video, start_time, duration)
    
    # Create a yellow tint image
    W, H = video.size
    yellow_tint = ImageClip(YELLOW_TINT, ismask=False).set_duration(duration).set_start(start_time).resize((W, H)).set_opacity(0.5)
    
    # Overlay the yellow tint on the video
    video_with_tint = CompositeVideoClip([video, yellow_tint])

    return video_with_tint