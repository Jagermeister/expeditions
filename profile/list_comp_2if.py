#    @staticmethod
#    def pull_options(discard, discardCardColor=None):
#        # each discard that has a card, that isnt discardCard
#        if discardCardColor:
#            return [i for i, x in enumerate(discard) if x and i != discardCardColor]
#        else:
#            return [i for i, x in enumerate(discard) if x]

# Is there a savings to fork the code?
#   prepare data
#   test 1: if branch
#   test 1: 1.8437576779177642, 1.852253070389595, 1.884655671629258
#   test 2: no branch
#   test 2: 1.9429708371301768, 1.8633108269914382, 1.8828132823701014
# The issue is all around the amount of None in the list

import random
random.seed(11031987)

size_of_list = 5
count_of_lists = 1100000
lists = []
lastDiscard = []
print('prepare data')
for _ in range(count_of_lists):
    l = []
    for _ in range(size_of_list):
        l.append((
            random.randint(0, 4),
            random.randint(0, 11)
        ))
    lists.append(l)
    lastDiscard.append(random.randint(0, 6))

import time
print('test 1: if branch')
now = time.clock()
for i in range(count_of_lists):
    l = lists[i]
    k = lastDiscard[i]
    if k is not None:
        l = [i for i, x in enumerate(l) if x and i != k]
    else:
        l = [i for i, x in enumerate(l) if x]


print('test 1:', time.clock() - now)


print('test 2: no branch')
now = time.clock()
for i in range(count_of_lists):
    l = lists[i]
    k = lastDiscard[i]
    l = [i for i, x in enumerate(l) if x and i != k]
print('test 2:', time.clock() - now)