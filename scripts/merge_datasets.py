import pandas as pd
from datetime import datetime

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

# --- 3. Enhanced Metadata Cleaning & Feature Engineering ---

print("Performing metadata cleaning and feature engineering...")

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
metadata_subset_df = metadata_df[metadata_columns_to_keep].copy()

# Date Engineering: Convert collection_date to datetime and extract features
def parse_date(date_str):
    if pd.isna(date_str):
        return pd.NaT
    try:
        # Handle various date formats
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%m/%d/%Y', '%Y']:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        # Try pandas automatic parsing
        return pd.to_datetime(date_str)
    except:
        return pd.NaT

metadata_subset_df['collection_date'] = metadata_subset_df['collection_date'].apply(parse_date)

# Extract date features
metadata_subset_df['collection_year'] = metadata_subset_df['collection_date'].dt.year
metadata_subset_df['collection_month'] = metadata_subset_df['collection_date'].dt.month

# Define seasons
def get_season(month):
    if pd.isna(month):
        return 'Unknown'
    elif month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

metadata_subset_df['collection_season'] = metadata_subset_df['collection_month'].apply(get_season)

# Categorical Standardization for host and isolation_source
def standardize_host(host):
    if pd.isna(host):
        return 'Unknown'
    host_lower = str(host).lower().strip()
    if any(term in host_lower for term in ['human', 'homo sapiens', 'patient', 'clinical']):
        return 'Human'
    elif any(term in host_lower for term in ['chicken', 'poultry', 'avian', 'bird']):
        return 'Avian'
    elif any(term in host_lower for term in ['pig', 'swine', 'porcine']):
        return 'Porcine'
    elif any(term in host_lower for term in ['cow', 'bovine', 'cattle']):
        return 'Bovine'
    elif any(term in host_lower for term in ['environment', 'water', 'soil', 'food']):
        return 'Environment'
    else:
        return 'Other'

def standardize_isolation_source(source):
    if pd.isna(source):
        return 'Unknown'
    source_lower = str(source).lower().strip()
    if any(term in source_lower for term in ['feces', 'stool', 'faecal', 'rectal']):
        return 'Fecal'
    elif any(term in source_lower for term in ['blood', 'serum']):
        return 'Blood'
    elif any(term in source_lower for term in ['urine']):
        return 'Urine'
    elif any(term in source_lower for term in ['food', 'meat', 'produce']):
        return 'Food'
    elif any(term in source_lower for term in ['water', 'environmental']):
        return 'Environmental'
    elif any(term in source_lower for term in ['clinical', 'hospital', 'patient']):
        return 'Clinical'
    else:
        return 'Other'

metadata_subset_df['host_standardized'] = metadata_subset_df['host'].apply(standardize_host)
metadata_subset_df['isolation_source_standardized'] = metadata_subset_df['isolation_source'].apply(standardize_isolation_source)

# --- 4. Perform the Merge ---
# We'll use a 'left' merge. This means we start with the amr_df (our primary data)
# and add information from the metadata_subset_df.
# If an Isolate_ID from the AMR data doesn't exist in the metadata, the new columns will be empty (NaN).
print("Merging AMR data with enhanced metadata...")
final_df = pd.merge(amr_df, metadata_subset_df, on='Isolate_ID', how='left')

# --- 5. Save the Final Enriched Dataset ---
output_filename = 'amr_dataset_final_enriched.csv'
print(f"Saving the final, enriched dataset to '{output_filename}'...")
final_df.to_csv(output_filename, index=False)

print("\nMerge complete!")
print("Final dataset shape:", final_df.shape)
print("Enhanced metadata columns added:")
print("- collection_year, collection_month, collection_season")
print("- host_standardized, isolation_source_standardized")
print("\nHere are the first 5 rows of your new master dataset:")
print(final_df.head())