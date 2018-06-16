#!/bin/bash -l

N=3

simulate_job=$(sbatch --array=1-${N} simulate.slurm | cut -f 4 -d' ')

sbatch --dependency=afterok:${simulate_job} collect.slurm
