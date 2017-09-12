
import re

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
	
	def __init__(self, chromosome = -1, position = -1, old_base = "", new_base = "", members = None, diseases = None, probability = -1.0 ):

		self.chromosome = chromosome
		self.position = position
		self.old_base = old_base
		self.new_base = new_base
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
	
		line = self.input_file.readline()
		if line == "": 
			self.input_file.close()
			#return None
			raise StopIteration
		line = line.split()
		
		chromo = line[ 0 ]
		position = int( line[ 1 ] )
		old_base = line[ 2 ]
		new_base = line[ 3 ]
		
		members = []
		for index, sample in enumerate( self.SAMPLE_FIELDS ):
			index += 4
			alleles = line[ index ].split( ":" )[ 0 ]
			if "1" in alleles:
				members.append( ( sample, alleles ) )
		
		v = Variant( chromosome = chromo, position = position, old_base = old_base, new_base = new_base, members = members, diseases=[] )
		return v

		
		
		
		
