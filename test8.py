myVar = 'hello python - global'
def myFunction():
    global myVar
    myVar = 'hello python - local'
    print('Inside myFunction(): ',myVar)
myFunction()
print('Outside myFunction(): ',myVar)