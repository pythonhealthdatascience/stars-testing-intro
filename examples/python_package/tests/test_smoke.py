"""
Smoke test.
"""

import pandas as pd

from waitingtimes.patient_analysis import (
    import_patient_data, calculate_wait_times, summary_stats
)


def test_smoke(tmp_path):
    """Smoke: end-to-end workflow produces the expected final output shape."""
    # Create test data
    test_data = pd.DataFrame(
        {
            "PATIENT_ID": ["p1", "p2", "p3"],
            "ARRIVAL_DATE": ["2024-01-01", "2024-01-01", "2024-01-02"],
            "ARRIVAL_TIME": ["0800", "0930", "1015"],
            "SERVICE_DATE": ["2024-01-01", "2024-01-01", "2024-01-02"],
            "SERVICE_TIME": ["0830", "1000", "1045"],
        }
    )

    # Write test CSV
    csv_path = tmp_path / "patients.csv"
    test_data.to_csv(csv_path, index=False)

    # Run complete workflow
    df = import_patient_data(csv_path)
    df = calculate_wait_times(df)
    stats = summary_stats(df["waittime"])

    # Final check
    assert stats is not None
