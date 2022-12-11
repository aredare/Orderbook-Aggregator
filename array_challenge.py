import itertools

arr = [16, 22, 35, 8, 20, 1, 21, 11]

equalSetSum = sum(arr)/2
count = int(len(arr) / 2)

combinations = set(itertools.combinations(arr,count))
    
for firstSet in combinations:
    if sum(firstSet) == equalSetSum:
        firstSet = list(firstSet)
        secondSet = arr
        
        for element in firstSet:
            secondSet.remove(element)
        
        firstSet.sort()
        secondSet.sort()
        
        if firstSet[0] < secondSet[0]:
            print((''.join(str(x) for x in firstSet) + ''.join(str(x) for x in secondSet))[::-1])
        else:
            print((''.join(str(x) for x in secondSet) + ''.join(str(x) for x in firstSet))[::-1])

        break
print(-1)
