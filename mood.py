import datetime

def get_prompt():
    now = datetime.datetime.utcnow()
    hour = now.hour
    month = now.month
    weekday = now.weekday()

    time = "night" if hour >= 18 else "day"
    season = "winter" if month in [12,1,2] else "summer"
    style = {0:"lofi",2:"ambient",4:"jazz"}.get(weekday,"lofi")

    return f"{style}, {time}, {season}, instrumental, no vocals"
