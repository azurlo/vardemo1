#!/bin/bash -l

#SBATCH -J collect
#SBATCH --mem=1G

echo collected files:
gsutil ls -l gs://risk-vardemo1
