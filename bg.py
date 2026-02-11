import requests, base64

def generate_bg(prompt):
    r = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img",json={
        "prompt":prompt,
        "steps":20,
        "width":768,
        "height":432
    })
    img = base64.b64decode(r.json()["images"][0])
    with open("bg.png","wb") as f:
        f.write(img)
