test_that("providing data to a test via mocking", {
  testdata <- tibble::tibble(
    PATIENT_ID   = "p1",
    ARRIVAL_DATE = lubridate::ymd("2024-01-01"),
    ARRIVAL_TIME = hms::as_hms("08:00:00"),
    SERVICE_DATE = lubridate::ymd("2024-01-01"),
    SERVICE_TIME = hms::as_hms("09:00:00")
  )

  testthat::local_mocked_bindings(
    read_csv = function(path, show_col_types = FALSE) testdata,
    .package = "waitingtimes"
  )

  df <- import_patient_data("does_not_matter.csv")
  expect_gt(nrow(df), 0)
})
