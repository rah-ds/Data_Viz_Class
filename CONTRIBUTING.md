# Contributing to SARC 5400 Data Visualization Projects

Thank you for contributing to this repository! This document provides guidelines for maintaining code quality and consistency.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Code Style Guidelines](#code-style-guidelines)
3. [Commit Message Guidelines](#commit-message-guidelines)
4. [Directory Structure](#directory-structure)
5. [Documentation Standards](#documentation-standards)
6. [Review Process](#review-process)

## Getting Started

### Prerequisites

- Git installed and configured
- Python 3.8+ or R 4.0+
- Familiarity with the repository structure (see main README.md)

### Setting Up Your Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rah-ds/Data_Viz_Class.git
   cd Data_Viz_Class
   ```

2. **Create a new branch for your work:**
   ```bash
   git checkout -b descriptive-branch-name
   ```

3. **Set up the environment:**
   ```bash
   # Python
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Or using conda
   conda env create -f environment.yml
   conda activate data-viz
   ```

## Code Style Guidelines

### Python

Follow [PEP 8](https://pep8.org/) style guide:

- Use 4 spaces for indentation (not tabs)
- Maximum line length: 88-100 characters (Black formatter default)
- Use meaningful variable names: `participant_count` not `pc`
- Add docstrings to functions and classes

**Good Example:**
```python
def calculate_summary_statistics(data: pd.DataFrame, column: str) -> dict:
    """
    Calculate summary statistics for a given column.
    
    Parameters
    ----------
    data : pd.DataFrame
        Input dataframe containing the data
    column : str
        Name of the column to analyze
        
    Returns
    -------
    dict
        Dictionary containing mean, median, std, min, max
        
    Examples
    --------
    >>> stats = calculate_summary_statistics(df, 'age')
    >>> print(stats['mean'])
    35.6
    """
    return {
        'mean': data[column].mean(),
        'median': data[column].median(),
        'std': data[column].std(),
        'min': data[column].min(),
        'max': data[column].max()
    }
```

**Formatting Tools:**
```bash
# Install formatting tools
pip install black flake8 isort

# Format code
black scripts/
isort scripts/

# Check style
flake8 scripts/
```

### R

Follow the [Tidyverse Style Guide](https://style.tidyverse.org/):

- Use `<-` for assignment, not `=`
- Use snake_case for variable names
- Add spaces around operators
- Use meaningful function names

**Good Example:**
```r
calculate_summary_statistics <- function(data, column) {
  #' Calculate Summary Statistics
  #'
  #' @param data A data frame containing the data
  #' @param column String name of the column to analyze
  #' @return A named list of summary statistics
  #' @examples
  #' stats <- calculate_summary_statistics(df, "age")
  #' print(stats$mean)
  
  list(
    mean = mean(data[[column]], na.rm = TRUE),
    median = median(data[[column]], na.rm = TRUE),
    sd = sd(data[[column]], na.rm = TRUE),
    min = min(data[[column]], na.rm = TRUE),
    max = max(data[[column]], na.rm = TRUE)
  )
}
```

**Formatting Tools:**
```r
# Install styler package
install.packages("styler")

# Format code
styler::style_dir("scripts")
```

### Data Visualization

Follow these principles for creating visualizations:

1. **Clear Labels:** Always label axes with units
2. **Readable Text:** Font size minimum 10pt for presentations, 8pt for papers
3. **Color Schemes:** Use colorblind-friendly palettes
4. **Titles:** Descriptive titles that explain what's shown
5. **Legends:** Place strategically; remove if redundant
6. **Accessibility:** Consider screen readers and alternative text

**Python Example (Matplotlib):**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Use colorblind-friendly palette
sns.set_palette("colorblind")

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x, y, alpha=0.6, s=100)
ax.set_xlabel('Variable X (units)', fontsize=12)
ax.set_ylabel('Variable Y (units)', fontsize=12)
ax.set_title('Clear Descriptive Title', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('results/figures/my_plot.png', dpi=300, bbox_inches='tight')
```

**R Example (ggplot2):**
```r
library(ggplot2)
library(viridis)  # Colorblind-friendly colors

ggplot(data, aes(x = var_x, y = var_y, color = category)) +
  geom_point(alpha = 0.6, size = 3) +
  scale_color_viridis_d() +
  labs(
    title = "Clear Descriptive Title",
    x = "Variable X (units)",
    y = "Variable Y (units)",
    color = "Category"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    legend.position = "bottom"
  )

ggsave("results/figures/my_plot.png", width = 10, height = 6, dpi = 300)
```

## Commit Message Guidelines

Write clear, descriptive commit messages:

### Format

```
<type>: <short summary> (max 50 chars)

<optional detailed description>

<optional footer>
```

### Types

- `feat`: New feature or analysis
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic change)
- `refactor`: Code restructuring (no behavior change)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

**Good:**
```
feat: add income distribution visualization

Created histogram and box plots to visualize income distribution
across demographic categories. Saved outputs to results/figures/.

Closes #42
```

**Also Good:**
```
fix: correct age filter in data cleaning script

Changed age filter from >= 18 to > 17 to include 18-year-olds.
Previous version incorrectly excluded valid participants.
```

**Bad:**
```
updated stuff
```

**Also Bad:**
```
fixed bug
```

## Directory Structure

Maintain the established directory structure:

```
.
├── data/
│   ├── raw/          # Original data (never modify)
│   └── processed/    # Cleaned data (reproducible from scripts)
├── scripts/          # Reusable code
├── notebooks/        # Exploratory analysis
├── results/          # Generated outputs
│   ├── figures/
│   └── tables/
├── docs/             # Documentation
└── tests/            # Unit tests (optional)
```

**Rules:**

1. **Never commit raw data without permission** (check with instructor)
2. **Never modify files in `data/raw/`** - create copies in `processed/`
3. **Keep scripts focused** - one script per major task
4. **Number scripts** to indicate execution order (01_, 02_, etc.)
5. **Document data sources** in `data/README.md` or `docs/`

## Documentation Standards

### Code Comments

- Explain **why**, not **what** (code shows what)
- Comment complex algorithms or non-obvious decisions
- Update comments when code changes

**Good:**
```python
# Use log transformation to handle right-skewed distribution
df['log_income'] = np.log1p(df['income'])
```

**Bad:**
```python
# Calculate log of income plus 1
df['log_income'] = np.log1p(df['income'])
```

### Docstrings

Use docstrings for all functions:

**Python (NumPy style):**
```python
def process_survey_data(filepath, remove_invalid=True):
    """
    Load and process survey data from CSV file.
    
    Parameters
    ----------
    filepath : str or Path
        Path to the CSV file containing survey data
    remove_invalid : bool, optional
        If True, remove responses that failed attention checks (default: True)
        
    Returns
    -------
    pd.DataFrame
        Processed survey data with invalid responses removed
        
    Raises
    ------
    FileNotFoundError
        If the specified file does not exist
    ValueError
        If the file is empty or missing required columns
        
    Examples
    --------
    >>> df = process_survey_data('data/raw/survey.csv')
    >>> print(len(df))
    456
    """
    # Implementation here
```

**R (roxygen2 style):**
```r
#' Process Survey Data
#'
#' Load and process survey data from CSV file.
#'
#' @param filepath Character string path to CSV file
#' @param remove_invalid Logical, if TRUE remove failed attention checks
#' @return A data frame with processed survey data
#' @examples
#' df <- process_survey_data("data/raw/survey.csv")
#' print(nrow(df))
#' @export
process_survey_data <- function(filepath, remove_invalid = TRUE) {
  # Implementation here
}
```

### README Files

Every subdirectory should have a README.md explaining:

- Purpose of the directory
- What files it contains
- How to use/run the code
- Any special considerations

## Review Process

### Before Submitting

1. **Test your code:**
   ```bash
   # Run your scripts
   python scripts/01_clean_data.py
   
   # Check for errors
   python -m pytest tests/  # If tests exist
   ```

2. **Check code style:**
   ```bash
   # Python
   black scripts/ --check
   flake8 scripts/
   
   # R
   # Run styler in RStudio
   ```

3. **Update documentation:**
   - Update README.md if structure changed
   - Add docstrings to new functions
   - Document new data sources

4. **Clean up:**
   ```bash
   # Remove temporary files
   find . -name "*.pyc" -delete
   find . -name "__pycache__" -delete
   find . -name ".DS_Store" -delete
   ```

### Pull Request Checklist

When submitting a pull request:

- [ ] Code follows style guidelines
- [ ] All scripts run without errors
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No sensitive data is committed
- [ ] Large files are excluded (use .gitignore)
- [ ] Results are reproducible

### Code Review

Code reviews focus on:

1. **Correctness:** Does the code do what it's supposed to?
2. **Clarity:** Is the code easy to understand?
3. **Reproducibility:** Can someone else run this?
4. **Style:** Does it follow our guidelines?
5. **Documentation:** Is it well-documented?

## Questions?

If you have questions:

1. Check the main [README.md](README.md)
2. Review the [reproducibility guide](docs/reproducibility.md)
3. Ask in class or office hours
4. Open a GitHub issue for repository-specific questions

## Additional Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [Tidyverse Style Guide](https://style.tidyverse.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Data Visualization Best Practices](https://clauswilke.com/dataviz/)
- [Reproducible Research in R](https://r4ds.had.co.nz/)

---

Thank you for contributing! Your attention to these guidelines helps maintain a high-quality, professional repository.
