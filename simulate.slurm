#!/bin/bash -l

#SBATCH -J simulate
#SBATCH --mem=1G
#SBATCH -c1

dir=${1}

# sudo yum install -y python-devel tkinter > /dev/null
( cd $dir; sudo pip install -r requirements.txt 2> /dev/null 1> /dev/null )

symbol=$(< $dir/companies.csv head -$(($SLURM_ARRAY_TASK_ID+1)) | tail -1 | cut -d "," -f1)

( python $dir/vardemo1/randomwalk.py -c $symbol --from-csv $dir/WIKI_PRICES_2018-01-01; if [ $? != 0 ]; then >&2 echo error $symbol; fi ) | gsutil -q cp - gs://risk-vardemo1/${symbol}.csv
