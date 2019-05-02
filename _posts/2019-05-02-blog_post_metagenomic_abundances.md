---
title: 'Metagenomic Analysis 1: From QC to Gene Abundances'
data: 2019-05-02
permalink: /posts/2019/05/blog_post_metagenomic_abundances/
tags:
  - metagenomics
  - microbiome
  - bioinformatics
  - alignments
---

The standard pipeline that we use in the Brito Lab for quality control, alignments, and gene abundance calculations for metagenomic data.


Quality Control (QC)
====================

Step 1
------
Removing Duplicates
Program: Prinseq (/programs/prinseq-lite-0.20.2)
Script: /workdir/scripts/QC/run_dereplication.qsub
Notes: Files must be uncompressed for this program. Use -no_qual_header to reduce file size and prevent prinseq from adding redundant qual header. This has been modified in original script. 
 
Step 2
------
Removing Human Reads
Notes: This step is only needed for metagenomic samples from humans. This step removes human reads that are considered contamination in your samples.
Input: Use the output from the dereplication step
Program:  BMTOOLS > BMTAGGER (/programs/bmtools/bmtagger)
Script: /workdir/scripts/QC/run_bmtagger.qsub
 
Step 3
------
Removing Adapter Sequence and Quality Trimming
Notes: This script removes adapter sequence, uses a sliding window to trim poor quality bases, and removes leading and trailing poor quality bases. It also restricts a minimum read length of 50 (this can be changed depending on your needs). The reference file of adapter sequences is located: /home/britolab/refdbs/nextera_truseq_adapters.fasta. The script outputs a FQ file for forward paired, forward singletons, reverse paired, and reverse singletons. 
Input: Use the output from the dereplication step (or the bmtagger step if you performed that)
Program: Trimmomatic (/programs/trimmomatic/trimmomatic-0.36.jar)
Scripts: /workdir/scripts/QC/run_trimmomatic.qsub


Alignments
==========
This process will start with quality controlled reads and go through alignments, filtering, and normalization, all the way to gene abundances.

Step 1
------
Align reads to reference
		a. BWA MEM - run_bwa_mem.qsub
		b. Input Fastq (R1 and R2), assemblies (IDBA), reference (IGC, indexed for BWA)
      i. Input reference can be whatever is relevant to your study. It must be indexed for BWA.
		c. Output SAM

Step 2
------
SAM -> BAM
		a. Samtools
		b. Filtering step - run_samfilter.qsub
			i. Removes alignments with less than 90% identity
			ii. Input: SAM files
			iii. Output: $NAME_filter.sam
		c. SAM2BAM - run_sam2bam_twins.qsub
			i.  removes unaligned reads, keeps only primary alignments, converts to BAM
			ii. Input filtered SAM files (part b.iii.)
			iii. Output BAM (sorted, indexed, and default)
			iv. Note: at this point, if all BAMs successfully created, you can delete SAM files

Step 3
------
Samtools idxstats
		a. Run_idxstats.qsub
		b. Input: sorted BAM files (indexed BAM files must be in same directory as the sorted files)
		c. Output: idxstats files (these contain alignment statistics used in the RPKM script)

Step 4
------
Samtools depth
		a. Run_samtools_depth.qsub
		b. This is how you get coverage for the genes
		c. Input: sorted BAM files (indexed BAM files must be in same directory as the sorted files)
		d. Output: depth files (depth files needed for RPKM)

Step 5
------
RPKM - This is a modified version of RPKM that normalizes to the total number of reads sequenced per sample, not the total number of reads mapped. This is because in microbiome research, there is no such concept as a complete reference genome for mapping.

		a. Run_rpkm.qsub --> Rpkm_calculate.py
		b. Input:
			i.  text file containing fastq lengths (not divided by 4, the full length of the file). It should look like:
				`Sample name	FQ1 length	FQ2 length`
			ii. Idxstats file
			iii. Depth file
		c. Output: Logs and gene abundance files (one per sample)

Step 6
------
Combine and filter the final RPKM table
		a. Filter RPKM files to only keep genes with at least 80% coverage across the gene
			i. Run_filterCountsFiles.qsub
			ii. Input: RPKM files
			iii. Output: filtered RPKM files (at this point, the counts are from alignments filtered at 90% identity and 80% coverage)
		b. Combine the individual RPKM tables into one big table
			i. Run_combineGeneAbundances.qsub
			ii. Input: filtered RPKM tables
			iii. Output: One large filtered RPKM table for the entire dataset (this table will be long, i.e. genes on the rows and samples on the columns)
      
The end result is a table of normalized gene abundances (rows = samples, columns = genes).

Download
--------
You can see the snakemake file for this pipeline [here](http://fnew.github.io/files/alignment_scripts.zip).
