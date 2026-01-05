# Processed Data

This directory contains cleaned and transformed datasets ready for analysis and visualization.

## Purpose

Store data that has been:
- Cleaned (missing values handled, outliers addressed)
- Transformed (calculated variables, aggregations)
- Merged (combined from multiple sources)
- Filtered (subsetted for specific analyses)
- Reformatted (changed data types, reshaped)

## Guidelines

1. **Naming Convention:**
   - Use descriptive names: `survey_cleaned.csv`, `sales_monthly_aggregated.csv`
   - Include processing level or date if helpful: `data_cleaned_v2.csv`
   - Be consistent with naming patterns

2. **Documentation:**
   - Document all transformations in your analysis scripts
   - Include comments explaining major processing steps
   - Create data dictionaries for processed datasets
   - Note any filtering or subsetting applied

3. **Reproducibility:**
   - All processed data should be reproducible from raw data + scripts
   - Never manually edit data files - use scripts instead
   - Keep track of data lineage (which raw files created which processed files)

4. **Version Control:**
   - Small files (< 10 MB) can be committed to git
   - Larger files should be regenerated from scripts or stored externally
   - Use `.gitignore` for large processed files

## Example Processing Workflow

```python
# In scripts/01_clean_data.py

# Read raw data
raw_data = pd.read_csv('data/raw/survey_data.csv')

# Clean and process
clean_data = (raw_data
    .dropna(subset=['important_var'])
    .query('age >= 18')
    .assign(new_var=lambda df: df['var1'] + df['var2'])
)

# Save to processed
clean_data.to_csv('data/processed/survey_cleaned.csv', index=False)
```

## Data Dictionary Template

For each processed dataset, consider creating a data dictionary:

```markdown
# Dataset: survey_cleaned.csv

## Source
- Raw data: data/raw/survey_data.csv
- Processing script: scripts/01_clean_data.py
- Date created: 2026-01-05

## Transformations Applied
1. Removed rows with missing 'important_var'
2. Filtered to participants age 18+
3. Created 'new_var' as sum of 'var1' and 'var2'

## Variables
| Variable | Type | Description | Range | Missing |
|----------|------|-------------|-------|---------|
| id | int | Participant ID | 1-500 | None |
| age | int | Age in years | 18-89 | None |
| new_var | float | Sum of var1 and var2 | 0-100 | Coded as -999 |
```
