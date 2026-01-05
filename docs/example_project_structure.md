# Example Project Structure

This document provides an example of how to organize a data visualization project within this repository.

## Scenario

You're working on **Assignment 1: Analyzing City Demographics** where you need to:
1. Download census data
2. Clean and prepare the data
3. Create visualizations showing demographic patterns
4. Write a report with your findings

## Step-by-Step Organization

### 1. Create a Project Branch

```bash
git checkout -b assignment1-demographics
```

### 2. Organize Your Data

```
data/
├── raw/
│   ├── census_2020.csv          # Original downloaded data
│   ├── census_codebook.pdf      # Variable descriptions
│   └── sources.md               # Document where data came from
└── processed/
    ├── census_clean.csv         # Cleaned data
    └── census_aggregated.csv    # City-level aggregations
```

**Create `data/raw/sources.md`:**

```markdown
# Data Sources for Assignment 1

## US Census Data 2020
- **Source:** US Census Bureau
- **URL:** https://data.census.gov/cedsci/
- **Date Downloaded:** 2026-01-05
- **License:** Public Domain
- **Description:** County-level demographic data including age, race, income
- **File:** census_2020.csv
```

### 3. Organize Your Code

```
scripts/
├── 01_download_data.py          # Download census data
├── 02_clean_data.py             # Clean and validate data
├── 03_aggregate_cities.py       # Aggregate to city level
├── 04_create_visualizations.py  # Generate all figures
└── utils/
    └── plotting_helpers.py      # Reusable plotting functions
```

**Example: `scripts/01_download_data.py`**

```python
"""
Download Census Data

This script downloads 2020 US Census data for the assignment.
Run this first before other scripts.

Usage:
    python scripts/01_download_data.py
"""

import pandas as pd
from pathlib import Path

# Configuration
OUTPUT_DIR = Path('data/raw')
OUTPUT_FILE = OUTPUT_DIR / 'census_2020.csv'
DATA_URL = 'https://example.census.gov/data.csv'

def main():
    """Download census data."""
    print(f"Downloading data from {DATA_URL}...")
    
    # Download (replace with actual download code)
    df = pd.read_csv(DATA_URL)
    
    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"Saved {len(df)} rows to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
```

### 4. Exploratory Analysis in Notebooks

```
notebooks/
├── 01_data_exploration.ipynb    # Initial EDA
├── 02_visualization_drafts.ipynb # Try different viz approaches
└── 03_final_analysis.ipynb      # Clean final analysis
```

**Example notebook structure:**

```python
# =============================================================================
# Assignment 1: City Demographics Exploration
# Author: Your Name
# Date: 2026-01-05
# =============================================================================

# %% Setup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline
sns.set_style('whitegrid')

# %% Load Data
df = pd.read_csv('../data/processed/census_clean.csv')
print(f"Loaded {len(df)} cities")

# %% Quick Overview
df.head()
df.describe()
df.info()

# %% Check for Missing Values
df.isnull().sum()

# %% Age Distribution
plt.figure(figsize=(10, 6))
plt.hist(df['median_age'], bins=30, edgecolor='black')
plt.xlabel('Median Age (years)')
plt.ylabel('Number of Cities')
plt.title('Distribution of Median Age Across US Cities')
plt.savefig('../results/figures/age_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# %% Income by Region
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='region', y='median_income')
plt.xlabel('Region')
plt.ylabel('Median Income ($)')
plt.title('Income Distribution by Region')
plt.xticks(rotation=45)
plt.savefig('../results/figures/income_by_region.png', dpi=300, bbox_inches='tight')
plt.show()

# %% Key Findings
print("""
Key Findings:
1. Median age ranges from 22 to 68 years across cities
2. West coast cities have highest median incomes
3. Strong correlation between education and income (r=0.72)
""")
```

### 5. Store Results

```
results/
├── figures/
│   ├── exploratory/
│   │   ├── age_hist_draft1.png
│   │   └── income_scatter_draft.png
│   └── final/
│       ├── figure1_age_distribution.png
│       ├── figure2_income_by_region.png
│       └── figure3_education_income.png
├── tables/
│   ├── summary_statistics.csv
│   └── top_10_cities.csv
└── README.md
```

### 6. Document Your Work

```
docs/
├── assignment1_report.md        # Your main report
├── data_dictionary.md           # Document variables
└── analysis_notes.md            # Decisions and findings
```

**Example: `docs/assignment1_report.md`**

