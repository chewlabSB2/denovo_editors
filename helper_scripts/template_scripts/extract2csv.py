import os
import csv
import re

# Relative path to the run directory
run_dir = '.'

# for example: if the run directory is 'run5' and all the names are 'run5', you need to edit the script accordingly

# CSV file name
csv_file_name = 'extracted_alphafold_values_run.csv'
csv_file_path = os.path.join(run_dir, csv_file_name)

# Header for the CSV file
headers = ['design number', 'sequence number', 'sequence', 'model rank', 
           'pdb_filename', 'pLDDT_score', 'pTM_score']

# Function to extract sequence from fasta file
def get_sequence(fasta_file):
    with open(fasta_file, 'r') as file:
        lines = file.readlines()
        return lines[1].strip()  # Assuming sequence is always on the second line

# Function to parse log.txt and extract model information
def parse_log(log_file):
    with open(log_file, 'r') as file:
        log_data = file.readlines()

    model_info = []
    for line in log_data:
        if 'rank' in line and 'alphafold2' in line and 'pLDDT' in line and 'pTM' in line:
            try:
                rank_match = re.search(r'rank_[\w_]+', line)
                plddt_match = re.search(r'pLDDT=\d+\.\d+', line)
                ptm_match = re.search(r'pTM=\d+\.\d+', line)

                if rank_match and plddt_match and ptm_match:
                    rank = rank_match.group()
                    plddt = plddt_match.group().split('=')[1]
                    ptm = ptm_match.group().split('=')[1]
                    model_info.append((rank, plddt, ptm))
            except Exception as e:
                print(f"Error parsing line in {log_file}: {line}")
                print(e)
                continue
    
    return model_info

# Function to create the CSV file
def create_csv():
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

        # Iterate over designs and sequences
        for design_num in range(20):
            for seq_num in ['seq1', 'seq2']:
                fasta_file = os.path.join(run5_dir, f'mpnn_seq_for_AF2/run_{design_num}_{seq_num}.fasta')
                if os.path.exists(fasta_file):
                    sequence = get_sequence(fasta_file)

                    # Iterate over models
                    for model_rank in range(1, 6):
                        sub_dir = f'run_{design_num}_{seq_num}'
                        sub_dir_path = os.path.join(run7_dir, sub_dir)
                        log_file = os.path.join(sub_dir_path, 'log.txt')

                        if os.path.exists(log_file):
                            models_info = parse_log(log_file)
                            for model in models_info:
                                rank, plddt, ptm = model
                                if rank.endswith(f'_{model_rank}'):
                                    pdb_filename = f'{sub_dir}_relaxed_{rank}.pdb'
                                    writer.writerow([design_num, seq_num, sequence, model_rank, 
                                                     pdb_filename, plddt, ptm])
                                    print(f'Writing data for design {design_num}, {seq_num}, model {model_rank}')
                        else:
                            print(f"Error: Log file not found in {sub_dir_path}")
                            return
                else:
                    print(f"Error: Fasta file not found for design {design_num}, {seq_num}")
                    return
    print(f"CSV file created successfully at {csv_file_path}")

# Run the function to create the CSV file
create_csv()
