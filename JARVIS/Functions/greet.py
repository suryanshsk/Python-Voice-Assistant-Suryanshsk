import datetime
from Functions.talk import talk
def greet_user():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        talk("Good morning!")
    elif hour >= 12 and hour < 18:
        talk("Good afternoon!")
    else:
        talk("Good evening!")
