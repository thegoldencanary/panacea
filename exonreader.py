exon = open("sample_exon.txt")
line = exon.readline()
lines = []
# tuple storing
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
		
		
"""
A template of the class for exon filtering

Just need to fill in the loading of the file and the exon checking

class ExonFilter:

	self.input = None
	self.exons = []
	
	def __init__( self, input, exon_filename ):
	
		f = open( exon_filename )
		# Load lines into exons
		
		# Set input
		self.input = input
		
	def __iter__( self ):
		return self
		
	def __next__( self ):
	
		# Get next variant
		try:
			variant = self.input.__next__()
		except StopIteration:
			raise StopIteration
			
		# Check BSP for if variant position is in exon
		# If not, call self.__next__()
		return variant
		
	
"""
	
	
	
	
	
	
	
	
	
	