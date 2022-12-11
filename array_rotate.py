arr = [4,3,4,3,1,2]

result = arr[arr[0]:] + arr[:arr[0]]
print((''.join(str(x) for x in result))[::-1])
