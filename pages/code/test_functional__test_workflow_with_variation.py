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
