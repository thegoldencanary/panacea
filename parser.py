
"""
	The main class for the Variances. 
	Contains:
		Integer chromosome: The number of the chromosome the variance is found on
		Integer position: The index where the variance occurs
		String old_base: The reference base
		String new_base: The changed base
		String member: The member assigned this variance
"""
class Variant:

	chromosome = -1
	position = -1
	old_base = ""
	new_base = ""
	member = ""
	
	def __init__(self, chromosome = -1, position = -1, old_base = "", new_base = "", member = "" ):

		self.chromosome = chromosome
		self.position = position
		self.old_base = old_base
		self.new_base = new_base
		self.member = member

"""
	The class for reading a vcf file
		Contains:

		Methods:
			read( String filename ):
				returns an iterator of Variant objects
"""
class vcf_reader():

	 def read( filename ):

		pass
