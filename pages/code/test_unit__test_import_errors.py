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
def test_import_errors(tmp_path, columns):
    """Incorrect columns should trigger ValueError."""

    # Create temporary CSV file
    df_in = pd.DataFrame([range(len(columns))], columns=columns)
    csv_path = tmp_path / "patients.csv"
    df_in.to_csv(csv_path, index=False)

    # Check it raises ValueError
    with pytest.raises(ValueError):
        import_patient_data(csv_path)
