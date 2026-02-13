def calculate_wait_times(df):
    """
    Add arrival/service datetimes and waiting time in minutes.

    Parameters
    ----------
    df : pandas.DataFrame
        Patient-level data containing `ARRIVAL_DATE`, `ARRIVAL_TIME`,
        `SERVICE_DATE`, and `SERVICE_TIME` columns.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame with additional columns:
        `arrival_datetime`, `service_datetime`, and `waittime`.

    Raises#<<
    ------#<<
    TypeError#<<
        If `df` is not a pandas DataFrame.#<<
    ValueError#<<
        If required columns (`ARRIVAL_DATE`, `ARRIVAL_TIME`,#<<
        `SERVICE_DATE`, `SERVICE_TIME`) are missing from the DataFrame.#<<

    Warns#<<
    -----#<<
    UserWarning#<<
        If the input DataFrame is empty.#<<
    """
    # Check `df` is a dataframe. Hard fail using exception.#<<
    if not isinstance(df, pd.DataFrame):#<<
        raise TypeError(f"Expected pandas DataFrame, got {type(df).__name__}")#<<

    # Check required columns are provided. Hard fail using exception.#<<
    required_cols = ["ARRIVAL_DATE", "ARRIVAL_TIME",#<<
                     "SERVICE_DATE", "SERVICE_TIME"]#<<
    missing_cols = [col for col in required_cols if col not in df.columns]#<<
    if missing_cols:#<<
        raise ValueError(f"Missing required columns: {missing_cols}")#<<

    # Check if dataframe is empty. Graceful fail return early + raise warning#<<
    if df.empty:#<<
        df = df.copy()#<<
        warnings.warn("Input DataFrame is empty; returning empty result with expected columns")#<<
        df["arrival_datetime"] = pd.Series(dtype='datetime64[ns]')#<<
        df["service_datetime"] = pd.Series(dtype='datetime64[ns]')#<<
        df["waittime"] = pd.Series(dtype='float64')#<<
        return df#<<

    df = df.copy()

    # Combine date and time columns into datetime columns
    for prefix in ("ARRIVAL", "SERVICE"):
        df[f"{prefix.lower()}_datetime"] = pd.to_datetime(
            df[f"{prefix}_DATE"].astype(str) +
            " " +
            df[f"{prefix}_TIME"].astype(str).str.zfill(4),
            format="%Y-%m-%d %H%M"
        )

    # Waiting time in minutes
    df["waittime"] = (
        df["service_datetime"] - df["arrival_datetime"]
    ) / pd.Timedelta(minutes=1)

    return df
