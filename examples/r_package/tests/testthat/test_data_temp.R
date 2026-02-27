# Using temporary file to provide CSV to a test


test_that("tempfile is created and read by import_patient_data", {

  # Create temporary CSV file
  testdata <- tibble::tibble(
    PATIENT_ID   = "p1",
    ARRIVAL_DATE = lubridate::ymd("2024-01-01"),
    ARRIVAL_TIME = hms::as_hms("08:00:00"),
    SERVICE_DATE = lubridate::ymd("2024-01-01"),
    SERVICE_TIME = hms::as_hms("09:00:00")
  )
  csv_path <- tempfile(fileext = ".csv")
  readr::write_csv(testdata, csv_path)

  # Load the data and check it was read
  df <- import_patient_data(csv_path)
  expect_gt(nrow(df), 0)
})