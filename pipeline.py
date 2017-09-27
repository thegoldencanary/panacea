
import re
import os
import math
import operator

"""
	The main class for the Variances. 
	Contains:
		Integer chromosome: The number of the chromosome the variance is found on
		Integer position: The index where the variance occurs
		String old_base: The reference base
		String new_base: The changed base
		String member: The member assigned this variance
		String allele: The inheritance pattern
"""
class Variant:

	chromosome = -1
	position = -1
	old_base = ""
	new_base = ""
	members = []
	diseases = []
	probability = -1.0
	raw_data = ""
	
	def __init__(self, chromosome = -1, position = -1, old_base = "", new_base = "", members = None, diseases = None, probability = -1.0, raw_data = None ):

		self.chromosome = chromosome
		self.position = position
		self.old_base = old_base
		self.new_base = new_base
		if raw_data == None:
			self.raw_data = ""
		else:
			self.raw_data = raw_data
		if members == None:
			self.members = []
		else:
			self.members = members
		if diseases == None:
			self.diseases = []
		else:
			self.diseases = diseases
		self.probability = probability

"""
	The class for reading a vcf file
		Contains:

		Methods:
			read( String filename ):
				returns an iterator of Variant objects
"""
class VCFReader():

	input_file = ""
	SAMPLE_FIELDS = [ "father", "mother", "daughter1", "daughter2", "daughter3", "son1", "son2" ]

	def __init__( self, filename ):
		self.input_file = open( filename )
		self.input_file.readline()
		
	def __iter__( self ):
		return self

	def __next__( self ):

		line = None
		while( True ):
			line = self.input_file.readline()
			if line == "": 
				self.input_file.close()
				#return None
				raise StopIteration
			else:
				if line[ 0 ] == "#": continue
				break
		raw_data = line.strip( "\n" )
		line = line.split()
		
		chromo = line[ 0 ]
		position = int( line[ 1 ] )
		old_base = line[ 3 ]
		new_base = line[ 4 ]
		
		members = []
		for index, sample in enumerate( self.SAMPLE_FIELDS ):
			index += 9
			alleles = line[ index ].split( ":" )[ 0 ]
			if "1" in alleles:
				members.append( ( sample, alleles ) )
		
		v = Variant( chromosome = chromo, position = position, old_base = old_base, new_base = new_base, members = members, diseases=[], raw_data = raw_data )
		return v
		
"""
	This class filters out any variances that are not in an exon
"""			
class ExonFilter:

	input = None #imports of variences
	exons = []
	
	def __init__( self, exon_filename, input=None ):

		exon = open(exon_filename)
		line = exon.readline()
		while line != "":
			splitLine = line.split()
			#getting first lot of tuples without last comma
			beginExon = splitLine[9][0:len(splitLine[9])-1]
			
			beginValues = beginExon.split(',') #should be a list
			beginValues = [ int(x) for x in beginValues ]
			  
			#same for end exon
			endExon = splitLine[10][0:len(splitLine[10])-1]

			endValues = endExon.split(',')
			endValues = [ int(x) for x in endValues ]

			#list of exon ranges 
				  
			for x, y in zip( beginValues, endValues ):
				self.exons.append( ( x, y ) )
			  
			#end of iteration for while loop
			  
			line = exon.readline()
			
		self.input = input
				
	def __iter__( self ):
		return self
				
	def in_bounds( self, v, t ):
		if v >= t[ 0 ] and v <= t[ 1 ]:
			return True
		return False
		
	def __next__( self ):
		
		# Get next variant
		while( True ):
			try:
				variant = self.input.__next__()
			except StopIteration:
				raise StopIteration
			
			variant_pos = variant.position
			end = len( self.exons ) - 1
			begin = 0
			while( True ):
			
				# Set the middle index
				index = begin + int( ( end - begin ) / 2 )
				node = self.exons[ index ]
				
				# If found scan for correct variant
				if self.in_bounds( variant_pos, node ) or self.in_bounds( variant_pos, self.exons[end] ):
					return variant
					
				# If we checked the whole array and found nothing, endf
				if int( ( end - begin ) / 2 ) == 0: break
				
				# if the indexes are the same now, end
				if end == begin:
					break
				
				# If middle node is < or > than indexes, move indexes accordingly.
				if node[ 0 ] < variant_pos:
					begin = index
					continue
				if node[ 1 ] > variant_pos:
					end = index
					continue	


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
	
	def __init__( self, input=None ):
		
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
			
			if self.variant.chromosome in ['Y','X']:
				try:
					self.variant = self.input.__next__()
				except StopIteration:
					raise StopIteration
				continue
		
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
				if any( neg_check ) and not len( neg_check ) == 0: continue
				
				# Tag with disease
				self.variant.diseases.append( disease )
				
			# If no diseases tagged just drop it
			if not len( self.variant.diseases ) == 0:
				return self.variant

			self.variant = self.input.__next__()
			
		raise StopIteration
		



