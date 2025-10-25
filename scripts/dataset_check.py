import pandas as pd

# Set pandas to display all columns (not truncate them with '...')
pd.set_option('display.max_columns', None)

print("Loading 'amr_summary_cleaned.csv'...")
try:
    # Load the cleaned dataset
    df = pd.read_csv('amr_summary_cleaned.csv')

    # --- 1. Check the "Shape" ---
    # This will show you (rows, columns). The second number is what we care about.
    print(f"\n--- 1. Dataset Dimensions (Rows, Columns) ---")
    print(df.shape)

    # --- 2. Print All Column Names ---
    # This will print the full list of all columns in your file.
    print(f"\n--- 2. All {len(df.columns)} Column Names ---")
    print(list(df.columns))

    # --- 3. Verify Your Example Isolate ---
    # Let's check the isolate you provided (AP039418.1)
    # and look for genes we know should be there from the .tsv file.

    isolate_to_check = 'AP039418.1'
    genes_to_check = ['gadW', 'gadX', 'mdtF', 'mdtE', 'CMY-59']

    print(f"\n--- 3. Verifying genes for isolate {isolate_to_check} ---")

    # Set the Isolate_ID as the index for easy lookup
    df_indexed = df.set_index('Isolate_ID')

    # Select the row for our isolate and the columns for our genes
    verification_data = df_indexed.loc[isolate_to_check, genes_to_check]

    print(verification_data)

except FileNotFoundError:
    print("Error: 'amr_summary_cleaned.csv' not found. Make sure it's in the same directory.")
except KeyError as e:
    print(f"\nError checking isolate: {e}")
    print("This might mean the Isolate_ID or a gene name is not in the file.")