import os
import pandas as pd
from Bio import SeqIO

# Define directories
input_dir = "Genome Extractor Run"
results_dir = "ABRicate Run"
output_file = "amr_summary_dataset.csv"

# List to collect data
data = []

# Iterate through .tsv files in results directory
for tsv_file in os.listdir(results_dir):
    if not tsv_file.endswith('.tsv'):
        continue

    # Extract Isolate_ID from filename
    isolate_id = tsv_file[:-4]  # Remove .tsv extension

    # Read .tsv file into DataFrame
    tsv_path = os.path.join(results_dir, tsv_file)
    try:
        df = pd.read_csv(tsv_path, sep='\t', comment='#', names=['FILE', 'SEQUENCE', 'START', 'END', 'STRAND', 'GENE', 'COVERAGE', 'COVERAGE_MAP', 'GAPS', '%COVERAGE', '%IDENTITY', 'DATABASE', 'ACCESSION', 'PRODUCT', 'RESISTANCE'])
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()

    # Process AMR genes and resistances
    if df.empty:
        genes = ''
        resistances = ''
    else:
        # Unique genes, sorted, semicolon-separated
        genes = ';'.join(sorted(df['GENE'].dropna().unique()))
        # Unique resistances, split on ';', flatten, unique, sorted, semicolon-separated
        res_list = df['RESISTANCE'].dropna().str.split(';').explode().unique()
        resistances = ';'.join(sorted(res_list))

    # Process corresponding .fasta file
    fasta_file = os.path.join(input_dir, isolate_id + '.fasta')
    if os.path.exists(fasta_file):
        total_len = 0
        gc_count = 0
        for record in SeqIO.parse(fasta_file, 'fasta'):
            seq = str(record.seq).upper()
            total_len += len(seq)
            gc_count += seq.count('G') + seq.count('C')
        gc_percent = round((gc_count / total_len) * 100, 2) if total_len > 0 else 0.0
    else:
        print(f"Warning: FASTA file for {isolate_id} not found.")
        total_len = None
        gc_percent = None

    # Collect data
    data.append({
        'Isolate_ID': isolate_id,
        'Genome_Length_BP': total_len,
        'GC_Content_Percent': gc_percent,
        'AMR_Gene_Profile': genes,
        'Drug_Resistance_Phenotype': resistances
    })

# Create final DataFrame and save to CSV
df_final = pd.DataFrame(data)
df_final.to_csv(output_file, index=False)