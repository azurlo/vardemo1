#!/bin/bash -l
symbol=$(< companies.csv head -$(($SLURM_ARRAY_TASK_ID+1)) | tail -1 | cut -d "," -f1)
python vardemo1/randomwalk.py -c $symbol -o /tmp
gsutil cp /tmp/${symbol}.csv gs://risk-vardemo1/
