---
title: 'Using Latent Strain Analysis (LSA)'
data: 2019-05-01
permalink: /posts/2019/05/blog_post_lsa/
tags:
  - strain
  - server
  - latent strain analysis
  - lsa
  - metagenomics
---

LSA was developed as a pre-assembly tool for partitioning metagenomic reads. It uses a hyperplane hashing function and streaming SVD in order to find covariance relations between k-mers. The code, and the process outline in LSFScripts in particular, have been optimized to scale to massive data sets in fixed memory with a highly distributed computing environment.
For resources on LSA, see the following:
  [Manual](http://latentstrainanalysis.readthedocs.io/en/latest/large_collections.html)
  [Github](https://github.com/brian-cleary/LatentStrainAnalysis/tree/master/misc)
  [Useful Tips](https://comptips.wordpress.com/lsa/)
  [Reference](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4720164/)

I thought it might be useful to outline the steps to run LSA from my own experience. Here I will go step by step how I was able to run LSA on a Linux computer.


Step 1
------
Copy the LSA folder to your local : 
   
`cd my_local_directory`<br/>
`tar -xf /local/LSA/LatentStrainAnalysis.tar`

Familiarize yourself with all of the directories included, especially /LatentStrainAnalysis/LSFScripts. 


Step 2
------
Initialize the environment. 

This step creates submission scripts and folders for use in the pipeline. This script is found in the /LSFScripts folder. Arguments include -I input directory, -n number of samples:

`python LSFScripts/setupDirs.py -i /input/reads/ -n #`

Step 3
-------
Split your reads. 

You have to split your fastq files into smaller chunks. LSA provides a script that will do this, but it is proving to be too difficult to modify for my own data. A lot of the programs are hard-coded and looking for certain types of files (pair1, pair2, singleton) and I don't have data that look like that. I'm using instead a little script to split the reads myself: [splitfastq.sh](http://fnew.github.io/files/splitfastq.sh)
	
To run, type: `sh splitfastqs.sh *.fastq` within the folder that contains the fastq files

Copy the FQ files for analysis to the LSA folder
Split the reads within the same folder
  
  
Step 4
-------
Generate the hash function.

Create a k-mer hash function by drawing a bunch of random hyperplanes. If you want to adjust the k-mer length or hash size, alter the “-k” or “-s” arguments in the create_hash.py command of CreateHash_Job.q.:

`python create_jobs.py -j CreateHash -i $WRK`<br/>
`python create_jobs.py -j CreateHash -I /workdir/users/fnn3/lsa_twins/LatentStrainAnalysis/`<br/>
`qsub CreateHash_Job.q #This script is created in the previous line`

This hash function will be found in: `/LSFScripts/hashed_reads/Wheels.txt`
	
NOTE: Some notes on the '.q' files: These are set up for a different type of scheduler, not SGE.  I have edited the python script that creates them to make them work for our own server, but it's important to still check the generated submission scripts for errors. Check the create_jobs.py script to see if the commands and defaults make sense for your own server set up. You can see how I edited mine here: [create_jobs.py](http://fnew.github.io/files/create_jobs.py)
	
I edited the script fastq_reader.py and fastq_reader.pyc. These are found in the /LSA/ folder. You can use my versions here: 
[fastq_reader.py](http://fnew.github.io/files/fastq_reader.py), and [fastq_reader.pyc](http://fnew.github.io/files/fastq_reader.pyc).
	

Step 5
-------
Hashing all the reads:

`python LSFScripts/create_jobs.py -j HashReads -i $WRK`<br/>
`qsub LSFScripts/HashReads_ArrayJob.q`

The job array is set by the number of chunks created with the splitfastqs.sh script, here I have: 1,496 chunks. At this stage, if a few jobs fail, you can still move forward, but those chunks will be left out. Check the logs for jobs that did not work.
	
This is the longest step. It took about 48 hours to complete hashing reads on 1,496 chunks. 


Step 6
-------
6a
--
Hashed k-mer counting

Tabulating k-mer counts in 1/5th of each sample:

First, make sure that there is just one .fastq file per sample in original_reads/. The reason this is important is that the number of *.fastq files will be used to determine the array size. (The *.fastq. files are no longer needed, so you can remove those as well if you want).:

`python LSFScripts/create_jobs.py -j MergeHash -i $WRK`	<br/>
`python create_jobs.py -j MergeHash -i /workdir/users/fnn3/lsa_twins/LatentStrainAnalysis`<br/>
`qsub LSFScripts/MergeHash_ArrayJob.q`
	
NOTE: I had to change the hard coding in the source code "hash_counting.py" from `.*.hashq.*` to `*hashq*`, and also in merge_hashq_files.py. You can see my versions here: [hash_counting.py](http://fnew.github.io/files/hash_counting.py), and [merge_hashq_files.py](http://fnew.github.io/files/merge_hashq_files.py).

NOTE: There should be five files per sample as the output. The array job size is number of samples X 5, I have 32 samples going in, so : `#$ -t 1-160` 


6b
---
Combining the 5 counts files for each sample:

`python LSFScripts/create_jobs.py -j CombineFractions -i $WRK`<br/>
`qsub LSFScripts/CombineFractions_ArrayJob.q`

It is important that these jobs finish, check logs.

NOTE: Make sure to adjust the submission script: the headers and the directories within the command.<br/>
NOTE: The number of tasks = the number of samples
	
  
Step 7
------
7a
--
Create the abundance matrix

Global (k-mer) conditioning:

`python LSFScripts/create_jobs.py -j GlobalWeights -i $WRK`<br/>
`qsub LSFScripts/GlobalWeights_Job.q`

This launches a single job that must succeed to continue. Should produce `cluster_vectors/global_weights.npy`

TIME: 3 minutes<br/>
MEMORY: 70G (for my dataset)<br/>
NOTE: This job must succeed to continue.<br/>

IMPORTANT: Add these lines to the scripts for 7a and 7b:

`export PATH=/programs/Anaconda2/bin:$PATH`<br/>
`export LD_LIBRARY_PATH=/programs/Anadonda2/lib:$LD_LIBRARY_PATH`


7b
---
Writing matrix rows to separate files, and computing local (sample) conditioning:

`python LSFScripts/create_jobs.py -j KmerCorpus -i $WRK`<br/>
`qsub LSFScripts/KmerCorpus_ArrayJob.q`


May create file ‘core’ in LatentStrainAnalysis directory if the job fails.<br/>
Creates one `.../hashed_reads/*count.hash.conditioned` file per sample<br/>
MEMORY: 60G per sample<br/>
TIME: 15 min per sample<br/>
NOTE: These jobs must all complete to continue. Relaunch any that failed.

IMPORTANT: Add these lines to the scripts for 7a and 7b:

`export PATH=/programs/Anaconda2/bin:$PATH  `<br/>
`export LD_LIBRARY_PATH=/programs/Anadonda2/lib:$LD_LIBRARY_PATH`


Step 8
------
Calculating the streaming SVD

`python LSFScripts/create_jobs.py -j KmerLSI -i $WRK`<br/>
`qsub  LSFScripts/KmerLSI_Job.q`

MEMORY: 60G, distributed<br/>
TIME: 7.115 hrs (64 small samples), 6.030 hrs (12 large samples), scales with the number of samples. For very large matrices, this one will probably take a couple days to complete.<br/>
Will produce `cluster_vectors/kmer_lsi.gensim`.

Add these to the submission script:

`export PYRO_SERIALIZERS_ACCEPTED=serpent,json,marshal,pickle`<br/>
`export PYRO_SERIALIZER=pickle`<br/>
`export PATH=/programs/Anaconda2/bin:$PATH`<br/>
`export LD_LIBRARY_PATH=/programs/Anadonda2/lib:$LD_LIBRARY_PATH`			


Script has to be run in a screen like this: `bash KmerLSI_Job.q` (I do not know why, it just does).<br/>
This step ran for 11 hours on this dataset. 


Step 9
-------
Kmer clustering

9a
---
Create the cluster index

`python LSFScripts/create_jobs.py -j KmerClusterIndex -i $WRK`<br/>
`qsub  LSFScripts/KmerClusterIndex_Job.q`
	
This step will set the k-mer cluster seeds, and the number of these seeds ultimately affects the resolution of partitioning. It is highly recommended that you check cluster_vectors/numClusters.txt for the number of clusters. If the resolution is markedly different from the expected / desired resolution, this job should be re-run with a different `-t` value in the submission script. From the manual: 

>Roughly speaking, we’ve found the following values to work for different scale datasets: 0.5-0.65 for large scale (Tb), 0.6-0.8 for medium scale (100Gb), >0.75 for small scale (10Gb). See misc/parameters.xlsx for more info.
	
NOTE: Add this to the submission script

`export PATH=/programs/Anaconda2/bin:$PATH`<br/>
`export LD_LIBRARY_PATH=/programs/Anadonda2/lib:$LD_LIBRARY_PATH`

Remember to edit directory paths in the submission script.
	
NOTE: This `–t` option is not how the manual makes it seem. My dataset is ~500GB, when I use `–t 0.6`, I get 19 clusters, when I do `–t 0.8` I get 1406 clusters.
	
This should produce the files: `cluster_vectors/numClusters.txt` and `cluster_vectors/cluster_index.npy`.


9b
---
Cluster blocks of k-mers:

`$ qsub  LSFScripts/KmerClusterParts_ArrayJob.q`

The number of tasks is: 2 ** hash size / 10e6 + 1<br/>
You get hash size from the CreateHash_Job.q script, it is `-s`. This is set to 31 by default. So the number of tasks is 2,148.<br/>
This step creates numbered directories in ./cluster_vectors/ for the number of clusters<br/>
TIME: 1 min per task, 2148 tasks = 16 min if highly distributed<br/>
MEMORY: 15G per task


9c
--
Merge cluster blocks:

`qsub  LSFScripts/KmerClusterMerge_ArrayJob.q`

This step creates ******.npy in cluster_vectors<br/>
NOTE: deletes the directories from above<br/>
TIME: FAST, but I had few reads sorted<br/>
MEMORY: 23G per task<br/>
Number of tasks:  The number of tasks is equal to the number of clusters, which comes from `cluster_vectors/numClusters.txt` (from Step 9a)


9d
---
Arrange k-mer clusters on disk:

`python ../LSFScripts/create_jobs.py -j KmerClusterCols -i $WRK`<br/>
`qsub  LSFScripts/KmerClusterCols_Job.q`

NOTE: Add this to the submission script

`export PATH=/programs/Anaconda2/bin:$PATH`<br/>
`export LD_LIBRARY_PATH=/programs/Anadonda2/lib:$LD_LIBRARY_PATH`

This step creates:
  cluster_vectors/cluster_cols.npy<br/>
  cluster_vectors/cluster_probs.npy<br/>
  cluster_vectors/cluster_vals.npy<br/>
  cluster_vectors/kmer_cluster_sizes.npy<br/>
  cluster_vectors/*cluster.npy
  
TIME: 4 min<br/>
MEMORY: 60G


Step 10
--------
Read Partitioning

Partition all the read chunks:

`python .../LSFScripts/create_jobs.py -j ReadPartitions -i $WRK`

You’ll need to modify ReadPartitions_ArrayJob.q to contain your tmp directory of choice.

`sed 's/TMPDIR/\/your\/tmp\/dir/g' < LSFScripts/ReadPartitions_ArrayJob.q | bsub`

NOTE: sed is not necessary with these scripts, you can set tmp directory as `/partitions_tmp`
The script will create numbered directories for each chunk in `/partitions_tmp` and eventually writes files into `/cluster_vectors/` numbered directories.<br/>
NOTE: May stall out on a few partitions. If a few fail it’s OK, but if many fail you should resubmit them.<br/>
TIME: 4 hrs per task<br/>
Number of tasks = number of chunks = the number of chunks that your original fastq files are split up into-- NOT the number of clusters from Step 9a.<br/>
MEMORY: 7G per task

NOTE: I changed `*.hashq.*` to `*hashq*` in the write_partition_parts.py

Step 11
-------
Merge Partition parts 

Merge the partition chunks:

`python ../LSFScripts/create_jobs.py -j MergeIntermediatePartitions -i $WRK`<br/>
`qsub  LSFScripts/MergeIntermediatePartitions_ArrayJob.q`

NOTE: Number of tasks = number of partitions = the number of clusters from Step 9a.<br/>
If any of these jobs fail you’ll need to resubmit them.


And that is the end of the LSA pipeline! From here, I typically assemble the bins (partitions from LSA) and then identify AMPHORA genes (or something similar) to taxanomically annotate and assess the contamination level of the bins. 
