import copy
import math
import random

import requests

from Second import box
from Second.box import *

CONST_GEN_SIZE = 200

f = open('14.txt', 'r')
l = f.readline()
wordList = l.split()
w_lim = int(wordList[0])
v_lim = int(wordList[1])
i=1
for line in f:
    pieces = line.split()
    print(pieces)
    read_data.append({'name': i, 'weight': int(pieces[0]), 'volume': float(pieces[1]), 'value': int(pieces[2])})
    i = i+1
f.closed

BOX_AMOUNT = i-1
ppl = []

def fit(b: box) -> bool:
    b.recalc()
    return (b.getVlm() <= v_lim and b.getWei() <= w_lim)

def extractBits(x:box, msb:int, lsb:int):
    return (x.getItems() >> lsb) & ~(~0 << (msb - lsb + 1))

def breed(a:box, b:box)->box:
    p1 = random.randint(1,28)
    p0 = random.randint(0,p1-1)
    p2 = random.randint(p1+1, 29)
    items = 0|extractBits(a,29,p2)|extractBits(b,p2-1,p1)|extractBits(a,p1-1,p0)|extractBits(b,p0-1,0)
    return box(items)
#generate 200 instances

while len(ppl) < 200:
    r = random.randint(0,1073741823)
    b = box(r)
    if fit(b):
        ppl.append(b)

print("starting the cycle")
lastValue = 0.5
for GEN in range(0,100):
    ppl.sort(key=lambda x: x.getVal(), reverse=True)

    if (max(ppl[0].getValPure(),lastValue)/min(ppl[0].getValPure(),lastValue)) < 1.01 :
        print(max(ppl[0].getValPure(),lastValue))
        print(min(ppl[0].getValPure(), lastValue))
        print("stopping")
        break

    lastValue = ppl[0].getValPure()
    print("BEST VALUE " + str(lastValue))
    cnt = len(ppl)
    #breed
    t20 = int(cnt*0.2)
    toCross = ppl[0:t20]
    for i in range(0,t20):
        if i == t20-1-i: #самому с собой нельзя
            break
        kid = breed(toCross[i],toCross[t20-1-i])
        kid.new = True
        ppl.append(kid)
        ppl.append(copy.deepcopy(kid))
        cnt+=2
    #breed
    #mutation
    t5 = int(len(ppl) * 0.07)
    toMutate = []
    for i in range(0,t5):
        unlucky:box = ppl.pop(random.randint(0,len(ppl)-1))
        b1 = random.randint(1, 28)
        b0 = random.randint(0, b1-1)
        b2 = random.randint(b1 + 1, 29)
        unlucky.inverseItem(b0)
        unlucky.inverseItem(b1)
        unlucky.inverseItem(b2)
        unlucky.recalc()
        toMutate.append(unlucky)
    ppl.extend(toMutate)
    #mutation
    #сокращаем популяцию до 200 и раздаем штрафы за старость
    for instance in ppl:
        if not fit(instance) and len(ppl) >200:
            ppl.remove(instance)
        elif instance.new == False:
            instance.health *= 0.8
        else:
            instance.new = False
ppl.sort(key=lambda x: x.getValPure(), reverse=True)
best = ppl[0]
print("Done in " + str(GEN) + " steps")
print(bin(best.getItems()))
print (best.getValPure())
print (best.getWei())
print (best.getVlm())
print(best.getItemList())



reg_a = 'https://cit-home1.herokuapp.com/api/ga_homework'
jsargs = {
    "user":14,
    "2": {
        "value" : best.getValPure(),
        "weight" : best.getWei(),
        "volume" : math.ceil(best.getVlm()),
        "items" : best.getItemList()
    }
}
head = {'content-type': 'application/json'}
print()

r = requests.post(reg_a, json=jsargs,headers=head)
print(r.json())
