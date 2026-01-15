"""
Functional testing.
"""

import numpy as np
import pandas as pd
import pytest

from waitingtimes.patient_analysis import (
    import_patient_data, calculate_wait_times, summary_stats
)


def test_workflow_success(tmp_path):
    """Complete workflow should calculate correct wait statistics."""

    # Create test data with known values
    test_data = pd.DataFrame({
        "PATIENT_ID": ["p1", "p2", "p3"],
        "ARRIVAL_DATE": ["2024-01-01", "2024-01-01", "2024-01-02"],
        "ARRIVAL_TIME": ["0800", "0930", "1015"],
        "SERVICE_DATE": ["2024-01-01", "2024-01-01", "2024-01-02"],
        "SERVICE_TIME": ["0830", "1000", "1045"],
    })

    # Write test CSV
    csv_path = tmp_path / "patients.csv"
    test_data.to_csv(csv_path, index=False)

    # Run complete workflow
    df = import_patient_data(csv_path)
    df = calculate_wait_times(df)
    stats = summary_stats(df["waittime"])

    # Verify the workflow produces correct results
    # Expected wait times: 30, 30, 30 minutes
    assert stats["mean"] == 30.0
    assert stats["std_dev"] == 0.0
    assert stats["ci_lower"] == 30.0
    assert stats["ci_upper"] == 30.0


def test_workflow_with_variation(tmp_path):
    """Workflow should correctly compute statistics for variable wait times."""

    # Create test data with known wait times: 15, 30, 45 minutes
    test_data = pd.DataFrame({
        "PATIENT_ID": ["p1", "p2", "p3"],
        "ARRIVAL_DATE": ["2024-01-01", "2024-01-01", "2024-01-01"],
        "ARRIVAL_TIME": ["0800", "0900", "1000"],
        "SERVICE_DATE": ["2024-01-01", "2024-01-01", "2024-01-01"],
        "SERVICE_TIME": ["0815", "0930", "1045"],
    })

    csv_path = tmp_path / "patients.csv"
    test_data.to_csv(csv_path, index=False)

    # Run complete workflow
    df = import_patient_data(csv_path)
    df = calculate_wait_times(df)
    stats = summary_stats(df["waittime"])

    # Verify mean and standard deviation
    assert stats["mean"] == 30
    assert np.isclose(stats["std_dev"], 15)

    # CI should be symmetric around mean for this small sample
    assert stats["ci_lower"] < stats["mean"] < stats["ci_upper"]


def test_missing_date_error(tmp_path):
    """Workflow should raise error when dates are missing."""

    test_data = pd.DataFrame({
        "PATIENT_ID": ["p1", "p2", "p3"],
        "ARRIVAL_DATE": ["2024-01-01", "2024-01-01", "2024-01-01"],
        "ARRIVAL_TIME": ["0800", "0900", "1000"],
        "SERVICE_DATE": ["2024-01-01", pd.NaT, "2024-01-01"],
        "SERVICE_TIME": ["0830", "1000", "1045"],
    })

    csv_path = tmp_path / "patients.csv"
    test_data.to_csv(csv_path, index=False)

    # Workflow should fail when calculating wait times with missing dates
    df = import_patient_data(csv_path)
    with pytest.raises(ValueError, match="time data"):
        df = calculate_wait_times(df)
