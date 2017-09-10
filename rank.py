


"""
	Tags Variants with prior probability for ranking.
"""
class PriorTagger:

	input = None
	prior_file = None
	
	prior_list = None
	
	def __init__( self, input, prior_file_name ):
	
		self.input = input
		self.prior_file = open( prior_file_name )
		
	def __iter__( self ):
		return self
		
	def __next__( self ):
	
		variant = None
		try:
			variant = self.input.__next__()
		except StopIteration:
			raise StopIteration
		
		
		# Best method: Binary Search Tree for position?