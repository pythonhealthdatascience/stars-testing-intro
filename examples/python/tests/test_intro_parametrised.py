"""
Introduction to test: parametrised test of summary_stats
"""

import pandas as pd
import pytest

from waitingtimes.patient_analysis import summary_stats


@pytest.mark.parametrize(
    "data, expected_mean, expected_std, expected_ci_lower, expected_ci_upper",
    [
        # Five value sample with known summary statistics
        ([1.0, 2.0, 3.0, 4.0, 5.0], 3.0, 1.58, 1.04, 4.96),
        # No variation: CI collapse to mean
        ([5, 5, 5], 5, 0, 5, 5),
    ],
)
def test_summary_stats(
    data, expected_mean, expected_std, expected_ci_lower, expected_ci_upper
):
    """Running summary_stats returns expected values."""
    mean, std, ci_lower, ci_upper = summary_stats(pd.Series(data))
    assert mean == pytest.approx(expected_mean, rel=5e-3)
    assert std == pytest.approx(expected_std, rel=5e-3)
    assert ci_lower == pytest.approx(expected_ci_lower, rel=5e-3)
    assert ci_upper == pytest.approx(expected_ci_upper, rel=5e-3)
