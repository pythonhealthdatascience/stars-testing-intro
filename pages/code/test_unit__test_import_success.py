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
