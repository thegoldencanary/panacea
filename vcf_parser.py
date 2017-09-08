
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
	member = ""
	alleles = ""
	
	def __init__(self, chromosome = -1, position = -1, old_base = "", new_base = "", member = "" ,alleles = ""):

		self.chromosome = chromosome
		self.position = position
		self.old_base = old_base
		self.new_base = new_base
		self.member = member
		self.alleles = alleles

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
	variants = []

	def __init__( self, filename ):
		self.input_file = open( filename )
		
	def __iter__( self ):
		return self
		
	def __next__( self ):

		if len( self.variants ) == 0:
	
			line = self.input_file.readline()
			if line == "": raise StopIteration
			line = line.split()
			
			chromo = line[ 0 ]
			position = line[ 1 ]
			old_base = line[ 2 ]
			new_base = line[ 3 ]
			
			for index, sample in enumerate( self.SAMPLE_FIELDS ):
				index += 4
				alleles = line[ index ].split( ":" )[ 0 ]
				if "1" not in alleles:
					continue 
				found = Variant( chromosome = chromo, position = position, old_base = old_base, new_base = new_base, alleles = alleles, member = sample )
				self.variants.append( found )

		return self.variants.pop()
		
		
		
		
