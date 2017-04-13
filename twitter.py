import sys
from datetime import datetime as dt 
f = sys.stdin
o = sys.stdout

startend = f.readline().split(',')
start = dt.strptime(startend[0].strip(), '%Y-%m')
end = dt.strptime(startend[1].strip(), '%Y-%m')


f.readline()
months_d = {}
for line in f.readlines():   
    l = line.split(',')
    date = dt.strptime(l[0].strip(), '%Y-%m-%d')
    date = date.replace(day=1)
    if date > end or date < start: continue
    if date in months_d: month_d = months_d[date]
    else: month_d = {}
        
    if l[1] in month_d: month_d[l[1]] += int(l[2])
    else: month_d[l[1]] = int(l[2])
        
    months_d[date] = month_d #store in dict
    
for k in sorted(months_d, reverse=True):
    o.write(k.strftime('%Y-%m'))
    for k, v in sorted(months_d[k].items()):
        o.write(',' + str(k) + ', ' + str(v))
    o.write('\n')