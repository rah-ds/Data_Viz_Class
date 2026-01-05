# Results

This directory contains generated outputs from analyses and visualizations.

## Purpose

Store:
- Visualizations (charts, graphs, plots)
- Statistical results and summaries
- Processed outputs for reports
- Generated tables and figures
- Model outputs and predictions

## Organization

### Suggested Structure

```
results/
├── figures/              # Visualization outputs
│   ├── exploratory/     # EDA plots
│   ├── final/           # Publication-quality figures
│   └── interactive/     # HTML interactive visualizations
├── tables/              # Summary tables and statistics
├── models/              # Trained models and predictions
└── reports/             # Generated reports (HTML, PDF)
```

## Best Practices

### 1. Naming Convention

Use descriptive, systematic names:

```
figures/
├── 01_age_distribution.png
├── 02_income_by_category.png
├── 03_correlation_matrix.png
└── final/
    ├── figure1_main_result.png
    ├── figure2_comparison.png
    └── supplementary_figS1.png
```

### 2. File Formats

**For Figures:**
- **PNG**: Good for web, presentations (use high DPI: 300+)
- **PDF**: Best for publications (vector graphics)
- **SVG**: Editable vector graphics
- **HTML**: Interactive visualizations (Plotly, Bokeh)

**For Tables:**
- **CSV**: Machine-readable tables
- **Excel**: Formatted tables with multiple sheets
- **Markdown**: Human-readable tables in documentation
- **LaTeX**: Publication-ready tables

### 3. Save High-Quality Figures

**Python (Matplotlib):**
```python
import matplotlib.pyplot as plt
from pathlib import Path

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y)
ax.set_title('My Visualization')

# Save with high DPI
output_path = Path('results/figures/my_plot.png')
fig.savefig(output_path, dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print(f"Saved figure to {output_path}")

# Also save as PDF for publication
fig.savefig(output_path.with_suffix('.pdf'), bbox_inches='tight')
```

**Python (Seaborn):**
```python
import seaborn as sns

# Create plot
plot = sns.scatterplot(data=df, x='var1', y='var2', hue='category')
plot.figure.savefig('results/figures/scatter.png', dpi=300, bbox_inches='tight')
```

**R (ggplot2):**
```r
library(ggplot2)
library(here)

# Create plot
p <- ggplot(df, aes(x = var1, y = var2)) +
  geom_point() +
  theme_minimal()

# Save
ggsave(
  filename = here("results", "figures", "scatter.png"),
  plot = p,
  width = 10,
  height = 6,
  dpi = 300,
  bg = "white"
)

# Save as PDF
ggsave(here("results", "figures", "scatter.pdf"), p, width = 10, height = 6)
```

### 4. Save Results Tables

**Python:**
```python
import pandas as pd

# Create results
results = pd.DataFrame({
    'category': ['A', 'B', 'C'],
    'mean': [10.5, 12.3, 11.1],
    'std': [2.1, 1.8, 2.3]
})

# Save as CSV
results.to_csv('results/tables/summary_stats.csv', index=False)

# Save as formatted Excel
with pd.ExcelWriter('results/tables/summary_stats.xlsx') as writer:
    results.to_excel(writer, sheet_name='Summary', index=False)

# Save as Markdown (for documentation)
results.to_markdown('results/tables/summary_stats.md', index=False)
```

**R:**
```r
library(tidyverse)
library(here)

# Create results
results <- tibble(
  category = c('A', 'B', 'C'),
  mean = c(10.5, 12.3, 11.1),
  std = c(2.1, 1.8, 2.3)
)

# Save as CSV
write_csv(results, here("results", "tables", "summary_stats.csv"))

# Save as RDS (R-specific format, preserves data types)
saveRDS(results, here("results", "tables", "summary_stats.rds"))
```

### 5. Interactive Visualizations

**Python (Plotly):**
```python
import plotly.express as px

# Create interactive plot
fig = px.scatter(df, x='var1', y='var2', color='category',
                 title='Interactive Scatter Plot')

# Save as HTML
fig.write_html('results/figures/interactive/scatter_interactive.html')
```

**R (Plotly):**
```r
library(plotly)

# Create interactive plot
p <- plot_ly(df, x = ~var1, y = ~var2, color = ~category, type = 'scatter')

# Save as HTML
htmlwidgets::saveWidget(p, here("results", "figures", "interactive", "scatter.html"))
```

## Version Control

### Git Configuration

By default, results can be committed to git, but consider:

1. **Small files** (< 1 MB): Commit to repository
2. **Medium files** (1-10 MB): Consider if necessary
3. **Large files** (> 10 MB): 
   - Add to `.gitignore`
   - Store in external location
   - Ensure they can be regenerated from scripts

### .gitignore Example

```
# Exclude large result files
results/**/*.pdf
results/**/*.html
results/**/large_*

# But keep folder structure
!results/**/.gitkeep
```

## Documentation

### Figure Captions

Create a `figure_captions.md` file to document each figure:

```markdown
# Figure Captions

## Figure 1: Age Distribution
**File:** `figures/01_age_distribution.png`
**Description:** Histogram showing the distribution of participant ages. 
Sample size n=500. Mean age = 34.5 years (SD = 8.2).

## Figure 2: Income by Category
**File:** `figures/02_income_by_category.png`
**Description:** Box plots comparing income distributions across employment 
categories. ANOVA F(3,496) = 12.4, p < 0.001.
```

### Results Index

Create an `INDEX.md` file:

```markdown
# Results Index

Generated: 2026-01-05

## Figures

### Exploratory
- `figures/exploratory/01_age_dist.png` - Age distribution histogram
- `figures/exploratory/02_scatter.png` - X vs Y scatter plot

### Final
- `figures/final/figure1_main.png` - Main result (300 DPI, PNG)
- `figures/final/figure1_main.pdf` - Main result (vector, PDF)

## Tables
- `tables/descriptive_stats.csv` - Summary statistics for all variables
- `tables/regression_results.csv` - Model coefficients and p-values

## Models
- `models/trained_model.pkl` - Trained classification model
- `models/predictions.csv` - Model predictions on test set
```

## Reproducibility

All results should be reproducible from code. Document:

1. **Which script generated each output**
2. **When it was generated**
3. **Software versions used**

Add metadata in filenames or companion files:

```
figures/
├── scatter_plot_2026-01-05.png
└── scatter_plot_metadata.json
```

```json
{
  "file": "scatter_plot_2026-01-05.png",
  "generated_by": "scripts/03_create_visualizations.py",
  "generated_date": "2026-01-05",
  "input_data": "data/processed/analysis_ready.csv",
  "description": "Scatter plot of X vs Y with regression line",
  "software": {
    "python": "3.11.0",
    "matplotlib": "3.7.1",
    "seaborn": "0.12.2"
  }
}
```

## Quality Checklist

Before finalizing visualizations:

- [ ] High resolution (300 DPI for publications)
- [ ] Clear axis labels with units
- [ ] Readable font sizes
- [ ] Appropriate color schemes (colorblind-friendly)
- [ ] Legend if needed
- [ ] Title that explains what's shown
- [ ] Source data cited if applicable
- [ ] Saved in appropriate format(s)
- [ ] Documented in figure captions file

## Resources

- [Data Visualization Best Practices](https://clauswilke.com/dataviz/)
- [ColorBrewer (color schemes)](https://colorbrewer2.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [ggplot2 Gallery](https://r-graph-gallery.com/ggplot2-package.html)
