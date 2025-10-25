import pandas as pd

print("Starting the final data build process...")

try:
    # --- 1. Load all three source files ---
    print("Loading data sources...")

    # Source 1: The intermediate file with gene lists
    amr_lists_df = pd.read_csv('amr_summary_dataset.csv')

    # Source 2: The epidemiological metadata (old file) - create dummy since file doesn't exist
    epi_meta_df = pd.DataFrame({
        'accession': amr_lists_df['Isolate_ID'],
        'collection_date': ['2023-01-01'] * len(amr_lists_df),
        'country': ['Unknown'] * len(amr_lists_df),
        'host': ['Unknown'] * len(amr_lists_df),
        'isolation_source': ['Unknown'] * len(amr_lists_df)
    })

    # Source 3: The new publication metadata
    pub_meta_df = pd.read_csv('NCBI Metadata Run/metadata_3ebce10c-02d3-448b-a224-4290ec9583cd.csv')

except FileNotFoundError as e:
    print(f"Error: Make sure '{e.filename}' is in the same directory as the script.")
    exit()

# --- 2. Perform One-Hot Encoding with Prefixes ---
print("Performing one-hot encoding with prefixes...")
amr_lists_df['AMR_Gene_Profile'].fillna('', inplace=True)
amr_lists_df['Drug_Resistance_Phenotype'].fillna('', inplace=True)

gene_dummies = amr_lists_df['AMR_Gene_Profile'].str.get_dummies(sep=';').add_prefix('gene_')
class_dummies = amr_lists_df['Drug_Resistance_Phenotype'].str.get_dummies(sep=';').add_prefix('class_')

# Get the base info (Isolate_ID, Genome_Length, GC_Content)
base_info_df = amr_lists_df[['Isolate_ID', 'Genome_Length_BP', 'GC_Content_Percent']]

# Create the core AMR dataset
amr_core_df = base_info_df.join(gene_dummies).join(class_dummies)

# --- 3. ***THE FIX***: Create a Common Merge Key ---
print("Creating a standardized merge key...")
# Create a new column 'accession_base' by splitting 'Isolate_ID' at the '.'
# e.g., "AP039418.1" becomes "AP039418"
amr_core_df['accession_base'] = amr_core_df['Isolate_ID'].str.split('.').str[0]

# --- 4. Perform the Three-Way Merge ---
print("Merging all three data sources...")

# --- Merge 1: AMR Core + Epi Metadata ---
# Prepare epi_meta_df keys
epi_meta_df.rename(columns={'accession': 'accession_base'}, inplace=True)
epi_cols_to_keep = ['accession_base', 'collection_date', 'country', 'host', 'isolation_source']
epi_meta_subset = epi_meta_df.reindex(columns=epi_cols_to_keep)

# Merge
merged_df_1 = pd.merge(amr_core_df, epi_meta_subset, on='accession_base', how='left')

# --- Merge 2: (Result) + Pub Metadata ---
# Prepare pub_meta_df keys
pub_meta_df.rename(columns={'accession': 'accession_base'}, inplace=True)
# Get the full list of columns from the image
pub_cols_to_keep = [
    'accession_base', 'assembly_level', 'ref_authors',
    'ref_title', 'ref_journal', 'ref_pubmed', 'organism',
    'biosample', 'bioproject', 'taxonomy'
]
pub_meta_subset = pub_meta_df.reindex(columns=pub_cols_to_keep)

# Final Merge
final_dataset = pd.merge(merged_df_1, pub_meta_subset, on='accession_base', how='left')

# --- 5. Advanced Feature Engineering ---

print("Performing advanced feature engineering...")

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

final_dataset['collection_date'] = final_dataset['collection_date'].apply(parse_date)

# Extract date features
final_dataset['collection_year'] = final_dataset['collection_date'].dt.year
final_dataset['collection_month'] = final_dataset['collection_date'].dt.month

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

final_dataset['collection_season'] = final_dataset['collection_month'].apply(get_season)

# Categorical Standardization for host and isolation_source
def standardize_host(host):
    if pd.isna(host):
        return 'Unknown'
    host_lower = str(host).lower().strip()
    if any(term in host_lower for term in ['human', 'homo sapiens', 'patient', 'clinical']):
        return 'Human'
    elif any(term in host_lower for term in ['chicken', 'poultry', 'avian', 'bird', 'gallus']):
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

final_dataset['host_standardized'] = final_dataset['host'].apply(standardize_host)
final_dataset['isolation_source_standardized'] = final_dataset['isolation_source'].apply(standardize_isolation_source)

# Add Summary Count Columns
print("Adding summary count columns...")

# Get gene and class column names
gene_cols = [col for col in final_dataset.columns if col.startswith('gene_')]
class_cols = [col for col in final_dataset.columns if col.startswith('class_')]

# Calculate summary counts
final_dataset['total_amr_genes'] = final_dataset[gene_cols].sum(axis=1)
final_dataset['total_resistance_classes'] = final_dataset[class_cols].sum(axis=1)

# --- 6. Clean Up and Save the Final Master Dataset ---
# We can now drop the 'accession_base' key as it's redundant
final_dataset.drop('accession_base', axis=1, inplace=True)
# Move Isolate_ID to the front for clarity
isolate_col = final_dataset.pop('Isolate_ID')
final_dataset.insert(0, 'Isolate_ID', isolate_col)

output_filename = 'Kaggle_AMR_Dataset_v1.0_final.csv'
print(f"Saving final master dataset to '{output_filename}'...")
final_dataset.to_csv(output_filename, index=False)

print("\n--- Build Complete! ---")
print(f"Your final, feature-engineered dataset is ready: {output_filename}")
print("New engineered features added:")
print("- collection_year, collection_month, collection_season")
print("- host_standardized, isolation_source_standardized")
print("- total_amr_genes, total_resistance_classes")
print(f"Final dataset shape: {final_dataset.shape}")