def test_real_data_file():
    """Importing a real data file to a test"""

    # Path to example test data
    csv_path = Path(__file__).parent.joinpath("data/patient_data.csv")

    # Load the data and check it was read
    df = import_patient_data(csv_path)
    assert not df.empty
