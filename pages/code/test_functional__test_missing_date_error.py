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
