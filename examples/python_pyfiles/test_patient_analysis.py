"""
Introduction to testing: simple test of summary_stats
"""

import pandas as pd

from patient_analysis import summary_stats


def test_summary_stats_single_value():
    """Running summary_stats on a single value should only return mean."""
    data = pd.Series([10])
    res = summary_stats(data)
    assert res["mean"] == 10
    assert pd.isna(res["std_dev"])
    assert pd.isna(res["ci_lower"])
    assert pd.isna(res["ci_upper"])
