test_that("complete workflow should calculate correct wait statistics", {

  # Create test data with known values
  test_data <- tibble::tibble(
    PATIENT_ID   = c("p1", "p2", "p3"),
    ARRIVAL_DATE = c("2024-01-01", "2024-01-01", "2024-01-02"),
    ARRIVAL_TIME = c("0800", "0930", "1015"),
    SERVICE_DATE = c("2024-01-01", "2024-01-01", "2024-01-02"),
    SERVICE_TIME = c("0830", "1000", "1045")
  )

  # Write test CSV
  csv_path <- tempfile(fileext = ".csv")
  readr::write_csv(test_data, csv_path)

  # Run complete workflow
  df <- import_patient_data(csv_path)
  df <- calculate_wait_times(df)
  stats <- summary_stats(df$waittime)

  # Verify the workflow produces correct results
  # Expected wait times: 30, 30, 30 minutes
  expect_identical(stats$mean, 30)
  expect_identical(stats$std_dev, 0)
  expect_identical(stats$ci_lower, 30)
  expect_identical(stats$ci_upper, 30)
})
