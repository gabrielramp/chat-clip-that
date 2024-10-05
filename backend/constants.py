import os

# mp3 paths for sound effects
AIRHORN_AUDIO_PATH = "sound_effects/airhorn.mp3"
AMONG_US_REVEAL_PATH = "sound_effects/among-us-reveal.mp3"
AMONG_US_PATH = "sound_effects/among-us.mp3"
BETTER_CALL_SAUL_PATH = "sound_effects/better-call-saul.mp3"
BRUH = "sound_effects/bruh.mp3"
CRAZY_FROG_PATH = "sound_effects/crazy-frog.mp3"
FART = "sound_effects/fart.mp3"
FORTNITE_DEATH_PATH = "sound_effects/fortnite-death.mp3"
HE_NEEDS_SOME_MILK_PATH = "sound_effects/he-needs-some-milk.mp3"
MAN_SCREAMING_PATH = "sound_effects/man-screaming.mp3"
METAL_PIPE_PATH = "sound_effects/metal-pipe.mp3"
MINECRAFT_OOF_PATH = "sound_effects/minecraft-oof.mp3"
NANI = "sound_effects/nani.mp3"
NERD = "sound_effects/nerd.mp3"
OOOOO = "sound_effects/ooooo.mp3"
SKIBIDI_PATH = "sound_effects/skibidi-toilet.mp3"
SUPA_HOT_FIRE_PATH = "sound_effects/supa-hot-fire.mp3"
TACO_BELL = "sound_effects/taco-bell.mp3"
ULTRA_INSTINCT_PATH = "sound_effects/ultra-instinct.mp3"
VINE_BOOM_PATH = "sound_effects/vine-boom.mp3"
WALTUH_PATH = "sound_effects/waltuh.mp3"
WHO_INVITED = "sound_effects/who-invited.mp3"
YAY_PATH = "sound_effects/yay.mp3"
RIZZ = "sound_effects/rizz.mp3"
HITMARKER = "sound_effects/gunshot.mp3"

# PNG assets
MOAI_PATH = "png_assets/moai.png"
AIRHORN_IMAGE_PATH = "png_assets/airhorn.png"
DRIP_GOKU_PATH = "png_assets/drip-goku.png"

# GIF assets
NERD_GIF = "gif_assets/nerd-gif.mp4"
CAR_CRASH = "gif_assets/car-crash-gif.mp4"

OUTPUT_VIDEO_PATH = "output_video.mp4"

TEENY_TINY_SCALAR = 0.01

YELLOW_TINT = "tint/yellow.jpg"

SYSTEM_PROMPT = 'You will receive words and timestamps corresponding to each word. You should only return a json like this {"<vine_boom>": "3.123",......}. These meme tokens can be <vine_boom>, <rizz>, <bruh>, <fart>, <taco_bell>, <airhorn>, <nerd>, <who_invited>, <among_us>, <among_us_reveal>, <better_call_saul>, <crazy_frog>, <fortnite_death>, <he_needs_some_milk>, <man_screaming>, <metal_pipe>, <minecraft_oof>, <nani>, <skibidi>, <ultra_instinct>, <waltuh>, <yay>. Only use these meme tokens. You will return up to seven to ten individual meme tokens at a minimum with a timestamp depending upon where the edit of the video should occur based on comedic timing, content of the user transcript where it makes sense, and the unexpected (moreso on spaces of timestamps). You must return seven to ten individual meme tokens. <rizz> should be used whenever there is flirtation or flirtatous intent'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

LOGO = "png_assets/cct-logo-white.png"