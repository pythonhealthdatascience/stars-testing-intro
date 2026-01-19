test_that("workflow should correctly compute statistics for variable wait times", {
  # Workflow should correctly compute statistics for variable wait times.

  # Create test data with known wait times: 15, 30, 45 minutes
  test_data <- tibble::tibble(
    PATIENT_ID   = c("p1", "p2", "p3"),
    ARRIVAL_DATE = c("2024-01-01", "2024-01-01", "2024-01-01"),
    ARRIVAL_TIME = c("0800", "0900", "1000"),
    SERVICE_DATE = c("2024-01-01", "2024-01-01", "2024-01-01"),
    SERVICE_TIME = c("0815", "0930", "1045")
  )

  csv_path <- tempfile(fileext = ".csv")
  readr::write_csv(test_data, csv_path)

  # Run complete workflow
  df <- import_patient_data(csv_path)
  df <- calculate_wait_times(df)
  stats <- summary_stats(df$waittime)

  # Verify mean and standard deviation
  expect_identical(stats$mean, 30)
  expect_equal(stats$std_dev, 15, tolerance = 1e-8)

  # CI should be symmetric around mean for this small sample
  expect_lt(stats$ci_lower, stats$mean)
  expect_gt(stats$ci_upper, stats$mean)
})
