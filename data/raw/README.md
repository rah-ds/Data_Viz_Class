# Raw Data

This directory contains original, unmodified data files.

## Important Guidelines

⚠️ **NEVER MODIFY FILES IN THIS DIRECTORY**

- This directory should contain only original data as received
- Keep data in its original format
- If you need to work with the data, make a copy in `../processed/`

## What to Include

- Original datasets downloaded from sources
- Survey responses in their raw form
- Scraped data files
- Database exports
- Metadata files (data dictionaries, codebooks, README files from data sources)

## Documentation

For each dataset, document:
1. **Source:** Where the data came from (URL, database, etc.)
2. **Date acquired:** When you obtained the data
3. **License:** Terms of use
4. **Description:** Brief description of what the data contains
5. **Format:** File format and any special considerations

Create a `sources.md` file in this directory or document in the main `docs/` folder.

## Example

```
raw/
├── census_data_2020.csv          # US Census data
├── census_data_2020_codebook.pdf # Variable descriptions
└── sources.md                     # Documentation of data sources
```
