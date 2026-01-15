def import_patient_data(path):
    """
    Import raw patient data and check that required columns are present.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV file containing the patient data.

    Returns
    -------
    pandas.DataFrame
        Dataframe containing the raw patient-level data.

    Raises
    ------
    ValueError
        If the CSV file does not contain exactly the expected columns
        in the expected order.
    """
    df = pd.read_csv(Path(path))

    # Expected columns in the raw data (names and order must match)
    expected = [
        "PATIENT_ID",
        "ARRIVAL_DATE", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME"
    ]
    if list(df.columns) != expected:
        raise ValueError(
            f"Unexpected columns: {list(df.columns)} (expected {expected})"
        )

    return df
