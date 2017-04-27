import os
from sleepy import Sleepy
abs_path = os.path.dirname(os.path.realpath(__file__))  # doesn't have /
#play 4.5h of background noise and slowly come up at the end for 10 minutes and then beep like

slpy = Sleepy(abs_path)
slpy.go([
    {
        "time": 90 * 3,
        "volume": 70,
        "folder": "whitenoise"
    },
    {
        "time": 10,
        "volume": 50,
        "folder": "slowlygettingup"
    },
    {
        "time": 60,
        "volume": 100,
        "folder": "alarm"
    }
])


"""
times = [
    4 * 60 + 30, # deep sleep 4.5 hours
             10, # 10 minutes kind of get out of it
             60  # 60 minutes beep all the alarms
]
volumes = [
    70,
    50,
    100
]
slpy.play("whitenoise", times[0], volumes[0])
slpy.play("slowlygettingup", times[1], volumes[1])
slpy.play("alarm", times[2],volumes[2])
slpy.go()
"""