"""
Functions to import, process, and summarise patient waiting time data.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st


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


def summary_stats(data):
    """
    Calculate mean, standard deviation and 95% confidence interval (CI).

    CI is calculated using the t-distribution, which is appropriate for
    small samples and converges to the normal distribution as the sample
    size increases.

    Parameters
    ----------
    data : pandas.Series
        Data to use in the calculation.

    Returns
    -------
    dict[str, float]
        A dictionary with keys `mean`, `std_dev`, `ci_lower` and `ci_upper`.
        Each value is a float, or `numpy.nan` if it can't be computed.
    """
    # Drop missing values
    data = data.dropna()

    # Find number of observations
    count = len(data)

    # If there are no observations, then set all to NaN
    if count == 0:
        mean, std_dev, ci_lower, ci_upper = np.nan, np.nan, np.nan, np.nan

    # If there are 1 or 2 observations, can do mean but not other statistics
    elif count < 3:
        mean = data.mean()
        std_dev, ci_lower, ci_upper = np.nan, np.nan, np.nan

    # With more than two observations, can calculate all...
    else:
        mean = data.mean()
        std_dev = data.std()

        # If there is no variation, then CI is equal to the mean
        if np.var(data) == 0:
            ci_lower, ci_upper = mean, mean
        else:
            # 95% CI based on the t-distribution
            ci_lower, ci_upper = st.t.interval(
                confidence=0.95,
                df=count-1,
                loc=mean,
                scale=st.sem(data)
            )

    return {
        "mean": mean,
        "std_dev": std_dev,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper
    }
