"""
Introduction to test: simple test of summary_stats
"""

import pandas as pd

from waitingtimes.patient_analysis import summary_stats


def test_summary_stats_single_value():
    """Running summary_stats on a single value should only return mean."""
    data = pd.Series([10])
    mean, std, ci_lower, ci_upper = summary_stats(data)
    assert mean == 10
    assert pd.isna(std)
    assert pd.isna(ci_lower)
    assert pd.isna(ci_upper)
