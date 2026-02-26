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
