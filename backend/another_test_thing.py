from util import add_sound_effect
from constants import CAR_CRASH, OUTPUT_VIDEO_PATH, NERD_GIF, LOGO
from moviepy.editor import *

def play_car_crash(video, car_crash_path, start_time):
    # Load the car crash gif video
    car_gif = VideoFileClip(car_crash_path).set_start(start_time)

    car_gif = car_gif.subclip(0, 3)

    # Create a mask for the green screen
    car_gif = car_gif.fx(vfx.mask_color, color=[0, 255, 0], thr=207, s=50)

    # Overlay the car gif onto the background video
    composite_video = CompositeVideoClip([video, car_gif.set_position(("center", "center"))])

    return composite_video

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

# Load the main video
video = VideoFileClip("../clip.avi").set_fps(24)

# Create the intro clip
intro = create_intro()

# Concatenate the intro clip with the main video
final_video = concatenate_videoclips([intro, video])

# Save the final video
final_video.write_videofile(OUTPUT_VIDEO_PATH, codec="libx264", audio_codec="aac")
