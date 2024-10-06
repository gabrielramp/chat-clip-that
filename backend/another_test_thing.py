from util import add_sound_effect
from constants import OOOOO_GIF, OUTPUT_VIDEO_PATH, NERD_GIF, LOGO
from moviepy.editor import *

def play_supa_hot_gif(video, supa_hot_path, start_time):
    # Load the background video
    # Load the nerd gif video
    supa_hot_gif = VideoFileClip(supa_hot_path).set_start(start_time)

    supa_hot_gif = supa_hot_gif.subclip(0, 1.25)
    # Create a mask for the green screen
    supa_hot_gif = supa_hot_gif.fx(vfx.mask_color, color=[0, 255, 0], thr=100, s=5)

    # Overlay the nerd gif onto the background video
    composite_video = CompositeVideoClip([video, supa_hot_gif.set_position(("center", "center"))])

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

# Load the main video
video = VideoFileClip("../clip.avi").set_fps(24)

video = play_supa_hot_gif(video, OOOOO_GIF, 1)

# Save the final video
video.write_videofile(OUTPUT_VIDEO_PATH, codec="libx264", audio_codec="aac")
