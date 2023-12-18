#!/bin/bash
#SBATCH --job-name=run_name
#SBATCH --gres=gpu:4
#SBATCH -N 1
#SBATCH --mem-per-gpu=21000M
#SBATCH --time=01:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=gpu4w
source /home/users/astar/gis/diyasri/scratch/miniforge3/etc/profile.d/conda.sh
mamba activate my_mlfold

# Define the directory containing PDB files and the directory with JSON files
pdb_dir="/home/users/astar/gis/your_username/scratch/denovo_editors/RFdiffusion/outputs/run_name"
json_dir="$ ="/home/users/astar/gis/your_username/scratch/denovo_editors/ /denovo_editors/ProteinMPNN/outputs/run_name/"

# Define the output directory
output_dir="/home/users/astar/gis/diyasri/scratch/ProteinMPNN/outputs"

# Change to the ProteinMPNN directory
cd home/users/astar/gis/your_username/scratch/denovo_editors/ProteinMPNN

# Loop through each PDB file in the pdb_dir
for pdb_file in ${pdb_dir}/*.pdb; do
    # Extract the base name of the PDB file
    base_name=$(basename ${pdb_file} .pdb)

    # Construct the JSON file path
    json_file="${json_dir}/${base_name}_fixed_residues.json"

    # Check if the JSON file exists
    if [[ -f "${json_file}" ]]; then
        # Run the ProteinMPNN command
        python protein_mpnn_run.py \
            --pdb_path "${pdb_file}" \
            --fixed_positions_jsonl "${json_file}" \
            --out_folder "${output_dir}" \
            --num_seq_per_target 2 \
            --sampling_temp "0.1" \
            --seed 37 \
            --batch_size 1
    else
        echo "No matching JSON file found for ${pdb_file}"
    fi
done  # This 'done' statement closes the for loop

