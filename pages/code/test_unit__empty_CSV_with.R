test_that("empty CSV with correct columns should succeed", {
  # Empty CSV with correct columns should succeed.

  expected_cols <- c(
    "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
    "SERVICE_DATE", "SERVICE_TIME"
  )

  # Create empty CSV with correct header
  df_in <- tibble::tibble(
    PATIENT_ID   = character(),
    ARRIVAL_DATE = character(),
    ARRIVAL_TIME = character(),
    SERVICE_DATE = character(),
    SERVICE_TIME = character()
  )
  csv_path <- tempfile(fileext = ".csv")
  readr::write_csv(df_in, csv_path)

  # Should succeed and return empty data frame
  result <- import_patient_data(csv_path)
  expect_identical(nrow(result), 0L)
  expect_identical(names(result), expected_cols)
})
