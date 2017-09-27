from pipeline import *


DATA_PATH = "/home/tcs/public_html/COMP555/VCFdata/"

POSITION_POS = 11869
POSITION_NEG = 11867

exon_filter = [Variant( members = [("daughter1",0)], position = POSITION_POS )]
exon_filter_neg = [Variant( members = [("daughter1",0)], position = POSITION_NEG )]

sickle_cell = [Variant( members = [("daughter1",0),("daughter2",0),("son1",0),("son2",0),("father",0),("mother",0)], position = POSITION_POS )]
ret_pig = [Variant( members = [("daughter2",0),("father",0),("son2",0)], position = POSITION_POS )]
sev_ske = [Variant( members = [("daughter2",0),("son1",0)], position = POSITION_POS )]
spas_para = [Variant( members = [("father",0),("daughter3",0),("son2",0),("daughter1",0)], position = POSITION_POS )]

NEG_sickle_cell = [Variant( members = [("daughter3",0)], position = POSITION_POS )]
NEG_ret_pig = [Variant( members = [("son1",0)], position = POSITION_POS ),\
			   Variant( members = [("daughter1",0)], position = POSITION_POS ),\
			   Variant( members = [("daughter3",0)], position = POSITION_POS ),\
			   Variant( members = [("mother",0)], position = POSITION_POS )]
NEG_sev_ske = [Variant( members = [("daughter1",0)], position = POSITION_POS ),\
			   Variant( members = [("father",0)], position = POSITION_POS ),\
			   Variant( members = [("daughter3",0)], position = POSITION_POS ),\
			   Variant( members = [("mother",0)], position = POSITION_POS ),\
			   Variant( members = [("son2",0)], position = POSITION_POS )]
NEG_spas_para = [Variant( members = [("daughter2",0)], position = POSITION_POS ),\
				 Variant( members = [("mother",0)], position = POSITION_POS ),\
				 Variant( members = [("son1",0)], position = POSITION_POS )]

X_Y = [Variant( members = [("daughter2",0),("father",0),("son2",0)], chromosome = 'Y' ),Variant( members = [("daughter2",0),("father",0),("son2",0)], chromosome = 'X' )]
X_Y_NEG = [Variant( members = [("daughter2",0),("father",0),("son2",0)], chromosome = '1' )]


def position_test():

	p = ExonFilter( DATA_PATH + "merged.vcf", input=iter( exon_filter ) )
	result = [ x for x in p ]
	assert( len( result ) == 1 )
	
	p = ExonFilter( DATA_PATH + "merged.vcf", input=iter( exon_filter_neg ) )
	result = [ x for x in p ]
	assert( len( result ) == 0 )
	

def X_Y_test():

	p = DiseaseFilter( input=iter( X_Y ) )
	result = [ x for x in p ]
	print( result )
	assert( len( result ) == 0 )
	
	p = DiseaseFilter( input=iter( X_Y_NEG ) )
	result = [ x for x in p ]
	assert( len( result ) == 1 )
	

def disease_tests():

	p = DiseaseFilter( input=iter( sickle_cell ) )
	result = [ x for x in p ]
	assert( len( result ) == len( sickle_cell ) )
	
	p = DiseaseFilter( input=iter( NEG_sickle_cell ) )
	result = [ x for x in p ]
	assert( len( result ) == 0 )
	
	p = DiseaseFilter( input=iter( ret_pig ) )
	result = [ x for x in p ]
	assert( len( result ) == len( ret_pig ) )
	
	p = DiseaseFilter( input=iter( NEG_ret_pig ) )
	result = [ x for x in p ]
	assert( len( result ) == 0 )

	p = DiseaseFilter( input=iter( sev_ske ) )
	result = [ x for x in p ]
	assert( len( result ) == len( sev_ske ) )
	
	p = DiseaseFilter( input=iter( NEG_sev_ske ) )
	result = [ x for x in p ]
	assert( len( result ) == 0 )
	
	p = DiseaseFilter( input=iter( spas_para ) )
	result = [ x for x in p ]
	assert( len( result ) == len( spas_para ) )
	
	p = DiseaseFilter( input=iter( NEG_spas_para ) )
	result = [ x for x in p ]
	assert( len( result ) == 0 )
	

position_test()
X_Y_test()
disease_tests()
	
	
	
	
	
	