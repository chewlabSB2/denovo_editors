#!/bin/bash
#SBATCH --job-name=run_name
#SBATCH --gres=gpu:4
#SBATCH -N 1
#SBATCH --mem-per-gpu=21000M
#SBATCH --time=04:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=gpu4w

#load required modules
module load cuda/12.1.1
module load cudnn/8.9.2_cu12

# Add the path to local_alphafold_batch to PATH
export PATH=$PATH:/charonfs/scratch/users/astar/gis/your_username/scratch/denovo_editors/local_alphafold /colabfold-conda/bin
/charonfs/scratch/users/astar/gis/your_username/local_alphafold/colabfold-conda/bin/colabfold_batch --num-recycle 3 --amber --max-msa 64:128 --num-seeds 1 /home/users/astar/gis/your_username/scratch/denovo_editors/ProteinMPNN/outputs/ /home/users/astar/gis/ your_username/scratch/denovo_editors / local_alphafold /outputs/run_name/
