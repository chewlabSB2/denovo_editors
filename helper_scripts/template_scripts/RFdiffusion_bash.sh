#!/bin/bash
#SBATCH --job-name=run_name
#SBATCH --gres=gpu:4
#SBATCH -N 1
#SBATCH --mem-per-gpu=21000M
#SBATCH --time=03:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=gpu4w

# Activate the Conda environment for RFdiffusion
source /home/users/astar/gis/your_username/scratch/miniforge3/etc/profile.d/conda.sh
conda activate SE3nv
# Print the path to the Python executable of the activated environment
python -c "import sys; print(sys.executable)"
# Navigate to the RFdiffusion directory (adjust path as needed)
cd /home/users/astar/gis/your_username/scratch/denovo_editors/RFdiffusion/
/home/users/astar/gis/your_username/scratch/miniforge3/envs/SE3nv/bin/python ./scripts/run_inference.py 'contigmap.contigs=[add]' inference.input_pdb=inputs/your.pdb contigmap.length=add inference.output_prefix=outputs/run_number/ diffuser.T=100 inference.num_designs=100 inference.ckpt_override_path=models/Complex_base_ckpt.pt
