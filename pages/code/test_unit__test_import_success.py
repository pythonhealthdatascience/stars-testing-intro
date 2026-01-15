def test_import_success(tmp_path):
    """Small CSV with correct columns should work."""

    expected_cols = [
        "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME",
    ]

    # Create temporary CSV file
    df_in = pd.DataFrame(
        [["p1", "2024-01-01", "08:00", "2024-01-01", "09:00"]],
        columns=expected_cols,
    )
    csv_path = tmp_path / "patients.csv"
    df_in.to_csv(csv_path, index=False)

    # Run function and check it looks correct
    result = import_patient_data(csv_path)
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == expected_cols
    pd.testing.assert_frame_equal(result, df_in)
