import requests, os

def generate_music(prompt):
    headers = {"Cookie": os.environ["SUNO_COOKIE"]}
    r = requests.post("https://studio-api.suno.ai/api/generate",headers=headers,json={
        "prompt":prompt,
        "instrumental":True,
        "duration":180
    })
    url = r.json()["audio_url"]
    data = requests.get(url).content
    with open("music.mp3","wb") as f:
        f.write(data)
