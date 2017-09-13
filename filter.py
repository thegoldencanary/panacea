
"""
	The class for the main filter
	Includes several dictionaries for rules:
		POSITIVE: Contains the list of members that a variant must have ( those with the disease )
		NEGATIVE: Contains the list of members that a variant can't have ( decided by the hiearchy )
		CHROMOSOME: Contains the list of chromosomes the variant must be expressed on
		
	empty list is treated as an all filter
		
	Iterator for variants, adds disease information
	
"""

class DiseaseFilter:

	# Setup rules for filtering variances per disease
	
	DISEASE_RULES_POSITIVE = {}
	DISEASE_RULES_NEGATIVE = {}
	DISEASE_RULES_CHROMOSOME = {}
	
	DISEASE_RULES_POSITIVE[ "sickle cell anaemia" ] = ["daughter2","son2"]
	DISEASE_RULES_POSITIVE[ "retinis pigmentosa dominant" ] = ["father","daughter2","son2"]
	DISEASE_RULES_POSITIVE[ "retinis pigmentosa recessive" ] = ["father","daughter2","son2"]
	DISEASE_RULES_POSITIVE[ "severe skeletal dysplasia" ] = ["daughter2","son1"]
	DISEASE_RULES_POSITIVE[ "spastic paraplegia dominant" ] = ["father","daughter1","daughter3","son2"]
	DISEASE_RULES_POSITIVE[ "spastic paraplegia recessive" ] = ["father","daughter1","daughter3","son2"]
	
	DISEASE_RULES_NEGATIVE[ "sickle cell anaemia" ] = ["daughter3"]
	DISEASE_RULES_NEGATIVE[ "retinis pigmentosa dominant" ] = ["mother","daughter1","daughter3","son1"]
	DISEASE_RULES_NEGATIVE[ "retinis pigmentosa recessive" ] = []
	DISEASE_RULES_NEGATIVE[ "severe skeletal dysplasia" ] = []
	DISEASE_RULES_NEGATIVE[ "spastic paraplegia dominant" ] = ["mother","daughter2","son1"]
	DISEASE_RULES_NEGATIVE[ "spastic paraplegia recessive" ] = []
	
	DISEASE_RULES_CHROMOSOME[ "sickle cell anaemia" ] = []
	DISEASE_RULES_CHROMOSOME[ "retinis pigmentosa dominant" ] = []
	DISEASE_RULES_CHROMOSOME[ "retinis pigmentosa recessive" ] = []
	DISEASE_RULES_CHROMOSOME[ "severe skeletal dysplasia" ] = []
	DISEASE_RULES_CHROMOSOME[ "spastic paraplegia dominant" ] = []
	DISEASE_RULES_CHROMOSOME[ "spastic paraplegia recessive" ] = []
	
	input = None
	
	variant = None
	
	def __init__( self, input ):
		
		self.input = input
	
	def __iter__( self ):
		return self
	
	def __next__( self ):
	
		# Get next variance
		try:
			self.variant = self.input.__next__()
		except StopIteration:
			raise StopIteration
		
		while self.variant != None:
			
			# For each disease
			for disease in self.DISEASE_RULES_POSITIVE:
			
				# Get rules and members with variance
				pos_rules = self.DISEASE_RULES_POSITIVE[ disease ]
				neg_rules = self.DISEASE_RULES_NEGATIVE[ disease ]
				chromo = self.DISEASE_RULES_CHROMOSOME[ disease ]
				variant_members = [ x for x, y in self.variant.members ]
				
				# Check if applicable
				chromosome_check = [ True if chromo == self.variant.chromosome else False for x in chromo ]
				pos_check = [ True if x in variant_members else False for x in pos_rules ]
				neg_check = [ True if x in variant_members else False for x in neg_rules ]
				
				if not any( chromosome_check ) and not len( chromosome_check ) == 0: continue
				if not all( pos_check ) and not len( pos_check ) == 0: continue
				if any( neg_check )and not len( neg_check ) == 0: continue
				
				# Tag with disease
				self.variant.diseases.append( disease )
				
			# If no diseases tagged just drop it
			if not len( self.variant.diseases ) == 0:
				return self.variant

			self.variant = self.input.__next__()
			
		raise StopIteration
		
		
		
		
		
				