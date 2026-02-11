import random, datetime

def get_mood():
    moods = [
        "lofi chill rainy night",
        "deep focus ambient",
        "cozy jazz cafe rain",
        "cyberpunk night rain",
        "soft piano winter night"
    ]
    today = datetime.datetime.utcnow().weekday()
    return moods[today % len(moods)]
