# Importing a real data file to a test

test_that("real data file imports in test", {

  # Path to example test data
  csv_path <- testthat::test_path("data", "patient_data.csv")

  # Load the data and check it was read
  df <- import_patient_data(csv_path)
  expect_gt(nrow(df), 0)
})
