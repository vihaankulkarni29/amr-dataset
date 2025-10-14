# AMR Genome Dataset Processor

This repository contains Python scripts to process bacterial genome files and their corresponding antimicrobial resistance (AMR) annotation files to generate a consolidated dataset suitable for machine learning and data analysis on Kaggle.

## Overview

The project processes:
- FASTA files containing bacterial genome sequences
- TSV files with AMR gene annotations from ABRicate
- Outputs a cleaned CSV with genome metrics and one-hot encoded AMR features

## Features

- **Genome Analysis**: Calculates total genome length and GC content using BioPython
- **AMR Processing**: Extracts and processes AMR genes and resistance phenotypes
- **Data Cleaning**: One-hot encodes categorical AMR data for ML readiness
- **Error Handling**: Manages missing files and empty datasets gracefully

## Files

- `process_amr_data.py`: Main script to process raw data into initial CSV
- `clean_amr_data.py`: Script to one-hot encode AMR features
- `merge_datasets.py`: Script to merge AMR data with metadata
- `amr_summary_dataset.csv`: Intermediate dataset with semicolon-separated AMR data
- `amr_summary_cleaned.csv`: Cleaned dataset with binary AMR features
- `amr_dataset_final_enriched.csv`: Final enriched dataset with metadata (44 rows, 133 columns)
- `requirements.txt`: Python dependencies
- `ABRicate Run/`: Directory containing AMR annotation TSV files (ignored by git)
- `Genome Extractor Run/`: Directory containing genome FASTA files (ignored by git)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Process Raw Data**:
   ```bash
   python process_amr_data.py
   ```
   This generates `amr_summary_dataset.csv` with genome metrics and AMR profiles.

2. **Clean and Encode Data**:
   ```bash
   python clean_amr_data.py
   ```
   This generates `amr_summary_cleaned.csv` with one-hot encoded features.

3. **Merge with Metadata** (Optional):
   ```bash
   python merge_datasets.py
   ```
   This generates `amr_dataset_final_enriched.csv` with additional metadata columns.

## Data Description

### Input Data
- **Genome Files**: FASTA format with NCBI accession numbers as filenames
- **AMR Files**: TSV format from ABRicate tool with GENE and RESISTANCE columns

### Output Data
- **Isolate_ID**: Unique accession number
- **Genome_Length_BP**: Total base pairs in genome
- **GC_Content_Percent**: GC content percentage (rounded to 2 decimals)
- **Gene Columns**: Binary columns for each unique AMR gene (1=present, 0=absent)
- **Phenotype Columns**: Binary columns for each unique resistance phenotype

### Final Enriched Dataset
The `amr_dataset_final_enriched.csv` includes additional metadata columns:
- **organism**: Bacterial species
- **strain**: Specific strain information
- **collection_date**: Date sample was collected
- **country**: Country of origin
- **host**: Host organism (if applicable)
- **isolation_source**: Source of isolation
- **bioproject**: NCBI BioProject ID
- **biosample**: NCBI BioSample ID

## Dependencies

- pandas: Data manipulation and CSV handling
- biopython: FASTA file parsing and sequence analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Contact

For questions or issues, please open a GitHub issue.