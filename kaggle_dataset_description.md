# Antimicrobial Resistance (AMR) Genome Dataset

## Dataset Description

A comprehensive, machine-learning ready dataset for antimicrobial resistance (AMR) prediction in bacterial genomes. This dataset combines genomic sequences, AMR gene annotations, and rich metadata to enable advanced research in antibiotic resistance surveillance and prediction.

## Overview

This repository provides a complete pipeline for processing bacterial genome data into a structured dataset suitable for machine learning applications in antimicrobial resistance research. The dataset includes 50 *Escherichia coli* isolates with comprehensive AMR annotations and metadata.

### Key Features

- **50 Bacterial Isolates**: Complete genome sequences with AMR annotations
- **79 AMR Features**: Binary-encoded presence/absence of resistance genes and phenotypes
- **Rich Metadata**: Epidemiological data, publication information, and quality metrics
- **ML-Ready Format**: One-hot encoded features for direct use in machine learning pipelines
- **Reproducible Pipeline**: Complete scripts for data processing and validation

## Dataset Content

### Primary Dataset: `Kaggle_AMR_Dataset_v1.0_final.csv`

**Dimensions**: 50 isolates × 112 features

**Data Sources**:
- **Genomic Data**: Complete bacterial genome assemblies from NCBI
- **AMR Annotations**: ABRicate tool results against CARD database
- **Metadata**: NCBI BioProject/BioSample information and publication data

### Isolate Characteristics

- **Species**: Primarily *Escherichia coli* with some other Enterobacteriaceae
- **Genome Size**: 4.7-5.5 Mbp
- **GC Content**: 50-51%
- **AMR Genes**: 43-51 genes per isolate
- **Resistance Classes**: 21-25 antibiotic classes per isolate

## Data Structure

### Core Features (3 columns)
- `Isolate_ID`: NCBI accession number (e.g., AP039418.1)
- `Genome_Length_BP`: Total genome length in base pairs
- `GC_Content_Percent`: GC content percentage

### AMR Gene Features (42 columns)
Binary features prefixed with `gene_`:
- `gene_CTX-M-15`: Extended-spectrum beta-lactamase
- `gene_acrB`: Multidrug efflux pump component
- `gene_tet(A)`: Tetracycline resistance gene
- *...and 39 additional genes*

### Resistance Phenotype Features (37 columns)
Binary features prefixed with `class_`:
- `class_carbapenem`: Resistance to carbapenem antibiotics
- `class_fluoroquinolone`: Resistance to fluoroquinolones
- `class_tetracycline`: Resistance to tetracyclines
- *...and 34 additional antibiotic classes*

### Metadata Features (14 columns)
- **Epidemiological**: `collection_date`, `country`, `host`, `isolation_source`
- **Engineered**: `collection_year`, `collection_month`, `collection_season`
- **Standardized**: `host_standardized`, `isolation_source_standardized`
- **Publication**: `ref_authors`, `ref_title`, `ref_journal`, `ref_pubmed`
- **Quality**: `assembly_level`, `biosample`, `bioproject`, `taxonomy`

### Summary Features (2 columns)
- `total_amr_genes`: Count of AMR genes present (43-51)
- `total_resistance_classes`: Count of resistance classes (21-25)

## Usage Examples

### Quick Start
```python
import pandas as pd

# Load the main dataset
df = pd.read_csv('Kaggle_AMR_Dataset_v1.0_final.csv')

# Basic exploration
print(f"Dataset shape: {df.shape}")
print(f"AMR genes detected: {df['total_amr_genes'].sum()}")
print(f"Unique resistance classes: {df.filter(like='class_').shape[1]}")
```

### Machine Learning Example
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Prepare features and target
feature_cols = [col for col in df.columns if col.startswith(('gene_', 'class_'))]
target_col = 'total_resistance_classes'  # Or specific resistance class

X = df[feature_cols]
y = (df[target_col] > df[target_col].median()).astype(int)  # Binary classification

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
```

## Data Processing Pipeline

### Raw Data → Processed Dataset

1. **Genome Assembly Data**: FASTA files with complete genome sequences and NCBI accession numbers as identifiers

2. **AMR Annotations**: ABRicate TSV output against CARD database with gene presence/absence and coverage metrics

3. **Metadata Integration**: BioProject/BioSample information, publication and author data, assembly quality metrics

4. **Data Processing**: Custom Python pipeline with feature engineering and one-hot encoding

5. **Final Dataset**: ML-ready format with 112 features and comprehensive metadata

## Research Applications

### Antimicrobial Resistance Surveillance
- Track emergence of resistance genes over time
- Identify multidrug-resistant isolates
- Monitor resistance patterns by geographic region

### Machine Learning Research
- Binary classification of resistance phenotypes
- Multi-label classification of resistance genes
- Feature importance analysis for resistance mechanisms
- Predictive modeling of resistance acquisition

### Epidemiological Studies
- Temporal trends in resistance emergence
- Host-specific resistance patterns
- Geographic distribution of resistance genes

### Comparative Genomics
- Identify core vs. accessory resistome
- Study co-occurrence of resistance genes
- Analyze plasmid-mediated resistance

## Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{kulkarni_amr_dataset_2024,
  title={AMR Genome Dataset: Antimicrobial Resistance Prediction Dataset},
  author={Kulkarni, Vihaan},
  year={2024},
  publisher={GitHub},
  url={https://github.com/vihaankulkarni29/amr-dataset}
}
```

## Files Included

- `Kaggle_AMR_Dataset_v1.0_final.csv`: Main dataset file (50×112)
- `AMR_Dataset_Exploration.ipynb`: Comprehensive analysis notebook
- `README.md`: Detailed documentation
- `requirements.txt`: Python dependencies

## License

This dataset is licensed under the MIT License.

## Contact

For questions about this dataset, please open an issue on the GitHub repository.