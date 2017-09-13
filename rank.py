


"""
	Tags Variants with prior probability for ranking.
"""
class PriorTagger:

	input = None
	prior_file = None
	
	prior_list = []
	
	def __init__( self, input, prior_file_name ):
	
		self.input = input
		self.prior_file = open( prior_file_name )
		
		# Read prior probabilities
		for line in self.prior_file:
		
			if line[ 0 ] == "#": continue
			
			line = line.split()
			pos = int( line[ 1 ] )
			alt = line[ 3 ]
			reg = line[ 4 ]
			
			numbers = line[ 7 ].split( ";" )
			AN = float( numbers[ 0 ].split("=")[ 1 ] ) if "AN" in numbers[ 0 ] else int( numbers[ 1 ].split("=")[ 1 ] )
			AC = float( numbers[ 0 ].split("=")[ 1 ] ) if "AC" in numbers[ 0 ] else int( numbers[ 1 ].split("=")[ 1 ] )
			
			prior = AC / AN
			
			self.prior_list.append( ( pos, alt, reg, prior ) )
		
	def __iter__( self ):
		return self
		
	def __next__( self ):
	
		# Get next variance
		variant = None
		try:
			variant = self.input.__next__()
		except StopIteration:
			raise StopIteration
		
		# Get variance position and set BST index and depth
		variant_pos = variant.position
		depth_index = len( self.prior_list ) / 4
		index = len( self.prior_list ) / 2
		while( True ):
		
			# If off end of list end
			if index < 0 or index > len( self.prior_list ):
				return self.__next__()
		
			node = self.prior_list[ int( index ) ]
			
			# If variant = variant in probabilities file set prob and return
			if variant_pos == node[ 0 ]:
				if variant.old_base == node[ 2 ] and variant.new_base == node[ 3 ]:
					variant.probability = node[ 4 ]
					return variant
					
			# If left go left subtree else right
			# This updates depth and the node index
			if variant_pos < node[ 0 ]:
				index = index - depth_index
				depth_index /= 2
			if variant_pos > node[ 0 ]:
				index = index + depth_index
				depth_index /= 2
				
			# If at leaf, end
			if depth_index < 1:
				return self.__next__()
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		