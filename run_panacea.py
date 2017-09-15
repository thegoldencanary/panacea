from pipeline import *

out = DiseaseOutput( PriorTagger( DiseaseFilter( VCFReader( "data/sample_extraction_family.vcf" ) ) , "data/sample_variant_vcf.txt" ) )

out.run()