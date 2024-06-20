import pythoness
import time
from datetime import datetime

@pythoness.spec("""Given a UTC time value timeval, return the full name of the day of the week 
                corresponding to that timeval""")

def UTCDay(timeval : float) -> str:
    ""

print("Running tests: utc-time")
assert(UTCDay(time.time()) == datetime.now().strftime('%A'))
print("Tests complete.")