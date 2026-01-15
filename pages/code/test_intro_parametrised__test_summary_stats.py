def test_summary_stats(
    data, expected_mean, expected_std, expected_ci_lower, expected_ci_upper
):
    """Running summary_stats returns expected values."""
    res = summary_stats(pd.Series(data))
    assert res["mean"] == pytest.approx(expected_mean, rel=5e-3)
    assert res["std_dev"] == pytest.approx(expected_std, rel=5e-3)
    assert res["ci_lower"] == pytest.approx(expected_ci_lower, rel=5e-3)
    assert res["ci_upper"] == pytest.approx(expected_ci_upper, rel=5e-3)
