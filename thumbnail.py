from PIL import Image, ImageDraw, ImageFont

def make_thumbnail(title):
    img = Image.open("bg.png")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0,0,1280,120), fill=(0,0,0,180))
    draw.text((40,40), title, fill="white")
    img.save("thumb.png")
