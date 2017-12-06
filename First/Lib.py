from pyeasyga import pyeasyga
import requests
import math

f = open('34.txt', 'r')
l = f.readline()
wordList = l.split()
w_lim = int(wordList[0])
v_lim = int(wordList[1])
read_data = []
i=0
for line in f:
    pieces = line.split()
    print(pieces)
    read_data.append({'name': i, 'weight': int(pieces[0]), 'volume': float(pieces[1]), 'value': int(pieces[2])})
    i = i+1
f.closed

# setup data

ga = pyeasyga.GeneticAlgorithm(read_data)        # initialise the GA with data

# define a fitness function
def fitness(individual, data):
    values, weights, volumes = 0, 0, 0
    for selected, box in zip(individual, data):
        if selected:
            values += box.get('value')
            weights += box.get('weight')
            volumes += box.get('volume')
    if weights > w_lim or volumes > v_lim:
        values = 0
    return values

ga.fitness_function = fitness               # set the GA's fitness function
ga.run()                                    # run the GA
print (ga.best_individual()  )                # print the GA's best solution

res = ga.best_individual()

#Смотрим, какие предметы вошли в лучший вариант
items = []
i=1
for item in res[1]:
    if item == 1:
        items.append(i)
    i= i+1

#Считаем по предметам результирующие показатели
wr,vr = 0,0
for box in items:
    wr += read_data[box-1].get('weight')
    vr += read_data[box-1].get('volume')
vr = math.ceil(vr)

reg_a = 'https://cit-home1.herokuapp.com/api/ga_homework'
jsargs = {
    "user":34,
    "1": {
        "value" : res[0],
        "weight" : wr,
        "volume" : vr,
        "items" : items
    }
    #"2": {"movie " + str(best+1) : firstTask["movie "+str(best+1)]}
}
head = {'content-type': 'application/json'}
print()

#r = requests.post(reg_a, json=jsargs,headers=head)
print(r.json())