"""
	Tags Variants with prior probability for ranking.
"""
class PriorTagger:

	input = None
	prior_file = None
	
	prior_list = []
	
	def __init__( self, prior_file_name, input=None ):
	
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

		while( True ):
	
			# Get next variance
			variant = None
			try:
				variant = self.input.__next__()
			except StopIteration:
				raise StopIteration
		
			# Get variance position and set indexes
			variant_pos = variant.position
			end = len( self.prior_list ) - 1
			begin = 0
			while( True ):
			
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
					
				if int( ( end - begin ) / 2 ) == 0: break
				
				if end == begin:
					break
				
				if node[ 0 ] < variant_pos:
					begin = index
					continue
				if node[ 0 ] > variant_pos:
					end = index
					continue
					
					
					
"""
	Outputs the variants given into disease files
"""	
class DiseaseOutput:

	input = None
	output = None
	
	diseases = ["sickle cell anaemia",\
	"retinis pigmentosa dominant",\
	"retinis pigmentosa recessive",\
	"severe skeletal dysplasia",\
	"spastic paraplegia dominant",\
	"spastic paraplegia recessive" ]

	DISEASE_PROBABILITY = {}
	DISEASE_PROBABILITY[ diseases[ 0 ] ] = 0.00007
	DISEASE_PROBABILITY[ diseases[ 1 ] ] = 0.00025
	DISEASE_PROBABILITY[ diseases[ 2 ] ] = 0.00025
	DISEASE_PROBABILITY[ diseases[ 3 ] ] = 0.0002
	DISEASE_PROBABILITY[ diseases[ 4 ] ] = 0.00065
	DISEASE_PROBABILITY[ diseases[ 5 ] ] = 0.00065

	disease_outputs = {}

	def __init__( self, output, input=None ):
		self.input = input
		self.output = output
		# Initialize files
		if not os.path.exists( self.output ):
			os.makedirs( self.output )
		for d in self.diseases:
			open( "{0}/{1}".format( self.output, d ), "w" )
		
	def stat( self, variance_prior, disease_prior ):
	
		return abs( disease_prior - variance_prior )
		
	def run( self ):
	
		while( True ):
			# Get variant
			variant = None
			try:
				variant = self.input.__next__()
			except StopIteration:
				break
			
			# Print information
			for disease in variant.diseases:
				try:
					self.disease_outputs[ disease ].append(( "{0}".format( variant.raw_data ), self.stat( variant.probability, self.DISEASE_PROBABILITY[ disease ] ) ))
				except KeyError:
					self.disease_outputs[ disease ] = [( "{0}".format( variant.raw_data ), self.stat( variant.probability, self.DISEASE_PROBABILITY[ disease ] ) ) ]

		for disease in self.diseases:
			values = []
			try:
				values = self.disease_outputs[ disease ]
			except:
				continue
			sorted_d = sorted( values, key=lambda x: x[1] )
			for x in sorted_d:
				print( x[0], file = open( "{0}/{1}".format( self.output, disease ), "a" ) )
				print( str(x[1]), file = open( "{0}/{1}".format( self.output, disease ), "a" ) )

		

class PipelineBuilder:

	pipeline = None
	
	def __init__( self, reader ):
		self.pipeline = reader
		
	def add( self, node_class, *args ):
	
		self.pipeline = node_class( *args, input=self.pipeline  )
		
	def build( self ):
	
		return self.pipeline
		
		
			
		
		
		
					
		
		
		
