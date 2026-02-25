test_that("smoke: end-to-end workflow produces some output", {
  # Create small, fast test data
  test_data <- data.frame(
    PATIENT_ID   = c("p1", "p2", "p3"),
    ARRIVAL_DATE = c("2024-01-01", "2024-01-01", "2024-01-02"),
    ARRIVAL_TIME = c("0800", "0930", "1015"),
    SERVICE_DATE = c("2024-01-01", "2024-01-01", "2024-01-02"),
    SERVICE_TIME = c("0830", "1000", "1045"),
    stringsAsFactors = FALSE
  )

  # Write test CSV to a temporary file
  csv_path <- tempfile(fileext = ".csv")
  utils::write.csv(test_data, csv_path, row.names = FALSE)

  # Run complete workflow
  df <- import_patient_data(csv_path)
  df <- calculate_wait_times(df)
  stats <- summary_stats(df$waittime)

  # Final smoke-test check: did we get *any* result?
  expect_false(is.null(stats))
})
