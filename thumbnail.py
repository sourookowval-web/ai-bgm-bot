from PIL import Image, ImageDraw, ImageFont

def make_thumb(title):
    img = Image.open("bg.png").resize((1280,720))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((50,50),title,fill="white",font=font)
    img.save("thumb.png")
