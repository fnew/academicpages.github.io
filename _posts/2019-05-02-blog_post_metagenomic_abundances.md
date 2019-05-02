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

  Input: Raw sequencing reads  
  Program: Prinseq (/programs/prinseq-lite-0.20.2)   
  Script: /workdir/scripts/QC/run_dereplication.qsub

Notes: Files must be uncompressed for this program. Use -no_qual_header to reduce file size and prevent prinseq from adding redundant qual header. This has been modified in original script. 
 
Step 2
------
Removing Human Reads

  Input: Use the output from the dereplication step   
  Program:  BMTOOLS > BMTAGGER (`/programs/bmtools/bmtagger`)   
  Script: /workdir/scripts/QC/run_bmtagger.qsub  

Notes: This step is only needed for metagenomic samples from humans. This step removes human reads that are considered contamination in your samples.

 
Step 3
------
Removing Adapter Sequence and Quality Trimming

  Input: Use the output from the dereplication step (or the bmtagger step if you performed that)  
  Program: Trimmomatic (`/programs/trimmomatic/trimmomatic-0.36.jar`)  
  Scripts: /workdir/scripts/QC/run_trimmomatic.qsub  

Notes: This script removes adapter sequence, uses a sliding window to trim poor quality bases, and removes leading and trailing poor quality bases. It also restricts a minimum read length of 50 (this can be changed depending on your needs). The reference file of adapter sequences is located: `/home/britolab/refdbs/nextera_truseq_adapters.fasta`. The script outputs a FQ file for forward paired, forward singletons, reverse paired, and reverse singletons. 


Alignments
==========
This process will start with quality controlled reads and go through alignments, filtering, and normalization, all the way to gene abundances.

Step 1
------
Align reads to reference

  Program: BWA MEM - run_bwa_mem.qsub  
  Input: Fastq (R1 and R2), assemblies (IDBA), reference (IGC, indexed for BWA)  
  Note: Input reference can be whatever is relevant to your study. It must be indexed for BWA.  
  Output: SAM files  

Step 2
------
SAM -> BAM

Program: Samtools

2a) Filtering step - *Removes alignments with less than 90% identity.* 
  
  Script: run_samfilter.qsub    
  Input: SAM files  
  Output: $NAME_filter.sam  

2b) SAM2BAM - *Removes unaligned reads, keeps only primary alignments, converts to BAM.*
  
  Script: run_sam2bam_twins.qsub  
  Input: filtered SAM files  
  Output: BAM (sorted, indexed, and default)  

Note: at this point, if all BAMs successfully created, you can delete SAM files

Step 3
------
Samtools idxstats

  Script: Run_idxstats.qsub  
  Input: sorted BAM files *(indexed BAM files must be in same directory as the sorted files)*  
  Output: idxstats files *(these contain alignment statistics used in the RPKM script)*  

Step 4
------
Samtools depth - *This is where coverage comes from*

  Script: Run_samtools_depth.qsub  
  Input: sorted BAM files (indexed BAM files must be in same directory as the sorted files). 
  Output: depth files (depth files needed for RPKM)  

Step 5
------
RPKM - *This is a modified version of RPKM that normalizes to the total number of reads sequenced per sample, not the total number of reads mapped. This is because in microbiome research, there is no such concept as a complete reference genome for mapping.*

  Script: Run_rpkm.qsub --> Rpkm_calculate.py  
  Input:  
* Text file containing fastq lengths (not divided by 4, the full length of the file). It should look like:
  Sample name | FQ1 length | FQ2 length		
* Idxstats file
* Depth file
  Output: Logs and gene abundance files (one per sample)  

Step 6
------
Combine and filter the final RPKM table

6a) Filter RPKM files - *keep genes with at least 80% coverage across the gene*

  Script: Run_filterCountsFiles.qsub  
  Input: RPKM files  
  Output: filtered RPKM files *(at this point, the counts are from alignments filtered at 90% identity and 80% coverage)*  

6b) Combine the individual RPKM tables into one big table

  Script: Run_combineGeneAbundances.qsub. 
  Input: filtered RPKM tables. 
  Output: The end result is a table of normalized gene abundances (rows = samples, columns = genes).  

Download
--------
You can see the snakemake file for this pipeline [here](http://fnew.github.io/files/alignment_scripts.zip).
