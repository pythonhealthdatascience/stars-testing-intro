"""
Unit testing examples for import_patient_data.
"""

import pandas as pd
import pytest

from waitingtimes.patient_analysis import import_patient_data


def test_import_success(monkeypatch):
    """Small CSV with correct columns should work."""

    # Create sample patient data
    expected_cols = [
        "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME",
    ]
    testdata = pd.DataFrame(
        [["p1", "2024-01-01", "08:00", "2024-01-01", "09:00"]],
        columns=expected_cols,
    )

    # Call function (with mocking for pd.read_csv())
    def mock_read_csv(*args, **kwargs):
        return testdata
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)
    result = import_patient_data("path.csv")

    # Check the result looks correct
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == expected_cols
    pd.testing.assert_frame_equal(result, testdata)


@pytest.mark.parametrize(
    "columns",
    [
        # Example 1: Missing columns
        [
            "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME", "SERVICE_DATE"
        ],
        # Example 2: Extra columns
        [
            "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
            "SERVICE_DATE", "SERVICE_TIME", "EXTRA",
        ],
        # Example 3: Right columns, wrong order
        [
            "ARRIVAL_DATE", "PATIENT_ID", "ARRIVAL_TIME",
            "SERVICE_DATE", "SERVICE_TIME",
        ],
    ],
)
def test_import_errors(monkeypatch, columns):
    """Incorrect columns should trigger ValueError."""

    # Create sample patient data
    testdata = pd.DataFrame([range(len(columns))], columns=columns)

    # Call function (with mocking for pd.read_csv()), should raise an error
    def mock_read_csv(*args, **kwargs):
        return testdata
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)
    with pytest.raises(ValueError):
        import_patient_data("path.csv")


def test_import_empty_csv(monkeypatch):
    """Empty CSV with correct columns should succeed."""

    # Create empty CSV with correct header
    expected_cols = [
        "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME",
    ]
    testdata = pd.DataFrame(columns=expected_cols)

    # Call function (with mocking for pd.read_csv())
    def mock_read_csv(*args, **kwargs):
        return testdata
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)
    result = import_patient_data("path.csv")

    # Should succeed and return an empty dataframe
    assert len(result) == 0
    assert list(result.columns) == expected_cols


def test_import_path_types(tmp_path):
    """str and Path inputs should behave identically."""
    # Create sample patient data
    expected_cols = [
        "PATIENT_ID",
        "ARRIVAL_DATE", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME",
    ]
    df_in = pd.DataFrame(
        [["p1", "2024-01-01", "08:00", "2024-01-01", "09:00"]],
        columns=expected_cols,
    )

    # Create temporary file (not mocking, as this is about checking
    # pd.read_csv is working as expected)
    csv_path = tmp_path / "patients.csv"
    df_in.to_csv(csv_path, index=False)

    # Run function with str or Path inputs
    df_str = import_patient_data(str(csv_path))
    df_path = import_patient_data(csv_path)

    # Check that results are the same
    pd.testing.assert_frame_equal(df_str, df_path)
