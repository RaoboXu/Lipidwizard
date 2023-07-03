import platform
from datetime import datetime
import os

def Normalize(data: list[float]):
    value_max = float('-inf')
    result = []
    for v in data:
        value_max = max(value_max, v)
    for v in data:
        result.append(v/value_max)
        # result.append(float('{:.6f}'.format(v/value_max)))
    return result


def GetTimeStamp():
    return datetime.now().strftime("%y-%m-%d-%H%M")


def AddTimeStamp(path: str, stamp: str):
    p = path.rfind('.')
    return path[0:p]+'_'+stamp+path[p:]


def GetNameOfFile(path: str):
    s = os.path.splitext(path)[0]
    s = s.split('/')
    return s[-1]


def GetPureNameOfFile(path: str):
    s = os.path.splitext(path)[0]
    s = s.split('/')
    return s[-1]


def cutLengthOfFile(path: str, maxLength=32):
    maxLength = int(maxLength)
    if len(path) > maxLength:
        return '...'+path[len(path)-maxLength:]
    else:
        return path


def getMTimeOfFile(path: str):
    mt = 0.0
    if os.path.exists(path):
        if platform.system() == 'Windows':
            mt = os.path.getmtime(path)
        else:
            stat = os.stat(path)
            mt = stat.st_mtime
        return datetime.fromtimestamp(mt).strftime("%m/%d/%Y, %H:%M:%S")

if __name__ == '__main__':
    print(AddTimeStamp('./config.json'))
