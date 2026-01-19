test_that("small CSV with correct columns imports successfully", {
  expected_cols <- c(
    "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
    "SERVICE_DATE", "SERVICE_TIME"
  )

  # Create temporary CSV file
  df_in <- tibble::tibble(
    PATIENT_ID   = "p1",
    ARRIVAL_DATE = lubridate::ymd("2024-01-01"),
    ARRIVAL_TIME = hms::as_hms("08:00:00"),
    SERVICE_DATE = lubridate::ymd("2024-01-01"),
    SERVICE_TIME = hms::as_hms("09:00:00")
  )
  csv_path <- tempfile(fileext = ".csv")
  readr::write_csv(df_in, csv_path)

  # Run function and check it looks correct
  result <- import_patient_data(csv_path)
  expect_s3_class(result, "data.frame")
  expect_identical(names(result), expected_cols)
  expect_equal(as.data.frame(result), as.data.frame(df_in))
})
