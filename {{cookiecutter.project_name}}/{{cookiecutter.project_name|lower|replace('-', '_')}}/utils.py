"""Utility functions for data analysis.

{% if cookiecutter.project_type == 'notebooks' -%}
This module provides helper functions for use in Jupyter notebooks.
{%- endif %}
"""

from __future__ import annotations

{% if cookiecutter.project_type == 'notebooks' -%}
import pandas as pd


def load_sample_data() -> pd.DataFrame:
    """Load sample dataset for exploration.

    Returns:
        DataFrame with sample data including x, y, and category columns.

    Example:
        >>> df = load_sample_data()
        >>> df.shape
        (10, 3)
    """
    # Create sample data
    return pd.DataFrame(
        {"x": range(10), "y": [i**2 for i in range(10)], "category": ["A", "B"] * 5}
    )


def setup_plotting_style() -> None:
    """Configure matplotlib/seaborn for better-looking plots.

    This function sets up a clean, professional plotting style with:
    - White grid background
    - Husl color palette
    - Larger default figure size
    - Readable font size

    Example:
        >>> setup_plotting_style()
        >>> # Now all plots will use the configured style
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_style("whitegrid")
    sns.set_palette("husl")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["font.size"] = 11
{%- endif %}
