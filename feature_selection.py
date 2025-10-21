import pandas as pd

# Load the cleaned dataset (since enriched doesn't exist yet)
print("Loading cleaned dataset...")
df = pd.read_csv('amr_summary_cleaned.csv')

# Identify gene and phenotype columns (binary features)
# Gene columns are those that start with gene names (contain parentheses or are gene symbols)
# Phenotype columns are the resistance class names (no parentheses, lowercase)

# Get all columns except the basic metadata columns (since enriched dataset doesn't exist yet)
metadata_cols = ['Isolate_ID', 'Genome_Length_BP', 'GC_Content_Percent']

feature_cols = [col for col in df.columns if col not in metadata_cols]

print(f"Total features: {len(feature_cols)}")

# Calculate frequency of each feature
feature_frequencies = {}
for col in feature_cols:
    freq = df[col].sum() / len(df) * 100  # Percentage
    feature_frequencies[col] = freq

# Print frequency distribution
print("\nFeature frequency distribution:")
freq_counts = {'Very Common (>95%)': 0, 'Common (50-95%)': 0, 'Variable (5-50%)': 0, 'Rare (1-5%)': 0, 'Very Rare (<1%)': 0}
for col, freq in feature_frequencies.items():
    if freq > 95:
        freq_counts['Very Common (>95%)'] += 1
    elif freq > 50:
        freq_counts['Common (50-95%)'] += 1
    elif freq > 5:
        freq_counts['Variable (5-50%)'] += 1
    elif freq > 1:
        freq_counts['Rare (1-5%)'] += 1
    else:
        freq_counts['Very Rare (<1%)'] += 1

for category, count in freq_counts.items():
    print(f"{category}: {count} features")

# Select variable features (1% to 95% frequency)
# This removes "housekeeping" genes that are always present and extremely rare genes
variable_features = [col for col, freq in feature_frequencies.items() if 1 <= freq <= 95]

print(f"\nSelected {len(variable_features)} variable features (1-95% frequency)")

# Create the variable features dataset
variable_cols = metadata_cols + variable_features
df_variable = df[variable_cols]

# Save the variable features dataset
output_filename = 'amr_dataset_variable_features.csv'
df_variable.to_csv(output_filename, index=False)

print(f"Saved variable features dataset to {output_filename}")
print(f"Dataset shape: {df_variable.shape}")

# Print some statistics about removed features
removed_features = len(feature_cols) - len(variable_features)
print(f"Removed {removed_features} features that were too common (>95%) or too rare (<1%)")

# Show examples of removed features
very_common = [col for col, freq in feature_frequencies.items() if freq > 95]
very_rare = [col for col, freq in feature_frequencies.items() if freq < 1]

print(f"\nExamples of very common features removed (>95%): {very_common[:5]}")
print(f"Examples of very rare features removed (<1%): {very_rare[:5]}")