# SARC 5400 - Data Visualization

**University of Virginia, 2026**

This repository serves as a structured workspace for the SARC 5400 Data Visualization course at UVA. It follows best practices for reproducible research and provides a template for organizing data visualization projects.

## Course Information

- **Course:** SARC 5400 - Data Visualization
- **Institution:** University of Virginia
- **Syllabus:** [https://web.arch.virginia.edu/arch547/syllabus.html](https://web.arch.virginia.edu/arch547/syllabus.html)

## Repository Purpose

This repository is designed to:
- Provide a structured environment for data visualization assignments and projects
- Demonstrate best practices for reproducible research
- Organize code, data, and outputs in a clear, maintainable way
- Serve as a template for future data science and visualization projects

## Repository Structure

```bash
.
├── data/               # Data files
│   ├── raw/           # Original, immutable data
│   └── processed/     # Cleaned and processed data
├── scripts/           # Analysis and visualization scripts
├── notebooks/         # Jupyter notebooks and R Markdown files
├── results/           # Generated visualizations and outputs
├── docs/              # Documentation and reports
├── requirements.txt   # Python dependencies
├── environment.yml    # Conda environment specification
└── README.md          # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8+ or R 4.0+
- Git
- (Optional) Anaconda/Miniconda for environment management

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rah-ds/Data_Viz_Class.git
   cd Data_Viz_Class
   ```

2. **Set up Python environment (Option 1 - pip):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Python environment (Option 2 - conda):**
   ```bash
   conda env create -f environment.yml
   conda activate data-viz
   ```

4. **Verify installation:**
   ```bash
   python --version
   pip list
   ```

## How to Use This Repository

### For Course Assignments

1. Create a new branch for each assignment:
   ```bash
   git checkout -b assignment-name
   ```

2. Place raw data in `data/raw/`
3. Write analysis scripts in `scripts/` or work in `notebooks/`
4. Save processed data to `data/processed/`
5. Export visualizations to `results/`
6. Document your work in `docs/`

### For Projects

1. Follow the same structure as assignments
2. Include a project-specific README in the project folder
3. Document your methodology in `docs/`
4. Keep track of data sources and citations

### Best Practices

- Never modify raw data; always work with copies in `processed/`
- Write clear, commented code
- Use meaningful file names and variable names
- Document data sources and transformations
- Commit regularly with descriptive messages
- Review `CONTRIBUTING.md` for detailed guidelines

## Documentation

- [Contributing Guidelines](CONTRIBUTING.md)
- [Reproducibility Guide](docs/reproducibility.md)
- [License](LICENSE)

## Resources

- Course Syllabus: https://web.arch.virginia.edu/arch547/syllabus.html
- UVA Library Data Services: https://data.library.virginia.edu/
- Data Visualization Best Practices: See course materials

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- SARC 5400 Data Visualization Course, University of Virginia
- Course instructors and teaching assistants
- Contributing students and researchers

## Contact

For questions about this repository or the course, please refer to the course syllabus or contact through Canvas.