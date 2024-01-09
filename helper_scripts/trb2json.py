import numpy as np
import re
import os
import json

# Directory containing PDB and TRB files
directory = '/home/users/astar/gis/your_username/scratch/RFdiffusion/outputs/run_1'
json_directory = os.path.join(directory, 'json_residues')

# Create json_residues directory if it doesn't exist
if not os.path.exists(json_directory):
    os.makedirs(json_directory)

# Function to process a single TRB file
def process_trb_file(trb_file):
    # Load the TRB file
    data = np.load(trb_file, allow_pickle=True)

    # Find the fixed residues
    fixed_residues = data.get('con_hal_idx0', [])

    # Adjust the indices (if needed)
    fixed_residues = [int(residue) + 1 for residue in fixed_residues]

    return fixed_residues

# Process all TRB files in the directory
for file in os.listdir(directory):
    if file.endswith('.trb'):
        trb_file_path = os.path.join(directory, file)
        fixed_residues = process_trb_file(trb_file_path)

        # Prepare JSON data
        json_data = {'A': fixed_residues}  # Assuming all residues are in chain 'A'

        # Create a JSON file for each set of fixed residues
        json_file_name = file.replace('.trb', '_fixed_residues.json')
        json_file_path = os.path.join(json_directory, json_file_name)

        # Write to JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

print("Finished processing TRB files and creating JSON files.")
