@pytest.mark.parametrize(
    "columns",
    [
        # Example 1: Missing columns
        [
            "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME", "SERVICE_DATE"
        ],
        # Example 2: Extra columns
        [
            "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
            "SERVICE_DATE", "SERVICE_TIME", "EXTRA",
        ],
        # Example 3: Right columns, wrong order
        [
            "ARRIVAL_DATE", "PATIENT_ID", "ARRIVAL_TIME",
            "SERVICE_DATE", "SERVICE_TIME",
        ],
    ],
)
def test_import_errors(monkeypatch, columns):
    """Incorrect columns should trigger ValueError."""

    # Create sample patient data
    testdata = pd.DataFrame([range(len(columns))], columns=columns)

    # Call function (with mocking for pd.read_csv()), should raise an error
    def mock_read_csv(*args, **kwargs):
        return testdata
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)
    with pytest.raises(ValueError):
        import_patient_data("path.csv")
