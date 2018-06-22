#!/bin/bash -l
basedir=$(dirname $0)
N=500

simulate_job=$(sbatch --array=1-${N} ${basedir}/simulate.slurm ${basedir} | cut -f 4 -d' ')

sbatch --dependency=afterok:${simulate_job} ${basedir}/collect.slurm
