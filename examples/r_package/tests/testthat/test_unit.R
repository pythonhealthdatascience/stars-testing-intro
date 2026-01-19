# Unit testing examples for import_patient_data


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


patrick::with_parameters_test_that(
  "incorrect columns cause import_patient_data() to fail",
  {
    # Create dataframe with incorrect columns
    df <- as.data.frame(as.list(seq_along(cols)))
    names(df) <- cols
    # Save as temporary CSV and run function, expecting an error
    csv_path <- tempfile(fileext = ".csv")
    readr::write_csv(df, csv_path)
    expect_error(import_patient_data(csv_path))
  },
  patrick::cases(
    # Example 1: Missing columns
    list(
      cols = c("PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME", "SERVICE_DATE")
    ),
    # Example 2: Extra columns
    list(
      cols = c(
        "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME", "SERVICE_DATE",
        "SERVICE_TIME", "EXTRA"
      )
    ),
    # Example 3: Right columns, wrong order
    list(
      cols = c(
        "ARRIVAL_DATE", "PATIENT_ID", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME"
      )
    )
  )
)


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
