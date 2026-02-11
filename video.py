import subprocess

def make_video():
    subprocess.run("ffmpeg -loop 1 -i bg.png -i music.mp3 -t 180 -c:v libx264 -c:a aac -pix_fmt yuv420p out.mp4",shell=True)
