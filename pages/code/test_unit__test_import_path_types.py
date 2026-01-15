def test_import_path_types(tmp_path):
    """str and Path inputs should behave identically."""
    # Create temporary CSV file
    expected_cols = [
        "PATIENT_ID",
        "ARRIVAL_DATE", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME",
    ]
    df_in = pd.DataFrame(
        [["p1", "2024-01-01", "08:00", "2024-01-01", "09:00"]],
        columns=expected_cols,
    )
    csv_path = tmp_path / "patients.csv"
    df_in.to_csv(csv_path, index=False)

    # Run function with str or Path inputs
    df_str = import_patient_data(str(csv_path))
    df_path = import_patient_data(csv_path)

    # Check that results are the same
    pd.testing.assert_frame_equal(df_str, df_path)
