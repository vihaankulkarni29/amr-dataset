import pandas as pd

# --- 1. Load Your Datasets ---
print("Loading datasets...")
try:
    # Load the AMR data you've already cleaned
    amr_df = pd.read_csv('amr_summary_cleaned.csv')

    # Load the rich metadata you just generated
    metadata_df = pd.read_csv('all_filtered_harmonized_metadata.csv')
except FileNotFoundError as e:
    print(f"Error: Make sure '{e.filename}' is in the same directory as the script.")
    exit()

# --- 2. Prepare for the Merge ---

# The column names for the isolate ID might be different. Let's standardize them.
# In amr_summary_cleaned.csv it's 'Isolate_ID'.
# In all_filtered_harmonized_metadata.csv it's 'accession'.
# Let's rename the metadata column to match.
metadata_df.rename(columns={'accession': 'Isolate_ID'}, inplace=True)


# Select the most useful metadata columns to add. We don't need everything,
# just the fields that provide the most context.
metadata_columns_to_keep = [
    'Isolate_ID',
    'organism',
    'strain',
    'collection_date',
    'country',
    'host',
    'isolation_source',
    'bioproject',
    'biosample'
]
metadata_subset_df = metadata_df[metadata_columns_to_keep]


# --- 3. Perform the Merge ---
# We'll use a 'left' merge. This means we start with the amr_df (our primary data)
# and add information from the metadata_subset_df.
# If an Isolate_ID from the AMR data doesn't exist in the metadata, the new columns will be empty (NaN).
print("Merging AMR data with metadata...")
final_df = pd.merge(amr_df, metadata_subset_df, on='Isolate_ID', how='left')


# --- 4. Save the Final Enriched Dataset ---
output_filename = 'amr_dataset_final_enriched.csv'
print(f"Saving the final, enriched dataset to '{output_filename}'...")
final_df.to_csv(output_filename, index=False)

print("\nMerge complete!")
print("Final dataset shape:", final_df.shape)
print("Here are the first 5 rows of your new master dataset:")
print(final_df.head())