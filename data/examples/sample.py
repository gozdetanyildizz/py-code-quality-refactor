def badFunctionName(x,y,z):
    total=0
    for i in range(0,10):
        if i%2==0:
            total+=i
        else:
            total-=i
    return total+x+y+z
