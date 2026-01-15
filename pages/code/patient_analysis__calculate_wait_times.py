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
    """
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
