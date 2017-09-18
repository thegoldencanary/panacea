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
		
		# BST - This is copied from pipeline - PriorTagger. You'll need to adjust the conditionals. 
		# i.e, where equality is checked check if in exon bounds, where < or > checked check either side
		# of exon boundary.
		
		
			# Get variance position and set indexes
			variant_pos = variant.position
			end = len( self.prior_list ) - 1
			begin = 0
			while( True ):
			
				# Set the middle index
				index = begin + int( ( end - begin ) / 2 )
				node = self.prior_list[ index ]
				
				# If found scan for correct variant
				if variant_pos == node[0] or variant_pos == self.prior_list[end][0]:
					if variant_pos == self.prior_list[end][0]: 
						index = end
						node = self.prior_list[end]
					saved = index
					while variant_pos == node[ 0 ]:
						if variant.old_base == node[ 2 ] and variant.new_base == node[ 1 ]:
							variant.probability = node[ 3 ]
							return variant
						index -= 1
						if index < ( 0 ): break
						node = self.prior_list[ index ]
					index = saved
					node = self.prior_list[ index ]
					while variant_pos == node[ 0 ]:
						if variant.old_base == node[ 2 ] and variant.new_base == node[ 1 ]:
							variant.probability = node[ 3 ]
							return variant	
						index += 1
						if index > ( len( self.prior_list ) - 1 ): break
						node = self.prior_list[ index ]
					break
					
				# If we checked the whole array and found nothing, end
				if int( ( end - begin ) / 2 ) == 0: break
				
				# if the indexes are the same now, end
				if end == begin:
					break
				
				# If middle node is < or > than indexes, move indexes accordingly.
				if node[ 0 ] < variant_pos:
					begin = index
					continue
				if node[ 0 ] > variant_pos:
					end = index
					continue
		
		
		
		
		# If not, get new variant
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
            
                
	
	
	
