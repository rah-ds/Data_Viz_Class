# Data Directory

This directory contains all data files used in the project.

## Structure

- `raw/` - Original, immutable data files
- `processed/` - Cleaned and transformed data ready for analysis

## Guidelines

### Raw Data (`raw/`)

- **Never modify files in this directory**
- Store original data exactly as received
- Include metadata files when available (e.g., data dictionaries, codebooks)
- Document data sources in a `sources.md` file or in the main documentation

### Processed Data (`processed/`)

- Store cleaned and transformed datasets here
- Name files descriptively (e.g., `survey_data_cleaned.csv`)
- Document transformations in your scripts or notebooks
- Include data dictionaries for processed datasets

## Data Management Best Practices

1. **Version Control:**
   - Small datasets (< 10 MB) can be committed to git
   - Large datasets should be stored externally (cloud storage, institutional repositories)
   - Use `.gitignore` to exclude large files

2. **Documentation:**
   - Always document data sources with URLs, dates accessed, and citations
   - Include data dictionaries describing variables, units, and coding schemes
   - Note any data quality issues or limitations

3. **Privacy and Ethics:**
   - Never commit sensitive or personally identifiable information (PII)
   - Follow IRB protocols if working with human subjects data
   - Respect data use agreements and licenses

4. **File Formats:**
   - Prefer open, non-proprietary formats (CSV, JSON, Parquet)
   - Include format conversion scripts if needed
   - Document any special encoding or formatting

## Example Data Dictionary

Create a file like `data_dictionary.md` or `codebook.csv` with this information:

| Variable Name | Description | Type | Unit | Valid Range | Missing Code |
|--------------|-------------|------|------|-------------|--------------|
| participant_id | Unique participant identifier | Integer | - | 1-1000 | NA |
| age | Participant age | Integer | years | 18-99 | -1 |
| response_time | Time to complete survey | Float | seconds | 0-3600 | -999 |

## Data Sources

Document your data sources here or in `docs/data_sources.md`:

- **Dataset Name:** [Source URL]
  - Date Accessed: YYYY-MM-DD
  - License: [License type]
  - Citation: [Proper citation]
