for f in $@
do 
    P=`basename $f`
    P=${P%%.fastq}
    echo $P $f
    cat $f | split -l 4000000 -d  - ${P}.fastq
done
