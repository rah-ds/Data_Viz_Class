# Data Dictionary Template

Use this template to document your datasets. Good documentation makes your data understandable and reusable.

## Dataset Information

- **Dataset Name:** [Descriptive name]
- **Version:** [e.g., v1.0]
- **Last Updated:** [YYYY-MM-DD]
- **Source File:** [Path to data file, e.g., `data/processed/survey_clean.csv`]
- **Source Data:** [Original data source, e.g., `data/raw/survey_raw.csv`]
- **Processing Script:** [Script that created this file, e.g., `scripts/01_clean_data.py`]

## Overview

- **Number of Rows:** [e.g., 456]
- **Number of Columns:** [e.g., 12]
- **Date Range:** [If applicable, e.g., "2025-01-01 to 2025-12-31"]
- **Geographic Coverage:** [If applicable, e.g., "United States"]
- **Unit of Analysis:** [e.g., "Individual participants", "US counties", "Daily measurements"]

## Description

[Provide a brief description of what this dataset contains and its purpose]

Example:
> This dataset contains cleaned survey responses from 456 participants who completed an online questionnaire about consumer preferences. Data was collected between November and December 2025. Participants who failed attention checks have been removed.

## Variables

### Categorical Variables

| Variable Name | Type | Description | Values | Missing Code | Notes |
|--------------|------|-------------|--------|--------------|-------|
| participant_id | string | Unique participant identifier | P001-P500 | None | Primary key |
| gender | string | Self-reported gender | M, F, NB, Other, Prefer not to say | NA | 12 missing values |
| education | string | Highest education level | High School, Some College, Bachelor's, Master's, PhD | NA | 5 levels |
| region | string | Geographic region | Northeast, South, Midwest, West | None | Based on ZIP code |

### Continuous Variables

| Variable Name | Type | Description | Unit | Valid Range | Missing Code | Notes |
|--------------|------|-------------|------|-------------|--------------|-------|
| age | integer | Participant age | years | 18-89 | -1 | 8 missing values |
| income | float | Annual household income | USD | 0-500000 | -999 | Values >500k top-coded |
| satisfaction | integer | Overall satisfaction score | 1-7 scale | 1-7 | -1 | Likert scale (1=very dissatisfied, 7=very satisfied) |
| response_time | float | Survey completion time | seconds | 60-3600 | -999 | Times >1 hour flagged for quality |

### Date/Time Variables

| Variable Name | Type | Description | Format | Valid Range | Missing Code | Notes |
|--------------|------|-------------|--------|-------------|--------------|-------|
| survey_date | date | Date survey was completed | YYYY-MM-DD | 2025-11-01 to 2025-12-31 | NA | 2 missing dates |
| timestamp | datetime | Exact submission time | YYYY-MM-DD HH:MM:SS | 2025-11-01 to 2025-12-31 | NA | UTC timezone |

## Data Processing

### Transformations Applied

Document all changes made to the raw data:

1. **Quality Control:**
   - Removed 44 participants who failed attention checks (attention_check != "pass")
   - Excluded responses with completion times < 60 seconds (likely bots)

2. **Missing Data Handling:**
   - Age: 8 missing values coded as -1
   - Income: 23 missing values coded as -999
   - Gender: 12 missing values coded as "NA"

3. **Outlier Treatment:**
   - Income values > $500,000 top-coded at $500,000 (n=7)
   - Response times > 1 hour flagged but retained (n=12)

4. **Variable Creation:**
   - Created `age_group` from `age` (18-29, 30-44, 45-59, 60+)
   - Created `income_category` from `income` (Low, Middle, High based on tertiles)

5. **Recoding:**
   - Education levels standardized from free-text responses
   - State names converted to region codes

### Excluded Records

- 44 participants excluded for failed attention checks
- 3 participants excluded for duplicate IDs
- 2 participants excluded for incomplete responses (<50% complete)

**Final Sample:** 456 participants (from original 505)

## Data Quality

### Known Issues

- **Income data:** High number of missing values (23/456 = 5%)
- **Response times:** 12 participants took >1 hour (possible interruptions)
- **Gender:** Free-text option led to inconsistent responses, manually recoded

### Validation Checks

- ✓ No duplicate participant IDs
- ✓ All ages within valid range
- ✓ All satisfaction scores between 1-7
- ✓ All dates within collection period
- ⚠ Income data has 5% missing values (acceptable)

## Data Source

### Original Data

- **Source:** Qualtrics survey platform
- **Collection Method:** Online survey distributed via email
- **Sample Frame:** University students and community members
- **Response Rate:** 456/1200 = 38%
- **Incentive:** $10 Amazon gift card
- **IRB Approval:** Protocol #2025-001 (approved 2025-10-15)

### Citation

If using this data, please cite:

> [Your Name/Team] (2026). Consumer Preferences Survey Data. SARC 5400 - Data Visualization, University of Virginia. [URL or DOI if available]

## Usage Guidelines

### Recommended Uses

- Analyzing demographic patterns in consumer preferences
- Testing relationships between satisfaction and demographics
- Creating data visualizations for educational purposes

### Limitations

- Sample is not representative of general population (convenience sample)
- Self-reported data subject to social desirability bias
- Cross-sectional design limits causal inference

### Restrictions

- Data is for educational purposes only
- Do not attempt to re-identify participants
- Aggregate results only (no individual-level reporting)
- Cite this dataset if used in publications

## Contact

For questions about this dataset:
- **Name:** [Your name]
- **Email:** [Your email]
- **Course:** SARC 5400 - Data Visualization
- **Term:** Spring 2026

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-05 | Initial cleaned dataset | [Your name] |
| 1.1 | 2026-01-10 | Added age_group variable | [Your name] |

## Additional Notes

[Any other important information about the dataset]

---

## Example Code for Loading Data

### Python

```python
import pandas as pd

# Load data
df = pd.read_csv('data/processed/survey_clean.csv')

# Handle missing values
df['age'] = df['age'].replace(-1, pd.NA)
df['income'] = df['income'].replace(-999, pd.NA)

# Convert date column
df['survey_date'] = pd.to_datetime(df['survey_date'])

print(f"Loaded {len(df)} records with {len(df.columns)} columns")
```

### R

```r
library(tidyverse)

# Load data
df <- read_csv('data/processed/survey_clean.csv')

# Handle missing values
df <- df %>%
  mutate(
    age = na_if(age, -1),
    income = na_if(income, -999)
  )

# Convert date column
df$survey_date <- as.Date(df$survey_date)

cat(sprintf("Loaded %d records with %d columns\n", nrow(df), ncol(df)))
```

---

**Template Version:** 1.0
**Last Updated:** 2026-01-05
