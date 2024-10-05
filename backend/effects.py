# effects.py
from random import randint
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip, ImageClip, vfx
from constants import *
from util import *

def add_sound_effect(sound_effect, video, start_time, duration=None):
    new_audio = AudioFileClip(sound_effect).set_start(start_time)
    
    # Trim the audio to the specified duration if provided
    if duration is not None:
        new_audio = new_audio.subclip(0, duration)
    
    original_audio = video.audio
    if original_audio is None:
        combined_audio = new_audio
    else:
        combined_audio = CompositeAudioClip([original_audio, new_audio])
    
    return video.set_audio(combined_audio)

def add_vine_boom_effect(video, start_time, duration, play_sound=False):
    if play_sound:
        video = add_sound_effect(VINE_BOOM_PATH, video, start_time, duration)

        num = randint(0, 3)

        for i in range(num):
            video = add_sound_effect(VINE_BOOM_PATH, video, start_time + 1 * .2, duration)


    video = add_static_image_of_maoi(video, MOAI_PATH, start_time, duration)

    return video

def add_goku_effect(video, start_time, duration, play_sound=False):
    if play_sound:
        video = add_sound_effect(ULTRA_INSTINCT_PATH, video, start_time, duration)

    video = add_static_image_of_goku(video, DRIP_GOKU_PATH, start_time, duration)

    return video

def add_spin_effect(video, start_time, duration, angle):
    subclip = video.subclip(start_time, start_time + duration)
    spin_effect = subclip.fx(vfx.rotate, lambda t: angle * t / duration)
    video_with_spin = CompositeVideoClip([video, spin_effect.set_start(start_time)])
    return video_with_spin

def add_flying_image(video, image_path, start_time, duration, start_pos, end_pos, spin=False):
    # Load the image
    image = ImageClip(image_path).set_duration(duration).set_start(start_time)

    image = image.fx(vfx.resize, lambda t: t / 1+TEENY_TINY_SCALAR)
    
    # Apply spin effect if spin is True
    if spin:
        image = image.fx(vfx.rotate, lambda t: 360 * t / duration)
    
    # Define the animation for the image to move from start_pos to end_pos and back
    W, H = video.size
    image = image.set_position(lambda t: (
        (start_pos[0] + (end_pos[0] - start_pos[0]) * (t / (duration / 2)), start_pos[1] + (end_pos[1] - start_pos[1]) * (t / (duration / 2))) if t < (duration / 2) else
        (end_pos[0] - (end_pos[0] - start_pos[0]) * ((t - (duration / 2)) / (duration / 2)), end_pos[1] - (end_pos[1] - start_pos[1]) * ((t - (duration / 2)) / (duration / 2)))
    ))
    
    # Overlay the animated image on the video
    video_with_image = CompositeVideoClip([video, image])
    return video_with_image