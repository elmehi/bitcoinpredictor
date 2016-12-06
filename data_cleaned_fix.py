import sys
import math
from datetime import datetime as dt

f = open('data_new.csv', 'w')

def convert_from_minutes(d, m):
    m = int(m)
    d = dt.strptime(d, '%Y-%m-%d')
    h = math.floor(m/60)
    m = int(m % 60)
    d = d.replace(hour=h, minute=m)
    return d.strftime("%Y-%m-%d %H:%M:%S")

sys.stdin.readline()

for line in sys.stdin:
    # print(line)

    l = line.split(',')
    l[1] = convert_from_minutes(l[1], l[2])
    l.pop(2)
    f.write(','.join(l))