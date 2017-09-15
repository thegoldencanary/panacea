from pipeline import *

"""
	Manual build
"""
out = DiseaseOutput( PriorTagger( DiseaseFilter( VCFReader( "data/sample_extraction_family.vcf" ) ) , "data/sample_variant_vcf.txt" ), "output" )

out.run()

"""
	Using builder
"""

builder = PipelineBuilder( VCFReader( "data/sample_extraction_family.vcf" ) )

builder.add( DiseaseFilter )
builder.add( PriorTagger, None, "data/sample_variant_vcf.txt" )
builder.add( DiseaseOutput, None, "output" )
pipeline = builder.build()

pipeline.run()