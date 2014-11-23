import subprocess
from time import sleep


def setFanSpeed(speed, fan=0):
    subprocess.Popen('aticonfig --pplib-cmd "set fanspeed ' + str(fan) + ' ' + \
                     str(speed) + '"', shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)


def getFanSpeed(fan=0):
    return int(subprocess.Popen('aticonfig --pplib-cmd "get fanspeed ' +\
                                str(fan) + '"', shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)\
               .stdout.readlines()[2][-5:-2])


def getTemp():
    return float(subprocess.Popen('aticonfig --odgt', shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)\
                 .stdout.readlines()[2][-9:-2])


def adjustFan():
    temp = getTemp()
    if temp < 40:
        setFanSpeed(20)
    elif temp < 90:
        setFanSpeed(temp - 20)
    else:
        setFanSpeed(100)


def main():
    while True:
        adjustFan()
        print("Fan speed:", getFanSpeed())
        sleep(5)


if __name__ == "__main__":
    main()