```markdown
# Assignment 1: City Demographics Analysis

**Author:** Your Name
**Date:** 2026-01-05
**Course:** SARC 5400 - Data Visualization

## Introduction

This analysis examines demographic patterns across 500 US cities using 2020 Census data. The goal is to understand relationships between age, income, education, and geographic region.

## Data

### Source
- US Census Bureau 2020 County-level data
- 500 largest US cities
- Variables: median_age, median_income, education_rate, region

### Processing
See `scripts/02_clean_data.py` for details:
1. Removed 12 cities with missing data
2. Aggregated county data to city level
3. Created region categories

## Methods

### Analysis
- Descriptive statistics for all variables
- Correlation analysis
- Group comparisons by region

### Visualizations
1. Histogram of age distribution
2. Box plots of income by region
3. Scatter plot of education vs income

## Results

### Finding 1: Age Distribution
Cities show a wide range of median ages (Figure 1), with most cities between 30-40 years. College towns skew younger (median=25), while retirement communities are older (median=65).

![Age Distribution](../results/figures/final/figure1_age_distribution.png)
*Figure 1: Distribution of median age across 500 US cities*

### Finding 2: Regional Income Differences
Significant income disparities exist across regions (Figure 2). West coast cities have highest median income ($78,000), while southern cities have lowest ($52,000). F(3,496)=45.2, p<0.001.

![Income by Region](../results/figures/final/figure2_income_by_region.png)
*Figure 2: Median income distribution by geographic region*

### Finding 3: Education-Income Relationship
Strong positive correlation between education and income (r=0.72, p<0.001). Each 10% increase in bachelor's degree holders associated with $8,000 higher median income.

![Education vs Income](../results/figures/final/figure3_education_income.png)
*Figure 3: Relationship between education level and median income*

## Discussion

Results reveal:
1. Geographic disparities in economic outcomes
2. Education as key factor in city prosperity
3. Age demographics vary by city type

### Limitations
- Cross-sectional data (no causality)
- City boundaries may not reflect metro areas
- 2020 data may not reflect post-pandemic changes

## Conclusion

This analysis demonstrates clear patterns in US city demographics, with education and region as key factors explaining income differences. These patterns have implications for policy and urban planning.

## References

1. US Census Bureau (2020). American Community Survey.
2. Course materials, SARC 5400 Data Visualization.

## Reproducibility

All analyses can be reproduced by running:
```bash
python scripts/01_download_data.py
python scripts/02_clean_data.py
python scripts/03_aggregate_cities.py
python scripts/04_create_visualizations.py
```
```

### 7. Final Project Structure

```
Data_Viz_Class/
├── data/
│   ├── raw/
│   │   ├── census_2020.csv
│   │   ├── census_codebook.pdf
│   │   └── sources.md
│   └── processed/
│       ├── census_clean.csv
│       └── census_aggregated.csv
├── scripts/
│   ├── 01_download_data.py
│   ├── 02_clean_data.py
│   ├── 03_aggregate_cities.py
│   ├── 04_create_visualizations.py
│   └── utils/
│       └── plotting_helpers.py
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_visualization_drafts.ipynb
│   └── 03_final_analysis.ipynb
├── results/
│   ├── figures/
│   │   ├── exploratory/
│   │   │   └── [draft plots]
│   │   └── final/
│   │       ├── figure1_age_distribution.png
│   │       ├── figure2_income_by_region.png
│   │       └── figure3_education_income.png
│   └── tables/
│       ├── summary_statistics.csv
│       └── top_10_cities.csv
├── docs/
│   ├── assignment1_report.md
│   ├── data_dictionary.md
│   └── analysis_notes.md
├── requirements.txt
├── environment.yml
└── README.md
```

## Workflow

### Daily Workflow

```bash
# 1. Start working
git checkout assignment1-demographics
conda activate data-viz

# 2. Work on your analysis
python scripts/02_clean_data.py
jupyter lab  # For exploratory work

# 3. Commit progress
git add data/processed/census_clean.csv
git add scripts/02_clean_data.py
git add notebooks/01_data_exploration.ipynb
git commit -m "feat: complete data cleaning and initial exploration"

# 4. Push changes
git push origin assignment1-demographics
```

### Submission Workflow

```bash
# 1. Generate final outputs
python scripts/04_create_visualizations.py

# 2. Write report
# Edit docs/assignment1_report.md

# 3. Final commit
git add results/figures/final/
git add docs/assignment1_report.md
git commit -m "docs: complete assignment 1 report with visualizations"

# 4. Create a tag
git tag -a assignment1-v1.0 -m "Assignment 1 submission"
git push origin assignment1-v1.0

# 5. Merge to main (if appropriate)
git checkout main
git merge assignment1-demographics
git push origin main
```

## Tips for Success

### 1. Start with Structure

Before writing any code:
- [ ] Create directory structure
- [ ] Document data sources
- [ ] Outline analysis plan
- [ ] Set up environment

### 2. Work Incrementally

Don't try to do everything at once:
1. Download and explore data (Day 1)
2. Clean data (Day 2)
3. Create visualizations (Day 3)
4. Write report (Day 4)
5. Review and polish (Day 5)

### 3. Commit Frequently

```bash
git commit -m "feat: add data download script"
git commit -m "feat: complete data cleaning"
git commit -m "fix: correct age filter bug"
git commit -m "docs: add data dictionary"
git commit -m "feat: create age distribution plot"
```

### 4. Document as You Go

Don't wait until the end to write documentation. Document:
- Data sources when you download them
- Decisions when you make them
- Issues when you encounter them
- Findings when you discover them

### 5. Keep It Clean

Before submitting:
- [ ] Remove unused code
- [ ] Clear notebook outputs
- [ ] Delete draft files
- [ ] Check for typos in reports
- [ ] Verify all paths work
- [ ] Test reproduction instructions

## Common Pitfalls to Avoid

❌ **Don't:**
- Hard-code absolute paths (`/Users/alice/project/data.csv`)
- Commit large data files without thinking
- Mix multiple assignments in one commit
- Skip documentation
- Forget to test reproducibility

✅ **Do:**
- Use relative paths (`data/raw/data.csv`)
- Check file sizes before committing
- Use clear, descriptive commit messages
- Document throughout
- Test that scripts run from scratch

## Resources

- [Main README](../README.md) - Repository overview
- [Contributing Guide](../CONTRIBUTING.md) - Code style and practices
- [Reproducibility Guide](reproducibility.md) - Detailed reproducibility info
- [Data Dictionary Template](data_dictionary_template.md) - Document your data

---

**Good luck with your projects!** Remember, the goal is not just to complete the analysis, but to create work that is clear, reproducible, and professional.
