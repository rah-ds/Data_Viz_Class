# Documentation

This directory contains project documentation, reports, and supplementary materials.

## Purpose

Store:
- Project reports and write-ups
- Data documentation (data dictionaries, codebooks)
- Methodology documentation
- Analysis notes
- Presentations and slides
- Supplementary materials

## Contents

- `reproducibility.md` - Guide for reproducible research practices
- Additional documentation files as needed for your projects

## Suggested Files

### Data Documentation

**`data_sources.md`** - Document all data sources:

```markdown
# Data Sources

## Dataset 1: US Census Data
- **URL:** https://data.census.gov/...
- **Date Accessed:** 2026-01-05
- **License:** Public Domain
- **Description:** County-level population data
- **Citation:** U.S. Census Bureau (2020)...
```

**`data_dictionary.md`** - Describe variables:

```markdown
# Data Dictionary

## Variables

| Variable | Type | Description | Range | Missing |
|----------|------|-------------|-------|---------|
| age | int | Participant age in years | 18-89 | -1 |
| income | float | Annual income (USD) | 0-500000 | -999 |
```

### Analysis Documentation

**`analysis_plan.md`** - Document your analysis approach:

```markdown
# Analysis Plan

## Research Question
What factors predict customer satisfaction?

## Hypotheses
1. H1: Age is positively correlated with satisfaction
2. H2: Income predicts satisfaction after controlling for age

## Methods
- Descriptive statistics
- Correlation analysis
- Multiple regression

## Planned Visualizations
1. Age distribution histogram
2. Satisfaction by income scatterplot
3. Regression diagnostics plots
```

**`methodology.md`** - Detailed methods:

```markdown
# Methodology

## Data Collection
- Survey distributed via Qualtrics
- Sample: 500 participants
- Period: Nov-Dec 2025

## Data Cleaning
1. Removed incomplete responses (n=44)
2. Addressed outliers in income (> 3 SD)
3. Recoded missing values

## Statistical Analysis
- Software: Python 3.11, statsmodels 0.14
- Significance level: α = 0.05
- Multiple testing correction: Bonferroni
```

### Results Documentation

**`results_summary.md`** - Summarize findings:

```markdown
# Results Summary

## Key Findings

1. **Finding 1**: Age is significantly correlated with satisfaction (r=0.45, p<0.001)
2. **Finding 2**: Income predicts satisfaction (β=0.32, p=0.002)
3. **Finding 3**: Model explains 34% of variance (R²=0.34)

## Figures

- **Figure 1** (`results/figures/fig1.png`): Age distribution
- **Figure 2** (`results/figures/fig2.png`): Satisfaction vs income

## Tables

- **Table 1** (`results/tables/descriptive_stats.csv`): Summary statistics
- **Table 2** (`results/tables/regression.csv`): Regression results
```

### Project Reports

Create reports for assignments or projects:

**`assignment1_report.md`** or **`project_report.md`**

```markdown
# Project Report: Customer Satisfaction Analysis

**Author:** Your Name
**Date:** 2026-01-05
**Course:** SARC 5400 - Data Visualization

## Abstract

Brief summary of the project...

## Introduction

Background and research question...

## Methods

Data and analysis approach...

## Results

### Descriptive Statistics
Table 1 shows...

### Main Analysis
Figure 1 illustrates...

## Discussion

Interpretation of findings...

## Conclusion

Summary and implications...

## References

1. Citation 1
2. Citation 2
```

## Best Practices

### 1. Use Clear Filenames

```
docs/
├── 01_data_sources.md
├── 02_methodology.md
├── 03_results_summary.md
└── assignment1_report.md
```

### 2. Keep Documentation Updated

- Update as the project evolves
- Document decisions and rationale
- Note any deviations from plans

### 3. Version Control

- Commit documentation with related code changes
- Use meaningful commit messages
- Tag important versions

### 4. Link to Other Files

Reference specific files in your documentation:

```markdown
See [data cleaning script](../scripts/01_clean_data.py) for details.

Results are in [results/figures/](../results/figures/).
```

### 5. Use Consistent Formatting

- Follow markdown conventions
- Use headers hierarchically
- Include code blocks with syntax highlighting
- Add tables for structured information

## Templates

### Report Template

```markdown
# [Project Title]

**Author:** [Your Name]
**Date:** [Date]
**Course:** SARC 5400 - Data Visualization

## 1. Introduction

### Background
[Provide context]

### Research Question
[State your question]

### Objectives
- Objective 1
- Objective 2

## 2. Data

### Data Sources
[Describe data]

### Variables
[List key variables]

### Data Quality
[Discuss any issues]

## 3. Methods

### Data Processing
[Cleaning steps]

### Analysis Approach
[Statistical methods]

### Visualization Strategy
[Chart types and rationale]

## 4. Results

### Descriptive Statistics
[Present summary stats]

### Main Findings
[Present key results with figures/tables]

### Supplementary Analyses
[Additional findings]

## 5. Discussion

### Interpretation
[What do results mean?]

### Limitations
[Acknowledge limitations]

### Implications
[So what?]

## 6. Conclusion

[Summarize key points]

## 7. References

[List sources]

## 8. Appendices

### Appendix A: Additional Figures
### Appendix B: Code Listings
```

## Resources

- [Markdown Guide](https://www.markdownguide.org/)
- [Academic Writing Guide](https://writingcenter.unc.edu/tips-and-tools/)
- [Data Documentation Best Practices](https://www.dataone.org/best-practices)
