#!/bin/bash -l

#SBATCH -J collect
#SBATCH --mem=1G

echo collected files:
gsutil ls -l gs://risk-vardemo1
echo Kick Airflow
gcloud beta composer environments run riskflow trigger_dag --location us-central1 -- var_load
