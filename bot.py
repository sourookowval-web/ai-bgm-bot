from mood import get_mood
from musicgen import generate_music
from bg import generate_bg
from video import make_video
from thumbnail import make_thumbnail
from youtube import upload

mood = get_mood()
title = f"{mood} | AI BGM"

generate_music(mood)
generate_bg("anime cozy room, rain, night, window, soft lighting")
make_video()
make_thumbnail(title)
upload(title)
