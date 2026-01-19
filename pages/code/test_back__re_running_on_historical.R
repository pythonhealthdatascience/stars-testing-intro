test_that("re-running on historical data produces consistent results", {
  # Re-running on historical data should produce consistent results.

  # Specify path to historical data
  csv_path <- testthat::test_path("data", "patient_data.csv")

  # Run functions
  df <- import_patient_data(csv_path)
  df <- calculate_wait_times(df)
  stats <- summary_stats(df$waittime)

  # Verify the workflow produces consistent results
  expect_equal(stats$mean,     4.1666, tolerance = 1e-4)
  expect_equal(stats$std_dev,  2.7869, tolerance = 1e-4)
  expect_equal(stats$ci_lower, 1.2420, tolerance = 1e-4)
  expect_equal(stats$ci_upper, 7.0913, tolerance = 1e-4)
})
