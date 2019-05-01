#!/usr/bin/env python

import sys, getopt
import glob, os

# MergeHash can maybe go on the hour queue

JobParams = {
	'CreateHash': {
		'outfile': """CreateHash_Job.q""",
		'header': ["""#$ -N CreateHash""","""#$ -o PROJECT_HOME/Logs/CreateHash-Out.out""","""#$ -e PROJECT_HOME/Logs/CreateHash-Err.err"""],
		'body': ["""python LSA/create_hash.py -i PROJECT_HOME/original_reads/ -o PROJECT_HOME/hashed_reads/ -k 33 -s 31"""]},
	'HashReads': {
		'outfile': """HashReads_ArrayJob.q""",
		'array': ["""original_reads/""","""*.fastq.*"""],
		'header': ["""#$ -N HashReads[1-""","""#$ -o PROJECT_HOME/Logs/HashReads-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/HashReads-Err-%I.err""","""#$ -t 1-8"""],
		# add -z option to omit reverse complimenting
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python LSA/hash_fastq_reads.py -r ${SGE_TASK_ID} -i PROJECT_HOME/original_reads/ -o PROJECT_HOME/hashed_reads/"""]},
	'MergeHash': {
		'outfile': """MergeHash_ArrayJob.q""",
		'array': ["""original_reads/""","""*.fastq""",5],
		'header': ["""#$ -N MergeHash[1-""","""#$ -o PROJECT_HOME/Logs/MergeHash-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/MergeHash-Err-%I.err""","""#$ -pe parenv 4""","""#$ -t 1-8"""],
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python LSA/merge_hashq_files.py -r ${SGE_TASK_ID} -i PROJECT_HOME/hashed_reads/ -o PROJECT_HOME/hashed_reads/"""]},
	'CombineFractions': {
		'outfile': """CombineFractions_ArrayJob.q""",
		'array': ["""original_reads/""","""*.fastq""",1],
		'header': ["""#$ -N CombineFractions[1-""","""#$ -o PROJECT_HOME/Logs/CombineFractions-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/CombineFractions-Err-%I.err""","""#$ -pe parenv 4""","""#$ -t 1-20"""],
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python LSA/merge_hashq_fractions.py -r ${SGE_TASK_ID} -i PROJECT_HOME/hashed_reads/ -o PROJECT_HOME/hashed_reads/"""]},
	'GlobalWeights': {
		'outfile': """GlobalWeights_Job.q""",
		'header': ["""#$ -N GlobalWeights""","""#$ -o PROJECT_HOME/Logs/GlobalWeights-Out.out""","""#$ -e PROJECT_HOME/Logs/GlobalWeights-Err.err"""],
		'body': ["""python LSA/tfidf_corpus.py -i PROJECT_HOME/hashed_reads/ -o PROJECT_HOME/cluster_vectors/"""]},
	'KmerCorpus': {
		'outfile': """KmerCorpus_ArrayJob.q""",
		'array': ["""hashed_reads/""","""*.count.hash"""],
		'header': ["""#$ -N KmerCorpus[1-""","""#$ -o PROJECT_HOME/Logs/KmerCorpus-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/KmerCorpus-Err-%I.err"""],
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python LSA/kmer_corpus.py -r ${SGE_TASK_ID} -i PROJECT_HOME/hashed_reads/ -o PROJECT_HOME/cluster_vectors/"""]},
	'KmerLSI': {
		'outfile': """KmerLSI_Job.q""",
		'header': ["""#$ -N KmerLSI""","""#$ -o PROJECT_HOME/Logs/KmerLSI-Out.out""","""#$ -e PROJECT_HOME/Logs/KmerLSI-Err.err""","""#$ -n 6""","""python -m Pyro4.naming -n 0.0.0.0 > PROJECT_HOME/Logs/nameserver.log 2>&1 &""","""P1=$!""","""python -m gensim.models.lsi_worker > PROJECT_HOME/Logs/worker1.log 2>&1 &""","""P2=$!""","""python -m gensim.models.lsi_worker > PROJECT_HOME/Logs/worker2.log 2>&1 &""","""P3=$!""","""python -m gensim.models.lsi_worker > PROJECT_HOME/Logs/worker3.log 2>&1 &""","""P4=$!""","""python -m gensim.models.lsi_worker > PROJECT_HOME/Logs/worker4.log 2>&1 &""","""P5=$!""","""python -m gensim.models.lsi_worker > PROJECT_HOME/Logs/worker5.log 2>&1 &""","""P6=$!""","""python -m gensim.models.lsi_dispatcher > PROJECT_HOME/Logs/dispatcher.log 2>&1 &""","""P7=$!"""],
		'body': ["""python LSA/kmer_lsi.py -i PROJECT_HOME/hashed_reads/ -o PROJECT_HOME/cluster_vectors/""","""kill $P1 $P2 $P3 $P4 $P5 $P6 $P7"""]},
	'KmerClusterIndex': {
		'outfile': """KmerClusterIndex_Job.q""",
		'header': ["""#$ -N KmerClusterIndex""","""#$ -o PROJECT_HOME/Logs/KmerClusterIndex-Out.out""","""#$ -e PROJECT_HOME/Logs/KmerClusterIndex-Err.err"""],
		# adjust cluster thresh (-t) as necessary
		'body': ["""python LSA/kmer_cluster_index.py -i PROJECT_HOME/hashed_reads/ -o PROJECT_HOME/cluster_vectors/ -t 0.7""","""python LSFScripts/create_jobs.py -j KmerClusterParts -i ./""","""X=`sed -n 1p hashed_reads/hashParts.txt`""","""sed -i 's/%parts%/$X/g' LSFScripts/KmerClusterParts_ArrayJob.q""","""python LSFScripts/create_jobs.py -j LSFScripts/KmerClusterMerge -i ./""","""X=`sed -n 1p cluster_vectors/numClusters.txt`""","""sed -i 's/%clusters%/$X/g' LSFScripts/KmerClusterMerge_ArrayJob.q"""]},
	'KmerClusterParts': {
		'outfile': """KmerClusterParts_ArrayJob.q""",
		# number of tasks is 2**hash_size/10**6 + 1
		#'array': ["""hashed_reads/""","""*.hashq.*"""],
		'header': ["""#$ -N KmerClusterParts[1-%parts%]""","""#$ -o PROJECT_HOME/Logs/KmerClusterParts-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/KmerClusterParts-Err-%I.err"""],
		###!!!
		# adjust cluster thresh (-t) as necessary - probably same as Index step (maybe slightly higher)
		###!!!
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python LSA/kmer_cluster_part.py -r ${SGE_TASK_ID} -i PROJECT_HOME/hashed_reads/ -o PROJECT_HOME/cluster_vectors/ -t 0.7"""]},
	'KmerClusterMerge': {
		'outfile': """KmerClusterMerge_ArrayJob.q""",
		# number of tasks is number of clusters
		#'array': ["""hashed_reads/""","""*.hashq.*"""],
		'header': ["""#$ -N KmerClusterMerge[1-%clusters%]""","""#$ -o PROJECT_HOME/Logs/KmerClusterMerge-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/KmerClusterMerge-Err-%I.err"""],
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python LSA/kmer_cluster_merge.py -r ${SGE_TASK_ID} -i PROJECT_HOME/cluster_vectors/ -o PROJECT_HOME/cluster_vectors/"""]},
	'KmerClusterCols': {
		'outfile': """KmerClusterCols_Job.q""",
		'header': ["""#$ -N KmerClusterCols""","""#$ -o PROJECT_HOME/Logs/KmerClusterCols-Out.out""","""#$ -e PROJECT_HOME/Logs/KmerClusterCols-Err.err""","""#$ -q long.q@cbsubrito2"""],
		'body': ["""python LSA/kmer_cluster_cols.py -i PROJECT_HOME/hashed_reads/ -o PROJECT_HOME/cluster_vectors/"""]},
	'ReadPartitions': {
		'outfile': """ReadPartitions_ArrayJob.q""",
		'array': ["""hashed_reads/""","""*.hashq.*"""],
		# MAKE SURE TO SET TMP FILE LOCATION
		'header': ["""#$ -N ReadPartitions[1-""","""#$ -o PROJECT_HOME/Logs/ReadPartitions-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/ReadPartitions-Err-%I.err"""],
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python LSA/write_partition_parts.py -r ${SGE_TASK_ID} -i PROJECT_HOME/hashed_reads/ -o PROJECT_HOME/cluster_vectors/ -t TMPDIR"""]},
	'MergeIntermediatePartitions': {
		'outfile': """MergeIntermediatePartitions_ArrayJob.q""",
		'array': ["""cluster_vectors/""","""*.cluster.npy"""],
		'header': ["""#$ -N MergeIntermediatePartitions[1-""","""#$ -o PROJECT_HOME/Logs/MergeIntermediatePartitions-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/MergeIntermediatePartitions-Err-%I.err"""],
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python LSA/merge_partition_parts.py -r ${SGE_TASK_ID} -i PROJECT_HOME/cluster_vectors/ -o PROJECT_HOME/read_partitions/"""]},
	# Check to make sure there are no files remaining in cluster_vectors/PARTITION_NUM/
	'SplitPairs': {
		'outfile': """SplitPairs_ArrayJob.q""",
		'array': ["""cluster_vectors/""","""*.cluster.npy"""],
		'header': ["""#$ -N SplitPairs[1-""","""#$ -o PROJECT_HOME/Logs/SplitPairs-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/SplitPairs-Err-%I.err""","""#$ -pe parenv 4"""],
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python LSA/split_read_pairs.py -r ${SGE_TASK_ID} -i PROJECT_HOME/read_partitions/ -o PROJECT_HOME/read_partitions/"""]},
	'PhylerClassify': {
		'outfile': """PhylerClassify_ArrayJob.q""",
		'array': ["""cluster_vectors/""","""*.cluster.npy"""],
		'header': ["""#$ -N PhylerClassify[1-""","""#$ -o PROJECT_HOME/Logs/PhylerClassify-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/PhylerClassify-Err-%I.err""","""source /broad/software/scripts/useuse""","""reuse BLAST"""],
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python misc/phyler_classify.py -r ${SGE_TASK_ID} -i PROJECT_HOME/read_partitions/ -o PROJECT_HOME/phyler/"""]},
	'PhylerIdentify': {
		'outfile': """PhylerIdentify_ArrayJob.q""",
		'array': ["""cluster_vectors/""","""*.cluster.npy"""],
		'header': ["""#$ -N PhylerIdentify[1-""","""#$ -o PROJECT_HOME/Logs/PhylerIdentify-Out-%I.out""","""#$ -e PROJECT_HOME/Logs/PhylerIdentify-Err-%I.err"""],
		'body': ["""sleep $(($SGE_TASK_ID % 60))""","""python misc/phyler_identify.py -r ${SGE_TASK_ID} -i PROJECT_HOME/read_partitions/ -o PROJECT_HOME/phyler/"""]},
	'PhylerSummary': {
		'outfile': """PhylerSummary_Job.q""",
		'header': ["""#$ -N PhylerSummary""","""#$ -o PROJECT_HOME/Logs/PhylerSummary-Out.out""","""#$ -e PROJECT_HOME/Logs/PhylerSummary-Err.err"""],
		'body': ["""python misc/phyler_summary.py -i PROJECT_HOME/phyler/"""]}
}

