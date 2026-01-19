test_that("workflow should raise error when dates are missing", {
  # Workflow should raise error when dates are missing.

  test_data <- tibble::tibble(
    PATIENT_ID   = c("p1", "p2", "p3"),
    ARRIVAL_DATE = c("2024-01-01", "2024-01-01", "2024-01-01"),
    ARRIVAL_TIME = c("0800", "0900", "1000"),
    SERVICE_DATE = c("2024-01-01", NA, "2024-01-01"),
    SERVICE_TIME = c("0830", "1000", "1045")
  )

  csv_path <- tempfile(fileext = ".csv")
  readr::write_csv(test_data, csv_path)

  # Workflow should fail when calculating wait times with missing dates
  # Will also have warning from ymd_hm() about returning NA
  df <- import_patient_data(csv_path)
  expect_warning(
    expect_error(
        calculate_wait_times(df),
        regexp = "Failed to parse arrival or service datetimes"
    ),
    regexp = "failed to parse"
  )
})
