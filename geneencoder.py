exon = open("sample_exon.txt")
line = exon.readline()
lines = []

while line != "":

    splitLine = line.split()
    
    # removing last comma
    beginExon = splitLine[9][0:len(splitLine[9])-1]
    
    #adding in starting values in tuple
    newTup = tuple(beginExon.split(','))
    #print(newTup)
    # removing last comma
    endExon = splitLine[10][0:len(splitLine[10])-1]
    #print (endExon)
    endTup = tuple(endExon.split(','))
   # print (endTup)
    finalTup = (newTup[0:]+endTup[0:])
   # print(finalTup)
    lines.append(finalTup)
    line = exon.readline()
print (lines)
#reading in console inputs
word = ""
while word is not None:
    try:
        word = input('Enter your input:')
        if word is not '':
            word = word.split()
            #print(word[1])
    except EOFError:
        break
