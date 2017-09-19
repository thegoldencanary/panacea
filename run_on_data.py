from pipeline import *

DATA_PATH = "/home/tcs/public_html/COMP555/VCFdata/"
builder = Builder( VCFReader( DATA_PATH + "merged.vcf" ) )
builder.add( ExonFilter, DATA_PATH + "wgEncodeGencodeBasicV17.txt" )
builder.add( DiseaseFilter )
builder.add( PriorTagger, DATA_PATH + "ALL.merged.phase1_release_v3.20101123.snps_indels_svs.vcf" )
pipeline = builder.build()

for v in pipeline:
	print( v )
