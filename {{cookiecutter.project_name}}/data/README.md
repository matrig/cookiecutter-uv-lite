# Data Directory

Store your datasets here.

## Structure

- `raw/`: Original, immutable data
- `processed/`: Cleaned, transformed data ready for analysis
- `external/`: Data from third-party sources

## `.gitignore`

Large data files are git-ignored by default. Use Git LFS or external storage for big datasets.

## Loading Data in Notebooks

```python
import pandas as pd
from pathlib import Path

# Example: Load data from this directory
data_dir = Path("../data")
df = pd.read_csv(data_dir / "raw" / "dataset.csv")
```
