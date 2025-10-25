# AMR Genome Dataset: Antimicrobial Resistance Prediction Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://img.shields.io/badge/DOI-Coming%20Soon-blue)](https://doi.org/)

A comprehensive, machine-learning ready dataset for antimicrobial resistance (AMR) prediction in bacterial genomes. This dataset combines genomic sequences, AMR gene annotations, and rich metadata to enable advanced research in antibiotic resistance surveillance and prediction.

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset Description](#dataset-description)
- [Data Structure](#data-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Processing Pipeline](#data-processing-pipeline)
- [Research Applications](#research-applications)
- [Citation](#citation)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository provides a complete pipeline for processing bacterial genome data into a structured dataset suitable for machine learning applications in antimicrobial resistance research. The dataset includes 50 *Escherichia coli* isolates with comprehensive AMR annotations and metadata.

### Key Features

- **50 Bacterial Isolates**: Complete genome sequences with AMR annotations
- **79 AMR Features**: Binary-encoded presence/absence of resistance genes and phenotypes
- **Rich Metadata**: Epidemiological data, publication information, and quality metrics
- **ML-Ready Format**: One-hot encoded features for direct use in machine learning pipelines
- **Reproducible Pipeline**: Complete scripts for data processing and validation

## 📊 Dataset Description

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

## 🏗️ Data Structure

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

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/vihaankulkarni29/amr-dataset.git
cd amr-dataset

# Create virtual environment (recommended)
python -m venv amr_env
source amr_env/bin/activate  # On Windows: amr_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage

### Quick Start
```python
import pandas as pd

# Load the main dataset
df = pd.read_csv('data/processed/Kaggle_AMR_Dataset_v1.0_final.csv')

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

## 🔬 Data Processing Pipeline

### Raw Data → Processed Dataset

1. **Genome Assembly Data** (`data/raw/Genome Extractor Run/`)
   - FASTA files with complete genome sequences
   - NCBI accession numbers as identifiers

2. **AMR Annotations** (`data/raw/ABRicate Run/`)
   - ABRicate TSV output against CARD database
   - Gene presence/absence with coverage metrics

3. **Metadata Integration** (`data/raw/NCBI Metadata Run/`)
   - BioProject/BioSample information
   - Publication and author data
   - Assembly quality metrics

4. **Data Processing** (`scripts/`)
   - `process_amr_data.py`: Initial data extraction
   - `build_master_dataset.py`: Complete pipeline with feature engineering

5. **Final Dataset** (`data/processed/Kaggle_AMR_Dataset_v1.0_final.csv`)
   - ML-ready format with 112 features
   - Comprehensive metadata and engineered features

## 🔍 Research Applications

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

## 📚 Citation

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

## 📁 Repository Structure

```
amr-dataset/
├── data/
│   ├── raw/                    # Raw genomic and metadata files
│   │   ├── ABRicate Run/      # AMR gene annotations (gitignored)
│   │   ├── Genome Extractor Run/  # Genome FASTA files (gitignored)
│   │   └── NCBI Metadata Run/  # Publication metadata
│   └── processed/             # Processed datasets at different stages
│       ├── amr_summary_dataset.csv          # Raw processed (semicolon lists)
│       ├── amr_summary_cleaned.csv          # One-hot encoded (93 cols)
│       ├── amr_dataset_variable_features.csv # Curated subset (29 cols)
│       └── Kaggle_AMR_Dataset_v1.0_final.csv # Complete dataset (112 cols)
├── scripts/                   # Data processing pipeline
│   ├── process_amr_data.py    # Initial data extraction
│   ├── clean_amr_data.py      # One-hot encoding
│   ├── merge_datasets.py      # Metadata integration
│   ├── build_master_dataset.py # Complete pipeline
│   └── dataset_check.py       # Validation scripts
├── AMR_Dataset_Exploration.ipynb  # Comprehensive analysis notebook
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── requirements.txt
```

### Data Processing Pipeline

The multiple files in `data/processed/` represent **different stages of data processing**:

| File | Stage | Purpose | Features | Use Case |
|------|-------|---------|----------|----------|
| `amr_summary_dataset.csv` | Raw Processing | Initial extraction with semicolon-separated lists | 5 cols | Intermediate processing |
| `amr_summary_cleaned.csv` | Feature Encoding | One-hot encoded AMR genes and classes | 93 cols | Full AMR analysis |
| `amr_dataset_variable_features.csv` | Feature Selection | Curated subset removing housekeeping genes | 29 cols | Focused ML models |
| `Kaggle_AMR_Dataset_v1.0_final.csv` | **Final Dataset** | Complete with rich metadata and engineered features | **112 cols** | **Publication & research** |

**Which file should you use?**
- **For Kaggle/publication**: `Kaggle_AMR_Dataset_v1.0_final.csv` (complete dataset)
- **For ML modeling**: `amr_dataset_variable_features.csv` (focused features)
- **For full AMR analysis**: `amr_summary_cleaned.csv` (all AMR features)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Reporting bugs and requesting features
- Contributing code and data
- Dataset standards and validation
- Code style guidelines

### Ways to Contribute

- **Data**: Additional bacterial isolates with AMR annotations
- **Features**: Improved metadata fields or processing scripts
- **Analysis**: New research applications or tutorials
- **Documentation**: Improved guides or examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Vihaan Kulkarni**
- GitHub: [@vihaankulkarni29](https://github.com/vihaankulkarni29)
- Issues: [GitHub Issues](https://github.com/vihaankulkarni29/amr-dataset/issues)

## 🙏 Acknowledgments

- **Data Sources**: NCBI GenBank, BioProject, and BioSample databases
- **Tools**: ABRicate, BioPython, pandas
- **Research Community**: Contributors to antimicrobial resistance surveillance

---

**Note**: This dataset is for research purposes. Please ensure compliance with data use agreements and ethical guidelines when using genomic data.
