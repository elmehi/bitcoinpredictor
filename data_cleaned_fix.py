import sys
# import math
from datetime import datetime as dt, timedelta


f = open('data_new.csv', 'w')

def convert_from_minutes(d, m):
    m = int(m)
    d = dt.strptime(d, '%Y-%m-%d')
    h = int(m/60)
    m = int(m % 60)
    d = d.replace(hour=h, minute=m)
    return (d.strftime("%Y-%m-%d %H:%M:%S"), d)

sys.stdin.readline()

# last = None
f.write('Error,Date,Date_Time,Price,Delta,Beta,Volume' + '\n')
for line in sys.stdin:
    # print(line)

    l = line.split(',')
    l[2], d = convert_from_minutes(l[1], l[2])
    # l.pop(2)
    f.write(','.join(l))

    # if last is not None:
    #     if d - last < datetime.timedelta(minutes=0):
    #         print(line)

    # last = d