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
