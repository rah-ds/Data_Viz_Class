# Reproducibility Guide

This guide outlines best practices for ensuring your research is reproducible. Following these guidelines will help you and others replicate your analyses and build upon your work.

## Table of Contents

1. [What is Reproducibility?](#what-is-reproducibility)
2. [Version Control Practices](#version-control-practices)
3. [Data Management](#data-management)
4. [Code Organization](#code-organization)
5. [Documentation Standards](#documentation-standards)
6. [Environment Management](#environment-management)
7. [How to Reproduce Results](#how-to-reproduce-results)

## What is Reproducibility?

**Reproducibility** means that someone else (or future you) can:
- Obtain the same results from the same data using your code
- Understand what you did and why
- Verify your findings
- Build upon your work

### Levels of Reproducibility

1. **Computational reproducibility**: Same results from same code + data
2. **Statistical reproducibility**: Same conclusions from independent analyses
3. **Empirical reproducibility**: Same findings from new data collection

This guide focuses on **computational reproducibility**.

## Version Control Practices

### Why Version Control?

Version control (Git) helps you:
- Track changes over time
- Collaborate with others
- Revert to previous versions
- Document your workflow

### Git Workflow

**1. Commit Often**

Make small, frequent commits with clear messages:

```bash
# Good commits
git add scripts/01_clean_data.py
git commit -m "feat: add age validation to data cleaning"

git add results/figures/income_dist.png
git commit -m "docs: add income distribution visualization"

# Bad commits
git add .
git commit -m "updates"
```

**2. Use Branches**

Create branches for different features or analyses:

```bash
# Create a new branch
git checkout -b analysis-income-inequality

# Work on your analysis
# ... make changes ...

# Commit changes
git add .
git commit -m "feat: complete income inequality analysis"

# Merge back to main
git checkout main
git merge analysis-income-inequality
```

**3. Write Meaningful Commit Messages**

Follow this format:

```
<type>: <short summary>

<optional detailed description>

<optional references>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**4. Don't Commit Sensitive Data**

Never commit:
- Passwords or API keys
- Personally identifiable information (PII)
- Large data files (> 10 MB)
- Proprietary data without permission

Use `.gitignore` to exclude sensitive files:

```bash
# Add to .gitignore
.env
secrets.json
data/raw/sensitive_data.csv
```

### Tags for Important Versions

Tag important milestones:

```bash
# Tag a release
git tag -a v1.0 -m "Analysis for assignment 1"
git push origin v1.0

# List tags
git tag -l
```

## Data Management

### Data Organization

```
data/
├── raw/              # Original, immutable data
│   ├── dataset1.csv
│   └── sources.md   # Document data sources
├── processed/        # Cleaned, processed data
│   ├── dataset1_clean.csv
│   └── README.md    # Document processing steps
└── README.md         # Overall data documentation
```

### Data Documentation

**Document data sources** in `data/raw/sources.md`:

```markdown
# Data Sources

## Census Data 2020
- **Source:** US Census Bureau
- **URL:** https://data.census.gov/...
- **Date Accessed:** 2026-01-05
- **License:** Public Domain
- **Description:** Population data by county
- **Citation:** U.S. Census Bureau (2020). American Community Survey...

## Survey Responses
- **Source:** Qualtrics survey
- **Collection Period:** 2025-11-01 to 2025-12-15
- **Sample Size:** 500 participants
- **IRB Approval:** #2025-001
- **Description:** Consumer preferences survey
```

**Create data dictionaries** for each dataset:

```markdown
# Data Dictionary: survey_clean.csv

## Overview
- **Rows:** 456
- **Columns:** 12
- **Source:** data/raw/survey_raw.csv
- **Processing:** scripts/01_clean_data.py
- **Date Created:** 2026-01-05

## Variables

| Variable | Type | Description | Valid Range | Missing Code |
|----------|------|-------------|-------------|--------------|
| participant_id | int | Unique participant identifier | 1-500 | None |
| age | int | Age in years | 18-89 | -1 |
| gender | str | Self-reported gender | M, F, NB, Other | NA |
| income | float | Annual income in USD | 0-500000 | -999 |
| satisfaction | int | Satisfaction score | 1-7 | -1 |

## Notes
- 44 participants removed for failing attention checks
- Income values > 500000 top-coded at 500000
- Missing gender responses coded as "NA"
```

### Data Management Rules

1. **Never modify raw data**
   - Keep original data unchanged
   - Document all transformations in scripts

2. **Make data processing reproducible**
   - Use scripts, not manual editing
   - Document transformation steps
   - Include data lineage information

3. **Version large datasets externally**
   - Store large files outside git
   - Use cloud storage (Google Drive, OneDrive, institutional repository)
   - Document where to find external data

4. **Respect data agreements**
   - Follow IRB protocols
   - Respect data use agreements
   - Cite data sources properly

## Code Organization

### Directory Structure

```
project/
├── data/              # Data files
├── scripts/           # Reusable scripts
│   ├── 01_clean_data.py
│   ├── 02_analyze.py
│   └── utils/        # Helper functions
├── notebooks/         # Exploratory notebooks
├── results/           # Generated outputs
│   ├── figures/
│   └── tables/
├── docs/              # Documentation
├── tests/             # Unit tests (optional)
├── requirements.txt   # Dependencies
└── README.md          # Project overview
```

### Code Style

**Use consistent naming:**

```python
# Good
def calculate_mean_income(data):
    """Calculate mean income by category."""
    return data.groupby('category')['income'].mean()

# Bad
def calcMean(d):
    return d.groupby('category')['income'].mean()
```

**Write modular code:**

```python
# Good: Small, focused functions
def load_data(filepath):
    """Load survey data from CSV."""
    return pd.read_csv(filepath)

def clean_data(df):
    """Remove invalid responses and handle missing values."""
    df = df[df['attention_check'] == 'pass']
    df = df.dropna(subset=['age', 'income'])
    return df

def main():
    """Main execution function."""
    df = load_data('data/raw/survey.csv')
    df_clean = clean_data(df)
    df_clean.to_csv('data/processed/survey_clean.csv', index=False)

# Bad: One giant function doing everything
def process_everything():
    df = pd.read_csv('data/raw/survey.csv')
    df = df[df['attention_check'] == 'pass']
    df = df.dropna(subset=['age', 'income'])
    df.to_csv('data/processed/survey_clean.csv', index=False)
```

**Handle paths correctly:**

```python
from pathlib import Path

# Good: Use pathlib for cross-platform compatibility
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data' / 'raw'
input_file = DATA_DIR / 'survey.csv'

# Also good: Relative paths from project root
input_file = 'data/raw/survey.csv'

# Bad: Absolute paths
input_file = '/Users/alice/projects/data-viz/data/raw/survey.csv'
```

### Execution Order

Number scripts to show execution order:

```
scripts/
├── 01_download_data.py      # First
├── 02_clean_data.py          # Second
├── 03_exploratory_analysis.py   # Third
├── 04_create_visualizations.py  # Fourth
└── utils/
    └── helpers.py             # Shared functions
```

## Documentation Standards

### Code Documentation

**Add docstrings to functions:**

```python
def calculate_summary_stats(data, column, group_by=None):
    """
    Calculate summary statistics for a column.
    
    Parameters
    ----------
    data : pd.DataFrame
        Input dataframe
    column : str
        Column name to analyze
    group_by : str, optional
        Column to group by (default: None)
        
    Returns
    -------
    pd.DataFrame
        Summary statistics (mean, std, min, max)
        
    Examples
    --------
    >>> stats = calculate_summary_stats(df, 'income')
    >>> stats = calculate_summary_stats(df, 'income', group_by='gender')
    """
    if group_by:
        return data.groupby(group_by)[column].describe()
    return data[column].describe()
```

**Comment complex logic:**

```python
# Use log transformation to handle right-skewed income distribution
# This helps meet normality assumptions for parametric tests
df['log_income'] = np.log1p(df['income'])

# Remove outliers beyond 3 standard deviations
# These likely represent data entry errors
mean = df['age'].mean()
std = df['age'].std()
df = df[(df['age'] > mean - 3*std) & (df['age'] < mean + 3*std)]
```

### Project Documentation

**README.md should include:**

1. Project title and description
2. Setup instructions
3. How to run the analysis
4. Dependencies
5. Project structure
6. Results summary
7. Citation information

**Example README structure:**

```markdown
# Project Title

Brief description of the project.

## Setup

1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download data: [instructions]

## Usage

Run scripts in order:
```bash
python scripts/01_clean_data.py
python scripts/02_analyze.py
python scripts/03_visualize.py
```

## Results

Key findings:
- Finding 1
- Finding 2
- Finding 3

See `results/` for all outputs.

## Citation

[How to cite this work]
```

## Environment Management

### Why Manage Environments?

Different projects need different package versions. Environment management:
- Ensures consistent package versions
- Avoids conflicts between projects
- Makes your work reproducible

### Python Environments

**Option 1: venv (built-in)**

```bash
# Create environment
python -m venv venv

# Activate
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt

# Save current packages
pip freeze > requirements.txt
```

**Option 2: conda (recommended)**

```bash
# Create environment from file
conda env create -f environment.yml

# Activate
conda activate data-viz

# Update environment file
conda env export > environment.yml

# Deactivate
conda deactivate
```

### R Environments

**Use `renv` package:**

```r
# Install renv
install.packages("renv")

# Initialize project
renv::init()

# Install packages (they'll be tracked)
install.packages("tidyverse")
install.packages("ggplot2")

# Save environment
renv::snapshot()

# Restore environment (on another machine)
renv::restore()
```

### Document Versions

Include version information in your analysis:

**Python:**

```python
import sys
import pandas as pd
import numpy as np

print("Software Versions:")
print(f"Python: {sys.version}")
print(f"Pandas: {pd.__version__}")
print(f"NumPy: {np.__version__}")
```

**R:**

```r
# At the end of your script
sessionInfo()
```

## How to Reproduce Results

### Create a Reproduction Guide

Add a `REPRODUCTION.md` file:

```markdown
# Reproduction Instructions

## Prerequisites

- Python 3.11+
- 16 GB RAM recommended
- 5 GB disk space

## Setup (15 minutes)

1. Clone repository:
   ```bash
   git clone https://github.com/username/project.git
   cd project
   ```

2. Create environment:
   ```bash
   conda env create -f environment.yml
   conda activate data-viz
   ```

3. Download data:
   - Census data: [URL] → save to `data/raw/census.csv`
   - Survey data: [URL] → save to `data/raw/survey.csv`

## Run Analysis (30 minutes)

Execute scripts in order:

```bash
python scripts/01_clean_data.py       # 5 min
python scripts/02_analyze.py          # 15 min
python scripts/03_visualize.py        # 10 min
```

## Expected Outputs

After running all scripts, you should have:

- `data/processed/clean_data.csv` (456 rows)
- `results/figures/fig1_distribution.png`
- `results/figures/fig2_comparison.png`
- `results/tables/summary_stats.csv`

## Verification

Check that results match:

```bash
python scripts/verify_results.py
```

Expected output:
```
✓ All results match reference values
✓ All figures generated successfully
```

## Troubleshooting

**Issue:** ImportError: No module named 'X'
**Solution:** Reinstall requirements: `pip install -r requirements.txt`

**Issue:** FileNotFoundError for data files
**Solution:** Download data files (see Setup step 3)
```

### Test Reproducibility

**Before submitting:**

1. Clone your repository to a fresh location
2. Follow your reproduction instructions
3. Verify you get the same results

```bash
# Test in a fresh environment
cd /tmp
git clone [your-repo-url] test-reproducibility
cd test-reproducibility
# Follow your reproduction instructions
```

### Random Seeds

Set random seeds for reproducibility:

**Python:**

```python
import random
import numpy as np

# Set seeds
random.seed(42)
np.random.seed(42)

# For pandas sampling
df.sample(n=100, random_state=42)

# For scikit-learn
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

**R:**

```r
# Set seed
set.seed(42)

# For sampling
sample_data <- df %>% sample_n(100)

# For train/test split
set.seed(42)
train_indices <- sample(1:nrow(df), 0.8 * nrow(df))
train_data <- df[train_indices, ]
test_data <- df[-train_indices, ]
```

## Reproducibility Checklist

Before sharing your work:

- [ ] All code is in version control
- [ ] Data sources are documented
- [ ] Data processing steps are scripted (not manual)
- [ ] Environment/dependencies are specified
- [ ] Random seeds are set
- [ ] README explains how to run the analysis
- [ ] Code runs from scratch in a fresh environment
- [ ] Results are documented
- [ ] Visualizations are high quality
- [ ] No hardcoded absolute paths
- [ ] No sensitive data is committed
- [ ] License is specified

## Additional Resources

### General
- [The Turing Way - Guide for Reproducible Research](https://the-turing-way.netlify.app/reproducible-research/reproducible-research.html)
- [Best Practices for Scientific Computing](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745)

### Version Control
- [Git Book](https://git-scm.com/book/en/v2)
- [GitHub Guides](https://guides.github.com/)

### Python
- [Python Packaging Guide](https://packaging.python.org/)
- [Conda User Guide](https://conda.io/projects/conda/en/latest/user-guide/index.html)

### R
- [R for Data Science](https://r4ds.had.co.nz/)
- [renv Documentation](https://rstudio.github.io/renv/)

### Data Visualization
- [Fundamentals of Data Visualization](https://clauswilke.com/dataviz/) by Claus O. Wilke
- [Data Visualization: A Practical Introduction](https://socviz.co/) by Kieran Healy

---

Remember: **Reproducibility is not just about code – it's about enabling others to understand and build upon your work.**
