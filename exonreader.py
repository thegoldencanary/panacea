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
	
class ExonFilter:

	input = None #imports of variences
	exons = []
	
	def __init__( self, input, exon_filename ):

            exon = open(exon_filename)
            line = exon.readline()
            while line != "":
                  splitLine = line.split()
                  #getting first lot of tuples without last comma
                  beginExon = splitLine[9][0:len(splitLine[9])-1]
                  
                  beginValues = beginExon.split(',') #should be a list
                  
                  #same for end exon
                  endExon = splitLine[10][0:len(splitLine[10])-1]

                  endValues = endExon.split(',')

                  #list of exon ranges 
                  #index 0 is the begin and index 1 is the end of range and so forth
                  #rangelist final size should be even
                  
                  for x in range(len(beginValues)):
                      self.exons+beginValues[x]
                      slef.exons+endValues[x]
                  
                  #end of iteration for while loop
            def __iter__( self ):
                return self
		
	    #def __next__( self ): # nathan to implement binary tree that checks if an
            #input varience is within the range allowed already one for ranker you repurpose
            # if you want
            
                
	
	
	
