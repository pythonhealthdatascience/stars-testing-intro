def test_import_errors(tmp_path, columns):
    """Incorrect columns should trigger ValueError."""

    # Create temporary CSV file
    df_in = pd.DataFrame([range(len(columns))], columns=columns)
    csv_path = tmp_path / "patients.csv"
    df_in.to_csv(csv_path, index=False)

    # Check it raises ValueError
    with pytest.raises(ValueError):
        import_patient_data(csv_path)
