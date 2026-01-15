def test_import_empty_csv(tmp_path):
    """Empty CSV with correct columns should succeed."""

    expected_cols = [
        "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME",
    ]

    # Create empty CSV with correct header
    df_in = pd.DataFrame(columns=expected_cols)
    csv_path = tmp_path / "patients.csv"
    df_in.to_csv(csv_path, index=False)

    # Should succeed and return empty DataFrame
    result = import_patient_data(csv_path)
    assert len(result) == 0
    assert list(result.columns) == expected_cols
