import pandas as pd
import numpy as np
from Bio import PDB

def process_pdb_file(pdb_file):
    parser = PDB.PDBParser()
    structure = parser.get_structure("protein", pdb_file)
    atom_details = []
    for model in structure:
        for chain in model:
            for residue in chain:
                if residue.id[0] == ' ':  # Exclude heteroatoms
                    atom_details.append([residue.get_resname(), residue.id[1]])
    df = pd.DataFrame(atom_details, columns=['resid', 'resno'])
    return df.drop_duplicates()

def format_consecutive_ranges(numbers):
    if not numbers:
        return ""
    ranges = []
    start = end = numbers[0]
    for number in numbers[1:]:
        if number == end + 1:
            end = number
        else:
            ranges.append(f"{start}-{end}" if start != end else str(start))
            start = end = number
    ranges.append(f"{start}-{end}" if start != end else str(start))
    return ", ".join(ranges)

def split_ranges_to_dataframe(formatted_ranges):
    ranges = formatted_ranges.split(", ")
    df_ranges = pd.DataFrame([r.split("-") for r in ranges], columns=["start", "end"])
    df_ranges['end'] = df_ranges['end'].fillna(df_ranges['start'])
    df_ranges = df_ranges.astype({'start': 'int', 'end': 'int'})
    return df_ranges

def calculate_and_modify_gaps(df_ranges):
    df_ranges['gap'] = df_ranges['start'].diff().fillna(0) - 1
    df_ranges.loc[df_ranges.index[0], 'gap'] = np.nan
    df_ranges['mod_gap'] = df_ranges['gap'].apply(lambda x: f"{int(x-5)}-{int(x+5)}" if x > 5 else x)
    return df_ranges

def add_additional_columns(df_ranges):
    df_ranges['mod_gap_min'] = df_ranges['mod_gap'].apply(lambda x: int(str(x).split("-")[0]) if "-" in str(x) else x)
    df_ranges['mod_gap_max'] = df_ranges['mod_gap'].apply(lambda x: int(str(x).split("-")[1]) if "-" in str(x) else x)
    df_ranges['orig_len'] = df_ranges.apply(lambda row: row['end'] - row['start'] + 1, axis=1)
    df_ranges['format'] = df_ranges.apply(lambda row: f"D{row['start']}-{row['end']}" if row['start'] != row['end'] else f"D{row['start']}", axis=1)
    return df_ranges

def create_final_output_string(df_ranges):
    def format_value(x):
        if isinstance(x, float) and pd.notna(x):
            return str(int(x)) if x.is_integer() else str(x)
        elif isinstance(x, str) and '-' in x:
            parts = x.split('-')
            formatted_parts = [str(int(part)) if part.replace('.', '', 1).isdigit() else part for part in parts]
            return '-'.join(formatted_parts)
        else:
            return str(x)

    interleaved = df_ranges.apply(lambda row: f"{format_value(row['mod_gap'])}/{row['format']}", axis=1).tolist()
    final_string = "/".join(interleaved).replace('nan/', '')
    return final_string

if __name__ == "__main__":
    pdb_file = '/path/to/your/pdb/file.pdb'  # Replace with the actual path
    df = process_pdb_file(pdb_file)
    formatted_ranges = format_consecutive_ranges(list(df['resno']))
    df_ranges = split_ranges_to_dataframe(formatted_ranges)
    df_ranges = calculate_and_modify_gaps(df_ranges)
    df_ranges = add_additional_columns(df_ranges)
    final_string = create_final_output_string(df_ranges)

    print(final_string)
    print('Sum of mod_gap_min and orig_len:', sum(df_ranges['mod_gap_min'].fillna(0) + df_ranges['orig_len']))
    print('Sum of mod_gap_max and orig_len:', sum(df_ranges['mod_gap_max'].fillna(0) + df_ranges['orig_len']))
    print('Sum of gap and orig_len:', sum(df_ranges['gap'].fillna(0) + df_ranges['orig_len']))
