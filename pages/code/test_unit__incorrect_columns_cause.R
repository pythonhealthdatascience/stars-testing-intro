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
