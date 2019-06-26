import time
from datetime import datetime

TIME = 207572046

def localtime(time):
    time.strftime("%H:%M:%S %z", time.localtime(time))

def makeTimestap(time):
    return datetime.fromtimestamp(time)


timestamp = time.gmtime(TIME)

print(datetime.utcnow())
print(datetime.now())
