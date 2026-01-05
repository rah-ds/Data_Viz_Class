# Notebooks

This directory contains Jupyter notebooks (`.ipynb`) and R Markdown files (`.Rmd`) for exploratory analysis, visualization, and reporting.

## Purpose

Notebooks are ideal for:
- Exploratory data analysis (EDA)
- Interactive visualizations
- Documenting analysis workflows
- Creating reports and presentations
- Teaching and demonstration
- Prototyping before creating production scripts

## Organization

### Naming Convention

Use descriptive names with numbered prefixes:

```
notebooks/
├── 01_data_exploration.ipynb
├── 02_visualization_experiments.ipynb
├── 03_final_analysis.ipynb
└── archive/
    └── old_exploratory_work.ipynb
```

### Organization Tips

- Number notebooks in logical order
- Use clear, descriptive names
- Move outdated notebooks to an `archive/` folder
- Keep notebooks focused on specific tasks

## Best Practices

### 1. Notebook Structure

```markdown
# Title: Data Exploration for Survey Analysis
**Author:** Your Name  
**Date:** 2026-01-05  
**Purpose:** Initial exploration of survey responses

## Table of Contents
1. Setup and Imports
2. Load Data
3. Data Quality Check
4. Exploratory Analysis
5. Key Findings
6. Next Steps

---

## 1. Setup and Imports
```

### 2. Cell Organization

```python
# CELL 1: Imports and Configuration
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline
sns.set_style('whitegrid')

# CELL 2: Load Data
df = pd.read_csv('../data/processed/survey_clean.csv')

# CELL 3: Quick overview
print(f"Shape: {df.shape}")
df.head()

# CELL 4: Visualization
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='age', bins=20)
plt.title('Age Distribution')
plt.show()
```

### 3. Documentation

- Add markdown cells to explain your thinking
- Document unexpected findings
- Include interpretations of visualizations
- Note any decisions or assumptions
- Summarize key insights at the end

### 4. Code Quality

- Keep cells short and focused
- Extract repeated code into functions
- Import utilities from `scripts/utils/`
- Restart kernel and run all cells before sharing
- Clear output before committing (for cleaner diffs)

### 5. Reproducibility

```python
# Set random seeds
import random
import numpy as np

random.seed(42)
np.random.seed(42)

# Document versions
import sys
print(f"Python version: {sys.version}")
print(f"Pandas version: {pd.__version__}")
```

## Jupyter Notebook Tips

### Installation

```bash
pip install jupyter notebook
# or
pip install jupyterlab
```

### Running Notebooks

```bash
# Classic Notebook
jupyter notebook

# JupyterLab (recommended)
jupyter lab
```

### Useful Magic Commands

```python
# Timing
%time df.groupby('category').mean()  # Single run
%timeit df.groupby('category').mean()  # Multiple runs

# Debugging
%debug  # Enter debugger after error

# System commands
!ls ../data/raw/

# Load external scripts
%load scripts/utils/helpers.py

# Autoreload modules
%load_ext autoreload
%autoreload 2
```

### Keyboard Shortcuts

- `Shift + Enter`: Run cell and move to next
- `Ctrl + Enter`: Run cell and stay
- `A`: Insert cell above
- `B`: Insert cell below
- `D, D`: Delete cell
- `M`: Convert cell to markdown
- `Y`: Convert cell to code

## R Markdown Tips

### Installation

```r
install.packages("rmarkdown")
install.packages("knitr")
```

### Basic Structure

```markdown
---
title: "Data Analysis Report"
author: "Your Name"
date: "`r Sys.Date()`"
output: 
  html_document:
    toc: true
    toc_float: true
    code_folding: hide
---

## Setup

​```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE, message = FALSE, warning = FALSE)
library(tidyverse)
library(here)
​```

## Load Data

​```{r load-data}
data <- read_csv(here("data", "processed", "clean_data.csv"))
​```

## Analysis

​```{r analysis}
summary_stats <- data %>%
  group_by(category) %>%
  summarize(mean_val = mean(value))

summary_stats
​```
```

### Rendering

```r
# In R console
rmarkdown::render("notebooks/analysis.Rmd")

# Or use RStudio "Knit" button
```

## Version Control

### Before Committing

1. **Clear outputs** to reduce file size and make diffs cleaner:
   ```bash
   # Using nbconvert
   jupyter nbconvert --clear-output --inplace notebook.ipynb
   ```

2. **Run all cells** to ensure notebook executes from top to bottom

3. **Check for sensitive data** (passwords, API keys, PII)

### Git Configuration

Add to `.gitattributes`:
```
*.ipynb filter=nbstripout
*.ipynb diff=jupyternotebook
```

## Converting Notebooks

### To Python Script

```bash
jupyter nbconvert --to python notebook.ipynb
```

### To HTML Report

```bash
jupyter nbconvert --to html notebook.ipynb
```

### To PDF

```bash
jupyter nbconvert --to pdf notebook.ipynb  # Requires LaTeX
```

## Example Notebook Structure

```python
# ========================================
# Title: Customer Segmentation Analysis
# Author: Jane Doe
# Date: 2026-01-05
# ========================================

# ## 1. Setup and Configuration

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
DATA_PATH = Path('../data/processed/customers.csv')
FIGURE_PATH = Path('../results/figures/')
FIGURE_PATH.mkdir(exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Style settings
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# ## 2. Load and Inspect Data

df = pd.read_csv(DATA_PATH)
print(f"Dataset shape: {df.shape}")
print(f"\nColumn types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")
df.head()

# ## 3. Exploratory Analysis

# ... analysis code ...

# ## 4. Key Findings

# **Summary:**
# 1. Finding one...
# 2. Finding two...
# 3. Finding three...

# ## 5. Next Steps

# - [ ] Further analysis needed on X
# - [ ] Create final visualizations for Y
# - [ ] Write up results in report
```

## Resources

- [Jupyter Documentation](https://jupyter.org/documentation)
- [R Markdown Guide](https://rmarkdown.rstudio.com/)
- [Gallery of Interesting Notebooks](https://github.com/jupyter/jupyter/wiki)
