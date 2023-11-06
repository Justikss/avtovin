def america():
    a = [num for num in range(1, 35)]
    r = []
    for index, number in enumerate(a[:-1]):
        if index == len(a)-2:
            if len(a) % 2 == 0: 
                r.append([number])
            r.append([a[index+1]])
            return r

        elif index == 0 or index % 2 == 0:
            r.append([a[index], a[index+1]])

    return r

print(america())