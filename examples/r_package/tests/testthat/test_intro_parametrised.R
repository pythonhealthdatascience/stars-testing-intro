# Introduction to testing: parametrised test of summary_stats


patrick::with_parameters_test_that(
  "summary_stats returns expected values",
  {
    res <- summary_stats(data)

    expect_equal(res$mean, expected_mean, tolerance = 5e-3)
    expect_equal(res$std_dev, expected_std, tolerance = 5e-3)
    expect_equal(res$ci_lower, expected_ci_lower, tolerance = 5e-3)
    expect_equal(res$ci_upper, expected_ci_upper, tolerance = 5e-3)
  },
  patrick::cases(
    # Five value sample with known summary statistics
    list(
      data = c(1.0, 2.0, 3.0, 4.0, 5.0),
      expected_mean = 3.0,
      expected_std = 1.58,
      expected_ci_lower = 1.04,
      expected_ci_upper = 4.96
    ),
    # No variation: CI collapse to mean
    list(
      data = c(5, 5, 5),
      expected_mean = 5,
      expected_std = 0,
      expected_ci_lower = 5,
      expected_ci_upper = 5
    )
  )
)
