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
