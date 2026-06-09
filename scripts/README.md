# Visualization Scripts

This repository includes lightweight visualization scripts that do not depend on heavyweight plotting libraries.

## Scripts

- `generate_wordcloud.py`
  - reads paper titles from `data/paper-matrix.csv` and `README.md`
  - generates `assets/wordcloud.svg`
  - generates `assets/word_frequency.csv`

- `generate_visualizations.py`
  - reads `data/paper-matrix.csv`
  - generates `assets/category_distribution.svg`
  - generates `assets/year_distribution.svg`

## Usage

```bash
python3 scripts/generate_wordcloud.py
python3 scripts/generate_visualizations.py
```

Or regenerate everything in one shot:

```bash
python3 scripts/generate_all_visualizations.py
```
