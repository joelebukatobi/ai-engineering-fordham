"""Helper functions for AI Engineering homeworks."""

import pandas as pd
from pathlib import Path


def load_wands_products(data_dir: str = "data") -> pd.DataFrame:
    """
    Load WANDS products from local file.

    Args:
        data_dir: Path to the data directory containing wayfair-products.csv

    Returns:
        DataFrame with product information including product_id, product_name,
        product_class, category_hierarchy, product_description, etc.
    """
    filepath = Path(data_dir) / "wayfair-products.csv"
    products = pd.read_csv(filepath, sep='\t')
    products = products.rename(columns={'category hierarchy': 'category_hierarchy'})
    return products


def load_wands_queries(data_dir: str = "data") -> pd.DataFrame:
    """
    Load WANDS queries from local file.

    Args:
        data_dir: Path to the data directory containing wayfair-queries.csv

    Returns:
        DataFrame with query_id and query columns
    """
    filepath = Path(data_dir) / "wayfair-queries.csv"
    queries = pd.read_csv(filepath, sep='\t')
    return queries


def load_wands_labels(data_dir: str = "data") -> pd.DataFrame:
    """
    Load WANDS relevance labels from local file.

    Args:
        data_dir: Path to the data directory containing wayfair-labels.csv

    Returns:
        DataFrame with query_id, product_id, label (Exact/Partial/Irrelevant),
        and grade (2/1/0) columns
    """
    filepath = Path(data_dir) / "wayfair-labels.csv"
    labels = pd.read_csv(filepath, sep='\t')
    grade_map = {'Exact': 2, 'Partial': 1, 'Irrelevant': 0}
    labels['grade'] = labels['label'].map(grade_map)
    return labels
