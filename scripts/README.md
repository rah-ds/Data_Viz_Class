# Scripts

This directory contains analysis scripts and code for data processing and visualization.

## Purpose

Store reusable code for:
- Data cleaning and preprocessing
- Statistical analysis
- Data visualization
- Model training and evaluation
- Utility functions and helpers

## Organization

### Naming Convention

Use numbered prefixes to indicate execution order:

```
scripts/
├── 01_data_cleaning.py
├── 02_exploratory_analysis.py
├── 03_create_visualizations.py
└── utils/
    ├── __init__.py
    └── plotting_helpers.py
```

### Language-Specific Structures

**Python:**
```
scripts/
├── 01_clean_data.py
├── 02_analyze.py
├── 03_visualize.py
└── utils/
    └── helpers.py
```

**R:**
```
scripts/
├── 01_clean_data.R
├── 02_analyze.R
├── 03_visualize.R
└── functions.R
```

## Best Practices

### 1. Code Style

- Follow language-specific style guides (PEP 8 for Python, tidyverse for R)
- Use consistent naming conventions
- Keep functions focused and modular
- Add docstrings/comments for complex logic

### 2. Structure

```python
"""
Script: 01_data_cleaning.py
Purpose: Clean raw survey data and prepare for analysis
Author: Your Name
Date: 2026-01-05
"""

# Imports
import pandas as pd
import numpy as np
from pathlib import Path

# Constants
RAW_DATA_PATH = Path('data/raw/survey.csv')
PROCESSED_DATA_PATH = Path('data/processed/survey_cleaned.csv')

# Functions
def remove_invalid_responses(df):
    """Remove responses that failed attention checks."""
    return df[df['attention_check'] == 'pass']

# Main execution
if __name__ == '__main__':
    # Load data
    df = pd.read_csv(RAW_DATA_PATH)
    
    # Process
    df_clean = remove_invalid_responses(df)
    
    # Save
    df_clean.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Saved {len(df_clean)} rows to {PROCESSED_DATA_PATH}")
```

### 3. Documentation

- Start each script with a header comment explaining purpose
- Comment complex algorithms or non-obvious decisions
- Document function parameters and return values
- Include usage examples for key functions

### 4. Error Handling

```python
# Check inputs
if not RAW_DATA_PATH.exists():
    raise FileNotFoundError(f"Raw data not found: {RAW_DATA_PATH}")

# Validate data
assert df['id'].is_unique, "Duplicate IDs found in data"

# Log progress
print(f"Processing {len(df)} records...")
```

### 5. Reproducibility

- Use random seeds for any stochastic processes
- Document software versions and dependencies
- Avoid hardcoded paths when possible (use relative paths or constants)
- Make scripts idempotent (safe to run multiple times)

## Example Scripts

### Python Data Cleaning Template

```python
"""Template for data cleaning scripts."""

import pandas as pd
from pathlib import Path

# Configuration
INPUT_FILE = Path('data/raw/input.csv')
OUTPUT_FILE = Path('data/processed/output.csv')

def clean_data(df):
    """Apply cleaning transformations."""
    df = df.copy()
    # Add your cleaning steps here
    return df

def main():
    """Main execution function."""
    # Load
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} rows")
    
    # Clean
    df_clean = clean_data(df)
    print(f"Cleaned to {len(df_clean)} rows")
    
    # Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
```

### R Analysis Template

```r
# Script: analysis_template.R
# Purpose: Template for analysis scripts
# Author: Your Name
# Date: 2026-01-05

# Load libraries
library(tidyverse)
library(here)

# Configuration
INPUT_FILE <- here("data", "processed", "clean_data.csv")
OUTPUT_DIR <- here("results")

# Load data
data <- read_csv(INPUT_FILE)

# Analysis
results <- data %>%
  group_by(category) %>%
  summarize(
    mean_value = mean(value, na.rm = TRUE),
    sd_value = sd(value, na.rm = TRUE)
  )

# Save results
write_csv(results, file.path(OUTPUT_DIR, "summary_stats.csv"))
```

## Testing

Consider adding tests for your functions:

```python
# tests/test_cleaning.py
import pytest
from scripts.utils.helpers import remove_invalid_responses

def test_remove_invalid_responses():
    # Create test data
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'attention_check': ['pass', 'fail', 'pass']
    })
    
    # Apply function
    result = remove_invalid_responses(df)
    
    # Assert expectations
    assert len(result) == 2
    assert all(result['attention_check'] == 'pass')
```

## Resources

- [PEP 8 Style Guide (Python)](https://pep8.org/)
- [Tidyverse Style Guide (R)](https://style.tidyverse.org/)
- [Writing Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
