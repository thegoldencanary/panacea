

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

	DISEASE_RULES_POSITIVE = {}
	DISEASE_RULES_NEGATIVE = {}
	DISEASE_RULES_CHROMOSOME = {}
	
	# Sickle cell has partial disease too?
	DISEASE_RULES_POSITIVE[ "sickle cell anaemia" ] = ["father","mother","daughter1","daughter2","son1","son2"]
	DISEASE_RULES_POSITIVE[ "retinis pigmentosa" ] = ["father","daughter2","son2"]
	DISEASE_RULES_POSITIVE[ "severe skeletal dysplasia" ] = ["daughter2","son1"]
	DISEASE_RULES_POSITIVE[ "spastic paraplegia" ] = ["father","daughter1","daughter3","son2"]
	
	DISEASE_RULES_NEGATIVE[ "sickle cell anaemia" ] = []
	DISEASE_RULES_NEGATIVE[ "retinis pigmentosa" ] = []
	DISEASE_RULES_NEGATIVE[ "severe skeletal dysplasia" ] = []
	DISEASE_RULES_NEGATIVE[ "spastic paraplegia" ] = []
	
	DISEASE_RULES_CHROMOSOME[ "sickle cell anaemia" ] = []
	DISEASE_RULES_CHROMOSOME[ "retinis pigmentosa" ] = []
	DISEASE_RULES_CHROMOSOME[ "severe skeletal dysplasia" ] = []
	DISEASE_RULES_CHROMOSOME[ "spastic paraplegia" ] = []
	
	input = None
	
	def __init__( self, input ):
		
		self.input = input
	
	def __iter__( self ):
		return self
	
	def __next__( self ):
	
		variant = self.input.__next__()
		while variant != None:

			for disease in self.DISEASE_RULES_POSITIVE:
			
				pos_rules = self.DISEASE_RULES_POSITIVE[ disease ]
				neg_rules = self.DISEASE_RULES_NEGATIVE[ disease ]
				chromo = self.DISEASE_RULES_CHROMOSOME[ disease ]
				
				variant_members = [ x for x, y in variant.members ]
				
				chromosome_check = [ True if chromo == variant.chromosome else False for x in chromo ]
				pos_check = [ True if x in variant_members else False for x in pos_rules ]
				neg_check = [ True if x in variant_members else False for x in neg_rules ]
				
				if not any( chromosome_check ) and not len( chromosome_check ) == 0: continue
				if not all( pos_check ) and not len( pos_check ) == 0: continue
				if any( neg_check )and not len( neg_check ) == 0: continue
				
				variant.diseases.append( disease )
				
			if not len( variant.diseases ) == 0: return variant
				
			variant = self.input.__next__()
			
		raise StopIteration
		
		
		
		
		
				