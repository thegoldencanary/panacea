from pipeline import *

"""
	Manual build
"""
out = DiseaseOutput( "output", input=PriorTagger("data/sample_variant_vcf.txt", input=DiseaseFilter( input = ExonFilter( "sample_exon.txt", input=VCFReader( "data/sample_extraction_family.vcf" ) ) ) ) )
out.run()

"""
	Using builder
"""

builder = PipelineBuilder( VCFReader( "data/sample_extraction_family.vcf" ) )

builder.add( ExonFilter, "data/sample_exon.txt" )
builder.add( DiseaseFilter )
builder.add( PriorTagger, "data/sample_variant_vcf.txt" )
builder.add( DiseaseOutput,  "output" )
pipeline = builder.build()

pipeline.run()