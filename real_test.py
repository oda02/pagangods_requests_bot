from collections import deque
from datetime import datetime

kok = deque()
for x in range(20):
    kok.append(x)
print(kok)
a = 560
i = 0
for acc in kok:
    if acc > a:
        kok.insert(i, a)
        break
    i+=1
else:
    kok.insert(i, a)
print(kok)

if 22 > datetime.now().hour > 14:
    print('kok')