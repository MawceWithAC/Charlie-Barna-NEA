import time
"""
Returns The Data On Time
"""

def GetTime():
    Time = time.strftime("%H:%M", time.gmtime())
    return Time

def GetDate():
    Date =time.strftime("%d-%m-%y", time.gmtime())
    return Date


print(f"DATE: {GetDate()}") #Gets The Date On Startup
print(f"TIME: {GetTime()}") #Gets The Time On Startup