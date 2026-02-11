from mood import get_prompt
from suno import generate_music
from bg import generate_bg
from video import make_video
from thumbnail import make_thumb
from youtube import upload

prompt = get_prompt()
title = prompt.title()

generate_music(prompt)
generate_bg("cozy room, rain, anime style")
make_video()
make_thumb(title)
upload(title)
