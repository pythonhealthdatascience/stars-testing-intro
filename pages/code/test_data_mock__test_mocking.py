def test_mocking(monkeypatch):
    """Providing data to a test via mocking"""

    # Create sample patient data
    testdata = pd.DataFrame(
        [["p1", "2024-01-01", "08:00", "2024-01-01", "09:00"]],
        columns=[
            "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
            "SERVICE_DATE", "SERVICE_TIME",
        ],
    )

    # Define a fake CSV reader that just returns our DataFrame
    def mock_read_csv(path):
        return testdata

    # Temporarily replace pd.read_csv with our fake version
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    # Call the function with any path - it does not matter - it will use the
    # mocked reader, and pd.read_csv is never actually called
    df = import_patient_data("does_not_matter.csv")
    assert not df.empty
