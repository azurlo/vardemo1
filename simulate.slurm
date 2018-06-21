#!/bin/bash -l

#SBATCH --mem=1000M

cd /apps/vardemo1

sudo yum install -y python-devel tkinter > /dev/null
sudo pip install -r requirements.txt > /dev/null

symbol=$(< companies.csv head -$(($SLURM_ARRAY_TASK_ID+1)) | tail -1 | cut -d "," -f1)
mkdir /tmp/${USER}
$(python vardemo1/randomwalk.py -c $symbol -o /tmp/${USER} --from-csv WIKI_PRICES_2018-01-01)

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
	echo error $symbol not found in quotes
else
	gsutil cp /tmp/${USER}/${symbol}_*.csv gs://risk-vardemo1/
fi
