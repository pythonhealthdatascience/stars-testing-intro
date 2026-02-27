def test_temporary_file(tmp_path):
    """Providing data to a test via a temporary file"""

    # Create sample patient data
    testdata = pd.DataFrame(
        [["p1", "2024-01-01", "08:00", "2024-01-01", "09:00"]],
        columns=[
            "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
            "SERVICE_DATE", "SERVICE_TIME",
        ],
    )

    # Create a temporary CSV file
    csv_path = tmp_path / "patients.csv"
    testdata.to_csv(csv_path, index=False)

    # Load the data and check it was read
    df = import_patient_data(csv_path)
    assert not df.empty
