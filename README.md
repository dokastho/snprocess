# SNPROCESS
  by Thomas Dokas
  
  <dokastho@umich.edu>
  
  SNProcess is a Single Nucleotide Polymorphism (SNP) Quality Control pipeline, written in python
  the procedure was developed by <INSERT LAB NAME HERE>.
## QC1
Steps for QC:
1. Check missingness and generate plots
2. Remove individuals with high missingness
3. Remove individuals with outlying gender SNP's
4. Select autosomal SNPs only and filter out SNPs with low minor allele frequency (MAF)
5. Delete SNPs not in the Hardy-WEinberg equilibrium (HWE)
6. Heterozygosity and LD Pruning

## QC2
This portion of the pipeline compares the user data with data in the 1,000 genome project and produces graphs that show the population stratification based on race & ethnicity