import time
#17-9-25 , 10:22

def GetTime():
    Time = time.strftime("%H:%M", time.gmtime())
    return Time

def GetDate():
    Date = time.strftime("%d-%m-%y", time.gmtime())
    return Date


print(GetDate())
print(GetTime())