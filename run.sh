#!/bin/bash -l
basedir=$(dirname $0)
N=500

rm -rf /tmp/${USER}*

simulate_job=$(sbatch --array=1-${N} ${basedir}/simulate.slurm | cut -f 4 -d' ')

sbatch --dependency=afterok:${simulate_job} ${basedir}/collect.slurm