CommonElements = {
	'header': ["""#!/bin/bash"""],
	'body': ["""echo Date: `date`""","""t1=`date +%s`"""],
	'footer': ["""[ $? -eq 0 ] || echo 'JOB FAILURE: $?'""","""echo Date: `date`""","""t2=`date +%s`""","""tdiff=`echo 'scale=3;('$t2'-'$t1')/3600' | bc`""","""echo 'Total time:  '$tdiff' hours'"""]
}
					
help_message = 'usage example: python create_jobs.py -j HashReads -i /project/home/'
if __name__ == "__main__":
	job = 'none specified'
	try:
		opts, args = getopt.getopt(sys.argv[1:],'hj:i:',["--jobname","inputdir="])
	except:
		print help_message
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h','--help'):
			print help_message
			sys.exit()
		elif opt in ('-j',"--jobname"):
			job = arg
		elif opt in ('-i','--inputdir'):
			inputdir = arg
			if inputdir[-1] != '/':
				inputdir += '/'
	try:
		params = JobParams[job]
	except:
		print job+' is not a known job.'
		print 'known jobs:',JobParams.keys()
		print help_message
		sys.exit(2)
	if params.get('array',None) != None:
		FP = glob.glob(os.path.join(inputdir+params['array'][0],params['array'][1]))
		if len(params['array']) == 3:
			FP = [fp[fp.rfind('/')+1:] for fp in FP]
			if params['array'][2] == -1:
				suffix = params['array'][1].replace('*','').replace('.','')
				FP = set([fp[:fp.index(suffix)] for fp in FP])
			else:
				FP = set([fp[:fp.index('.')] for fp in FP])
			FP = [None]*len(FP)*abs(params['array'][2])
		array_size = str(len(FP))
		params['header'][0] += array_size+']'
		print job+' array size will be '+array_size
	f = open(inputdir+'LSFScripts/'+params['outfile'],'w')
	f.write('\n'.join(CommonElements['header']) + '\n')
	f.write('\n'.join(params['header']).replace('PROJECT_HOME/',inputdir) + '\n')
	f.write('\n'.join(CommonElements['body']) + '\n')
	f.write('\n'.join(params['body']).replace('PROJECT_HOME/',inputdir) + '\n')
	f.write('\n'.join(CommonElements['footer']) +'\n')
	f.close()
	
