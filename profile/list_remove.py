import random
random.seed(11031987)

size_of_list = 8
count_of_lists = 1100000
lists = []
toberemoved = []
print('prepare data')
for _ in range(count_of_lists):
    l = []
    for _ in range(size_of_list):
        l.append((
            random.randint(0, 4),
            random.randint(0, 11)
        ))
    lists.append(l)
    toberemoved.append(l[random.randint(0, size_of_list-1)])

import copy
lists2 = copy.deepcopy(lists)

import time
print('test 1: remove')
now = time.clock()
for i in range(count_of_lists):
    l = lists[i]
    k = toberemoved[i]
    l.remove(k)
print('test 1:', time.clock() - now)


print('test 2: list')
now = time.clock()
for i in range(count_of_lists):
    l = lists[i]
    k = toberemoved[i]
    l = [c for c in l if c != k]
print('test 2:', time.clock() - now)