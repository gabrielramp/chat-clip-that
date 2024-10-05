import json
from moviepy.editor import *

from constants import *

def deepfry_video(video, start_time, duration):
    subclip = video.subclip(start_time, start_time + duration)
    deepfry_effect = subclip.fx(vfx.colorx, 3.5)
    video_with_deepfry = CompositeVideoClip([video, deepfry_effect.set_start(start_time)])
    return video_with_deepfry

def add_static_image(video, image_path, start_time, duration, position):
    # Load the image
    image = ImageClip(image_path).set_duration(duration).set_start(start_time)
    
    # Set the position of the image
    image = image.set_position(position)
    
    # Overlay the static image on the video
    video_with_image = CompositeVideoClip([video, image])
    return video_with_image

def add_static_image_of_goku(video, image_path, start_time, duration):
    # Load the image
    image = ImageClip(image_path).set_duration(duration).set_start(start_time)
    
    # Overlay the static image on the video
    video_with_image = CompositeVideoClip([video, image])
    return video_with_image

def add_static_image_of_maoi(video, image_path, start_time, duration):
    # Load the image
    image = ImageClip(image_path).set_duration(duration).set_start(start_time)
    image = image.fx(vfx.resize, .75)
    W, H = video.size
    image = image.set_position(((W - image.w) / 2 + 50, 'center'))
    
    # Overlay the static image on the video
    video_with_image = CompositeVideoClip([video, image])
    return video_with_image

# util.py
def return_time_since_0(time_string):
    return float(time_string)

def return_json_as_object(json_string):
    import json
    return json.loads(json_string)

def add_sound_effect(sound_effect, video, start_time, duration=None):
    new_audio = AudioFileClip(sound_effect).set_start(start_time)
    
    # Trim the audio to the specified duration if provided
    if duration is not None:
        new_audio = new_audio.subclip(0, duration)
    
    original_audio = video.audio
    combined_audio = CompositeAudioClip([original_audio, new_audio])
    return video.set_audio(combined_audio)

def return_two_arrays(json_object):
    words = []
    timestamps = []
    for item in json_object:
        words.append(item['word'])
        timestamps.append(item['timestamp'])
    return words, timestamps