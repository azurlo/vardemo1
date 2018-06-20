#!/bin/bash -l

#SBATCH --mem=1000M

sudo yum install -y python-devel tkinter
sudo pip install -r requirements.txt

symbol=$(< companies.csv head -$(($SLURM_ARRAY_TASK_ID+1)) | tail -1 | cut -d "," -f1)
python vardemo1/randomwalk.py -v -c $symbol -o /tmp --from-csv WIKI_PRICES_5ef6d81a50fea63448e9dbaf8e633881.csv
gsutil cp /tmp/$symbol*.csv gs://risk-vardemo1/
