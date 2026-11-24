import datetime as dt, calendar
start=dt.date(2026,10,31); gap0=-462.0
def surplus(path, d):
    y,m=d.year,d.month
    if path=='y2025':
        return 1.7 if (y==2026) else 2.0
    if path=='iea':
        return 1.7 if y==2026 else 3.8
    if path=='eia':
        if y==2026: return 1.46
        q=(m-1)//3
        return [3.18,3.91,4.07,5.02][q] if y==2027 else 5.02
paths=[('y2025',0.5),('y2025',1.1),('y2025',0.0),('iea',0.5),('eia',0.5),('iea_h',0.5)]
months=[]
y,m=2026,11
while (y,m)<=(2028,6):
    months.append((y,m)); m+=1
    if m==13: y,m=y+1,1
for p,c in paths:
    g=gap0; row=[]; cross=None
    for (y,m) in months:
        nd=calendar.monthrange(y,m)[1]
        for day in range(1,nd+1):
            d=dt.date(y,m,day)
            base=p.replace('_h','')
            s=surplus(base,d)
            if p.endswith('_h'): s*=1.3/1.88
            g+= s-c
            if cross is None and g>=0: cross=d
        row.append(round(g))
    print(p,c,cross,row)
print([f"{y%100}.{m}" for y,m in months])
