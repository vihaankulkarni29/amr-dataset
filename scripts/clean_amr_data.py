import pandas as pd

# Load the dataset
df = pd.read_csv('amr_summary_dataset.csv')

# Fill missing values in AMR columns with empty strings
df['AMR_Gene_Profile'] = df['AMR_Gene_Profile'].fillna('')
df['Drug_Resistance_Phenotype'] = df['Drug_Resistance_Phenotype'].fillna('')

# One-hot encode AMR_Gene_Profile
genes_dummies = df['AMR_Gene_Profile'].str.get_dummies(sep=';')

# One-hot encode Drug_Resistance_Phenotype
phenotypes_dummies = df['Drug_Resistance_Phenotype'].str.get_dummies(sep=';')

# Concatenate the dummies with the original DataFrame
df_cleaned = pd.concat([df, genes_dummies, phenotypes_dummies], axis=1)

# Drop the original AMR columns
df_cleaned = df_cleaned.drop(columns=['AMR_Gene_Profile', 'Drug_Resistance_Phenotype'])

# Save the cleaned dataset
df_cleaned.to_csv('amr_summary_cleaned.csv', index=False)

# Print confirmation and dimensions
print(f"Cleaned dataset saved to amr_summary_cleaned.csv")
print(f"Dataset dimensions: {df_cleaned.shape[0]} rows, {df_cleaned.shape[1]} columns")