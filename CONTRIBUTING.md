# Contributing to AMR Genome Dataset

We welcome contributions to improve this antimicrobial resistance genome dataset! This document provides guidelines for contributors.

## How to Contribute

### 1. Reporting Issues
- Use GitHub Issues to report bugs or request features
- Provide detailed descriptions including steps to reproduce
- Include relevant dataset information and expected vs. actual behavior

### 2. Contributing Code
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes following our coding standards
4. Add tests if applicable
5. Commit with clear, descriptive messages
6. Push to your fork
7. Submit a Pull Request

### 3. Dataset Contributions
- New bacterial isolates with AMR annotations
- Additional metadata fields
- Improved data processing scripts
- Enhanced feature engineering

### 4. Documentation
- Improve README clarity
- Add usage examples
- Update API documentation
- Create tutorials or guides

## Code Standards

### Python Scripts
- Follow PEP 8 style guidelines
- Use descriptive variable names
- Add docstrings to functions
- Include error handling
- Comment complex logic

### Data Processing
- Validate data integrity
- Handle missing values appropriately
- Document data transformations
- Ensure reproducible results

## Dataset Standards

### AMR Annotations
- Use ABRicate tool output format
- Include complete gene coverage information
- Validate against known resistance databases
- Document annotation parameters

### Metadata Requirements
- Standardize collection dates (ISO format)
- Use controlled vocabularies for host/source
- Include BioProject/BioSample IDs when available
- Document data provenance

## Testing

### Data Validation
```python
# Run validation scripts
python scripts/dataset_check.py
python scripts/validate_data.py
```

### Code Testing
```python
# Run unit tests
python -m pytest tests/
```

## Data Privacy and Ethics

- Ensure all data is publicly available
- Respect data use agreements
- Anonymize sensitive information
- Document data sources and licenses

## Review Process

1. All PRs require review
2. Automated tests must pass
3. Data validation checks required
4. Documentation updates needed
5. Maintainers will provide feedback

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Acknowledged in dataset publications
- Credited in release notes

## Questions?

Contact the maintainers or open a GitHub Discussion for questions about contributing.