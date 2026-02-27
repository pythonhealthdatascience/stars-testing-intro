def test_reproduction():
    """Re-running on historical data should produce consistent results."""
    # Specify path to historical data
    csv_path = Path(__file__).parent.joinpath("data/patient_data.csv")

    # Run functions
    df = import_patient_data(csv_path)
    df = calculate_wait_times(df)
    stats = summary_stats(df["waittime"])

    # Verify the workflow produces consistent results
    assert np.isclose(stats["mean"], 4.1666, rtol=0.0001)
    assert np.isclose(stats["std_dev"], 2.7869, rtol=0.0001)
    assert np.isclose(stats["ci_lower"], 1.2420, rtol=0.0001)
    assert np.isclose(stats["ci_upper"], 7.0913, rtol=0.0001)
