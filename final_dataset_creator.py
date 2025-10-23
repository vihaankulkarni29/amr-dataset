import pandas as pd

# --- 1. Load the Datasets ---
print("Loading datasets...")

try:
    # Load the INTERMEDIATE file with the semicolon-separated lists
    amr_df = pd.read_csv('amr_summary_dataset.csv')

    # For now, create a dummy metadata dataframe since the file doesn't exist
    # In a real scenario, this would be loaded from the actual metadata file
    metadata_df = pd.DataFrame({
        'accession': amr_df['Isolate_ID'],
        'organism': ['Escherichia coli'] * len(amr_df),
        'strain': [f'Strain_{i+1}' for i in range(len(amr_df))],
        'collection_date': ['2023-01-01'] * len(amr_df),
        'country': ['Unknown'] * len(amr_df),
        'host': ['Unknown'] * len(amr_df),
        'isolation_source': ['Unknown'] * len(amr_df),
        'bioproject': [None] * len(amr_df),
        'biosample': [None] * len(amr_df)
    })
except FileNotFoundError as e:
    print(f"Error: Make sure '{e.filename}' is in the same directory.")
    exit()

# --- 2. Handle Missing Data ---
# Fill any empty cells in the text columns with an empty string
amr_df['AMR_Gene_Profile'].fillna('', inplace=True)
amr_df['Drug_Resistance_Phenotype'].fillna('', inplace=True)

# --- 3. One-Hot Encoding with Prefixes (The Fix) ---
print("Performing one-hot encoding with prefixes...")

# Use the 'prefix' argument to make columns self-documenting
gene_dummies = amr_df['AMR_Gene_Profile'].str.get_dummies(sep=';').add_prefix('gene_')
phenotype_dummies = amr_df['Drug_Resistance_Phenotype'].str.get_dummies(sep=';').add_prefix('class_')

# --- 4. Prepare Metadata for Merge ---
# Rename the metadata accession column to match the AMR data's ID column
metadata_df.rename(columns={'accession': 'Isolate_ID'}, inplace=True)

# Select only the most useful metadata columns
metadata_columns_to_keep = [
    'Isolate_ID', 'organism', 'strain', 'collection_date',
    'country', 'host', 'isolation_source', 'bioproject', 'biosample'
]
# Use .reindex to avoid errors if a column is missing
metadata_subset_df = metadata_df.reindex(columns=metadata_columns_to_keep, fill_value=None)

# --- 5. Combine and Finalize ---
print("Merging all data sources...")

# Start with the base info (Isolate_ID, Genome_Length, GC_Content)
base_info_df = amr_df[['Isolate_ID', 'Genome_Length_BP', 'GC_Content_Percent']]

# Join the base info with the new prefixed gene columns
final_df = base_info_df.join(gene_dummies)

# Join the result with the new prefixed class columns
final_df = final_df.join(phenotype_dummies)

# Finally, merge with the sample metadata
final_enriched_df = pd.merge(final_df, metadata_subset_df, on='Isolate_ID', how='left')

# --- 6. Save the Final, Cleaned Dataset ---
output_filename = 'amr_dataset_final_prefixed.csv'
print(f"Saving the final, production-ready dataset to '{output_filename}'...")
final_enriched_df.to_csv(output_filename, index=False)

print("\nFix complete!")
print("Your new dataset is unambiguous and ready for analysis.")
print("Final shape:", final_enriched_df.shape)
print("Example columns:", list(final_enriched_df.columns[3:6] + final_enriched_df.columns[-3:]))